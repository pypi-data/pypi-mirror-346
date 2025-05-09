import json

from copy import deepcopy

from funcy import group_by


def process_stubs_some_service(stubs):
    processed_stubs = list()

    for stub in stubs:
        processed_stub = deepcopy(stub)
        # do some magic here
        processed_stubs.append(processed_stub)

    return processed_stubs


def process_stubs_another_service(stubs):
    processed_stubs = list()

    for stub in stubs:
        processed_stub = deepcopy(stub)
        # do another magic here
        processed_stubs.append(processed_stub)

    return processed_stubs


class PostProcessor:
    @staticmethod
    def merge_duplicate_responses(stub):
        # Recursively merges response with the
        # next one in queue if they are identical
        # increasing repeat volume accordingly
        processed_stub = deepcopy(stub)
        processed_responses = list()
        last_response = dict()
        for response in processed_stub['responses']:
            if last_response.get('is') == response.get('is'):
                last_response['repeat'] = last_response.get('repeat', 1) + response.get(
                    'repeat', 1
                )
            else:
                if last_response:
                    processed_responses.append(last_response)
                last_response = deepcopy(response)
        if last_response:
            processed_responses.append(last_response)
        processed_stub['responses'] = processed_responses
        return processed_stub

    @staticmethod
    def set_repeat_responses(stub):
        # If multiple responses received for one set of predicates - set repeat
        # parameter for all except last one
        # see more https://www.mbtest.org/docs/api/stubs
        # It's impossible to set infinite times for repeat,
        # So setting 999999 for the last one
        processed_stub = deepcopy(stub)
        for response in processed_stub['responses'][:-1]:
            response['repeat'] = 1
        processed_stub['responses'][-1]['repeat'] = 999999
        return processed_stub

    @classmethod
    def process_responses(cls, stub):
        prepared_stub = cls.set_repeat_responses(stub)
        for response in prepared_stub['responses']:
            for key, value in response.items():
                if isinstance(value, dict):
                    response[key].pop('headers', None)
                    response[key].pop('_mode', None)
                    response[key].pop('_proxyResponseTime', None)
        prepared_stub = cls.merge_duplicate_responses(prepared_stub)
        return prepared_stub

    @staticmethod
    def group_duplicate_predicates(stubs):
        """
        Group stubs by their predicates
        """
        new_stubs = list()
        for stub_group in group_by(
            lambda item: json.dumps(item['predicates'], sort_keys=True), stubs
        ).values():
            new_stub = stub_group[0]
            for stub in stub_group[1:]:
                new_stub['responses'] += stub['responses']
            new_stubs.append(new_stub)
        return new_stubs

    @classmethod
    def process_stubs(cls, stubs: list):
        processed_stubs = list()

        for stub in cls.group_duplicate_predicates(stubs):
            processed_stub = deepcopy(stub)
            processed_stub = cls.process_responses(processed_stub)
            processed_stubs.append(processed_stub)

        return processed_stubs

    @classmethod
    def process(cls, imposters: dict):
        # Check this example how to write your own post-processor
        processed_imposters = deepcopy(imposters)
        for name, stubs in processed_imposters.items():
            match name:
                case 'some_service':
                    processed_imposters[name] = process_stubs_some_service(stubs)
                case 'another_service':
                    processed_imposters[name] = process_stubs_another_service(stubs)

            processed_imposters[name] = cls.process_stubs(processed_imposters[name])

        return processed_imposters
