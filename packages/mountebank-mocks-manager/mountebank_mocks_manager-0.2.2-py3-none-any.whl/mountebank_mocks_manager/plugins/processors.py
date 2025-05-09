import base64
import gzip
import json
import zlib

from copy import deepcopy


class CommonProcessor:
    @staticmethod
    def has_proxy_stub(imposter):
        for stub in imposter['stubs']:
            for response in stub['responses']:
                if 'proxy' in response:
                    return True
        return False

    @staticmethod
    def remove_proxy_stubs(imposter):
        filtered_stubs = list()
        for stub in imposter['stubs']:
            for response in stub['responses']:
                if 'proxy' not in response:
                    filtered_stubs.append(stub)
        return filtered_stubs

    @classmethod
    def get_recorded_imposters(cls, imposters):
        """Retrieve all stubs that were recorded by proxy imposters"""
        recorded_imposters = dict()
        for name, stubs in imposters.items():
            if cls.has_proxy_stub(stubs):
                recorded_imposters[name] = cls.remove_proxy_stubs(stubs)

        return recorded_imposters

    @staticmethod
    def as_json(body):
        """Try to convert body to json, return original body on error"""
        try:
            return json.loads(body)
        except (ValueError, TypeError):
            return body

    @staticmethod
    def deflate(body, codec):
        """Try to deflate body, return original body on error"""
        try:
            body_bytes = base64.urlsafe_b64decode(body)
            decompressed_body = zlib.decompress(body_bytes)
            return decompressed_body.decode(codec)
        except (TypeError, Exception):
            return body

    @staticmethod
    def decompress(body):
        """Try to decompress body, return original body on error"""
        try:
            body_bytes = base64.urlsafe_b64decode(body)
            decompressed_body = gzip.decompress(body_bytes)
            return decompressed_body.decode('utf-8')
        except (TypeError, Exception):
            return body

    @classmethod
    def decode_body(cls, body: str):
        body = cls.deflate(body, 'utf-8')
        body = cls.deflate(body, 'cp1252')
        body = cls.decompress(body)
        body = cls.as_json(body)
        return body

    @classmethod
    def process_predicates(cls, stub):
        """Process predicates in recorded mock definition in a more convenient way to use them
        in the future"""
        prepared_stub = deepcopy(stub)
        for predicate in prepared_stub['predicates']:
            for key, value in predicate.items():
                if isinstance(value, dict) and 'body' in value:
                    predicate[key]['body'] = cls.as_json(predicate[key]['body'])
        return prepared_stub

    @classmethod
    def process_responses(cls, stub):
        """Process responses in recorded mock definition in a more convenient way to use them
        in future"""
        prepared_stub = deepcopy(stub)
        for response in prepared_stub['responses']:
            for key, value in response.items():
                if isinstance(value, dict):
                    if 'body' in value:
                        response[key]['body'] = cls.decode_body(response[key]['body'])
        return prepared_stub

    @classmethod
    def process_imposter(cls, stubs):
        processed_stubs = list()

        for stub in stubs:
            processed_stub = deepcopy(stub)
            processed_stub.pop('_links')
            processed_stub = cls.process_predicates(processed_stub)
            processed_stub = cls.process_responses(processed_stub)
            processed_stubs.append(processed_stub)

        return processed_stubs

    @classmethod
    def process(cls, imposters):
        recorded_imposters = cls.get_recorded_imposters(imposters)
        for name, stubs in recorded_imposters.items():
            recorded_imposters[name] = cls.process_imposter(stubs)
        return recorded_imposters
