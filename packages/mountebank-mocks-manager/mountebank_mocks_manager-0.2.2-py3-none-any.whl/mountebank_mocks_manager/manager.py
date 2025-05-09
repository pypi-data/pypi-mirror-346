import json
import os
import subprocess
import time

from contextlib import contextmanager
from pathlib import Path

import pytest

from filelock import FileLock
from funcy import select_keys
from pathvalidate import sanitize_filename
from pytest import FixtureRequest

from mountebank_mocks_manager.logger import logger
from mountebank_mocks_manager.plugins.patchers import patch_some_service
from mountebank_mocks_manager.plugins.post_processors import PostProcessor
from mountebank_mocks_manager.plugins.processors import CommonProcessor
from mountebank_mocks_manager.server import MBServer


class ModeNotAllowed(Exception):
    def __init__(
        self, message='Semi proxy mode is not allowed in parallel mode', *args, **kwargs
    ):
        super().__init__(message, *args, **kwargs)


class MocksManager:
    REPLACE_DATES_IMPOSTERS = {'imposter_name'}
    RECORD_REQUESTS_IMPOSTERS = {'imposter_name'}

    def __init__(
        self,
        request: FixtureRequest = None,
        imposters_root: str | Path = None,
        parallel: bool = False,
        session_id: str = None,
        mb_server_host: str = None,
        mb_server_port: int = None,
        proxy_enabled: bool = False,
        semi_proxies: list | None = None,
        proxy_wait: bool = False,
        proxy_wait_time: int = 1,
        services: dict = None,
    ):
        self.session_id = session_id
        self.request = request
        self.mocks_settings = 1
        self.imposters_root = Path(imposters_root or '')
        self.parallel_mode = parallel
        self.mountebank_server = MBServer(mb_server_host, mb_server_port)

        self.test_path = self.get_test_path()

        # Available markers
        self.proxy_enabled = proxy_enabled
        self.semi_proxies = semi_proxies or []
        self.proxy_wait = proxy_wait
        self.proxy_wait_time = proxy_wait_time

        # Custom markers:
        # Add custom attributes to init to support custom pytest markers

        self.read_test_markers()

        self.mocks_lock = FileLock(self.imposters_root / 'mocks.lock')

        self.services = services

    def read_test_markers(self):
        if self.request is None:
            # Ability to use MMM in session or isolated scope
            return

        if self.request.node.get_closest_marker(name='force_proxy'):
            self.proxy_enabled = True

        if self.request.node.get_closest_marker(name='skip_in_proxy_mode'):
            if self.proxy_enabled:
                pytest.skip('Skipping in proxy mode')

        if self.request.node.get_closest_marker(name='proxy_wait'):
            self.proxy_wait = True

        if marker := self.request.node.get_closest_marker(name='imposters'):
            main_test = marker.kwargs.get('main', False)
            if self.proxy_enabled and not main_test:
                pytest.skip('Skipping in proxy mode')

        if marker := self.request.node.get_closest_marker(name='semi_proxies'):
            self.semi_proxies = marker.kwargs.get('imposters', [])
            if self.parallel_mode and self.semi_proxies:
                raise ModeNotAllowed()

        return True

        # Extend this method to support custom pytest markers

    def get_test_path(self):
        if self.request is None:
            return ''

        if marker := self.request.node.get_closest_marker(name='imposters'):
            # Try to find imposters path in custom pytest.mark first
            custom_imposters_path = marker.kwargs.get('path')
            test_imposters_path = os.path.join('tests', custom_imposters_path)
        else:
            # Construct imposters' paths for imposters for specific test
            test_full_name = self.request.node.name
            if not self.request.node.get_closest_marker(name='parametrize'):
                test_full_name = test_full_name.split('[')[0]

            test_path = self.request.function.__module__
            test_modules = [i.removeprefix('test_') for i in test_path.split('.')]
            test_names = [
                sanitize_filename(i)
                for i in test_full_name.removeprefix('test_')
                .removesuffix(']')
                .split('[')
            ]

            test_imposters_path = os.path.join(*test_modules, *test_names)

        return test_imposters_path

    def get_imposters_from_path(self, dir_path: str | Path):
        imposters = dict()

        dir_path = Path(dir_path)

        if not dir_path.exists():
            logger.warning(f'No imposters data found in {dir_path}')
            return imposters

        for path in dir_path.iterdir():
            full_path = dir_path / path
            if full_path.is_file() and full_path.suffix == '.json':
                imposter_name = path.stem
                imposter = self.services.get(imposter_name)
                if imposter:
                    imposter_str = full_path.read_text()
                    imposter_str = self.pre_load_patch_imposter(
                        imposter_name, imposter_str
                    )
                    imposter_stubs = json.loads(imposter_str)
                    imposters[imposter_name] = {
                        'stubs': imposter_stubs,
                        'port': imposter.get('port'),
                    }
                else:
                    logger.warning(f'Unknown imposter found: {imposter_name}')

        imposters = self.post_load_patch_imposters(imposters)

        return imposters

    def set_stubs_serial(self, imposter_port: int, imposter_name: str, stubs: list):
        """
        Used to set stubs in non-parallel mode, when only one test can be active
        """
        if self.mountebank_server.get_imposter_details(imposter_port) is not None:
            logger.warning(f' - {imposter_name} updated')
            self.mountebank_server.delete_imposter(imposter_port)
        else:
            logger.info(f' - {imposter_name} set')
        self.mountebank_server.add_imposter(
            port=imposter_port,
            name=imposter_name,
            stubs=stubs,
        )

    def set_stubs_parallel(self, imposter_port: int, imposter_name: str, stubs: list):
        """
        Used to set stubs in parallel mode, when several tests can be active
        """
        with self.mocks_lock:
            old_stubs = self.mountebank_server.get_imposter_stubs(imposter_port)
            new_stubs = self.set_stubs_session_ids(stubs, self.session_id)

            if old_stubs is None:
                self.mountebank_server.add_imposter(
                    port=imposter_port,
                    name=imposter_name,
                    stubs=new_stubs,
                    record_requests=imposter_name in self.RECORD_REQUESTS_IMPOSTERS,
                )
            else:
                self.mountebank_server.add_stubs(port=imposter_port, stubs=new_stubs)

    def set_proxy_stubs(self, imposter_port: int, imposter_name: str, stubs: list):
        self.mountebank_server.add_imposter(
            port=imposter_port,
            name=imposter_name,
            stubs=stubs,
        )

    def unset_proxy_stubs(self, imposter_port: int):
        self.mountebank_server.delete_imposter(imposter_port)

    def set_test_stubs(self, imposter_port: int, imposter_name: str, stubs: list):
        if self.parallel_mode:
            self.set_stubs_parallel(imposter_port, imposter_name, stubs)
        else:
            self.set_stubs_serial(imposter_port, imposter_name, stubs)

    def unset_test_stubs(self, imposter_port: int):
        with self.mocks_lock:

            old_stubs = self.mountebank_server.get_imposter_stubs(imposter_port)
            stubs_ids = self.get_stubs_ids_to_remove_by_session_id(
                old_stubs, self.session_id
            )

            if len(stubs_ids) == len(old_stubs):
                self.mountebank_server.delete_imposter(port=imposter_port)
            else:
                self.mountebank_server.remove_stubs(
                    port=imposter_port, indices=stubs_ids
                )

    def set_imposters_from_path(
        self,
        imposters_path: str | Path,
        full_path: bool = False,
        imposters_names: list[str] | None = None,
    ):
        if not full_path:
            imposters_path = os.path.join(self.imposters_root, imposters_path)
        imposters = self.get_imposters_from_path(imposters_path)
        if imposters_names:
            imposters = select_keys(lambda x: x in imposters_names, imposters)
        logger.info(f' Loading mocks from: {imposters_path}')
        for imposter_name, imposter_data in imposters.items():
            imposter_port = imposter_data['port']
            stubs = imposter_data['stubs']
            if self.proxy_enabled:
                self.set_proxy_stubs(imposter_port, imposter_name, stubs)
            else:
                self.set_test_stubs(imposter_port, imposter_name, stubs)

    def unset_imposters_from_path(self, imposters_path: str | Path, full=False):
        if not full:
            imposters_path = os.path.join(self.imposters_root, imposters_path)
        imposters = self.get_imposters_from_path(imposters_path)
        logger.info(f' Unloading mocks from: {imposters_path}')
        for imposter_name, imposter_data in imposters.items():
            imposter_port = imposter_data['port']
            if self.proxy_enabled:
                self.unset_proxy_stubs(imposter_port)
            else:
                self.unset_test_stubs(imposter_port)

    def set_common_imposters(self):
        self.set_imposters_from_path('common')

    def unset_common_imposters(self):
        self.unset_imposters_from_path('common')

    def set_proxy_imposters(self):
        self.set_imposters_from_path('proxies')

    def set_semi_proxy_imposters(self, imposters_names: list[str]):
        self.set_imposters_from_path('proxies', imposters_names=imposters_names)

    def unset_proxy_imposters(self):
        self.unset_imposters_from_path('proxies')

    def set_test_imposters(self, group_name: str = '', test_path: str | Path = None):
        if test_path is None:
            test_path = self.test_path
        full_imposters_path = os.path.join(test_path, group_name)
        self.set_imposters_from_path(full_imposters_path)

    def unset_test_imposters(self, group_name: str = '', test_path: str | Path = None):
        if test_path is None:
            test_path = self.test_path
        full_imposters_path = os.path.join(test_path, group_name)
        self.unset_imposters_from_path(full_imposters_path)

    def set_imposters(
        self,
        group_name: str = '',
        test_path: str | Path = None,
        semi_proxies: list[str] | None = None,
    ):
        if group_name:
            logger.info(f' Group: **{group_name}**')
        if self.proxy_enabled:
            self.set_proxy_imposters()
        else:
            self.set_common_imposters()
            self.set_test_imposters(group_name, test_path)
            semi_proxies = self.semi_proxies + (semi_proxies or [])
            if semi_proxies:
                if self.parallel_mode:
                    raise ModeNotAllowed()
                self.set_semi_proxy_imposters(semi_proxies)

    def unset_imposters(
        self,
        group_name: str = '',
        test_path: str | Path = None,
        wait: bool = False,
        rewrite_allowed: bool = True,
        semi_proxies: list[str] | None = None,
    ):
        semi_proxies = self.semi_proxies + (semi_proxies or [])
        if self.proxy_enabled:
            if rewrite_allowed:
                self.process_imposters(
                    group_name=group_name, test_path=test_path, wait=wait
                )
            self.unset_proxy_imposters()
        elif semi_proxies:
            if self.parallel_mode:
                raise ModeNotAllowed()
            if rewrite_allowed:
                self.process_imposters(
                    group_name=group_name, test_path=test_path, wait=wait
                )
            self.mountebank_server.delete_all_imposters()
        else:
            if self.parallel_mode:
                self.unset_common_imposters()
                self.unset_test_imposters(group_name, test_path)
            else:
                self.mountebank_server.delete_all_imposters()

    def process_imposters(
        self,
        group_name: str = '',
        test_path: str | Path = None,
        wait: bool = False,
    ):
        logger.info('Creating new imposters based on proxy data')
        if self.proxy_wait or wait:
            logger.info(
                f'Sleeping {self.proxy_wait_time}s for collecting requests to mocks'
            )
            time.sleep(self.proxy_wait_time)
        logger.info('Generating mocks for tests')
        if test_path is None:
            test_path = self.test_path
        test_imposters_path = os.path.join(test_path, group_name)

        full_imposters_path = os.path.join(self.imposters_root, test_imposters_path)
        raw_imposters_path = os.path.join(full_imposters_path, '_raw')

        recorded_imposters = self.mountebank_server.all_imposters_details()
        processed_imposters = self.common_processors(recorded_imposters)

        self.dump_imposters(processed_imposters, raw_imposters_path)
        post_processed_imposters = self.post_processors(processed_imposters)

        self.dump_imposters(
            post_processed_imposters,
            full_imposters_path,
            git_add=True,
            raw=False,
        )

    def dump_imposters(
        self,
        recorded_stubs: dict,
        folder_path: str,
        git_add: bool = False,
        raw: bool = True,
    ):
        for imposter_name, stubs in recorded_stubs.items():
            if len(stubs):
                if git_add:
                    logger.info(f'Dumping {imposter_name} imposter')
                filename = f'{imposter_name}.json'
                filepath = os.path.join(folder_path, filename)
                os.makedirs(folder_path, exist_ok=True)
                with open(filepath, 'w') as imposter_file:
                    stubs_str = json.dumps(stubs, indent=2)
                    stubs_str = self.pre_dump_patch_stubs(imposter_name, stubs_str, raw)
                    imposter_file.write(stubs_str)
                if git_add:
                    subprocess.run(['git', 'add', filepath])

    @contextmanager
    def mocks_group(
        self,
        group_name: str = '',
        test_path: str | None = None,
        wait: bool = False,
        rewrite_allowed: bool = True,
        semi_proxies: list[str] | None = None,
        **kwargs,
    ):
        try:
            for key, value in kwargs.items():
                # Ability to create custom markers or patch some attributes via mocks_group
                if hasattr(self, key):
                    setattr(self, key, value)

            self.set_imposters(
                group_name=group_name, test_path=test_path, semi_proxies=semi_proxies
            )
            yield
        finally:
            self.unset_imposters(
                group_name=group_name,
                test_path=test_path,
                wait=wait,
                rewrite_allowed=rewrite_allowed,
                semi_proxies=semi_proxies,
            )

    # Methods to override
    @classmethod
    def set_log_level(cls, log_level: str):
        logger.setLevel(log_level)

    def common_processors(self, recorded_imposters: dict):
        # Override this method to use your own rules for processing imposters
        return CommonProcessor.process(recorded_imposters)

    def post_processors(self, processed_imposters: dict):
        # Override this method to use your own rules for post-processing imposters
        return PostProcessor.process(processed_imposters)

    def pre_load_patch_imposter(self, imposter_name: str, imposter_str: str):
        # Override this method to patch your imposter before it was loaded and transformed from str to dict
        if imposter_name:
            return imposter_str

    def post_load_patch_imposters(self, imposters: dict):
        # Override this method to patch your imposters after they were loaded
        return patch_some_service(imposters, '/example', 'example')

    def pre_dump_patch_stubs(self, imposter_name: str, stubs_str: str, raw: bool):
        # Override this method to patch your stubs right before they were dumped in str
        if imposter_name or raw:
            return stubs_str

    def set_stubs_session_ids(self, stubs: list, session_id: str):
        """Override this method to introduce your own patching mocks with session ids
        to use them in parallel run"""
        return stubs

    def get_stubs_ids_to_remove_by_session_id(self, stubs: list, session_id: str):
        """Override this method to introduce your own logic to get list
        of stubs to remove by session ids during parallel run in unset imposters method
        """
        return [stubs.index(stub) for stub in stubs]
