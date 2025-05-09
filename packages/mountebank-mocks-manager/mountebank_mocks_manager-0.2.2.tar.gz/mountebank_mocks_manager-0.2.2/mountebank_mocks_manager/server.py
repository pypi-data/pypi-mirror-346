from furl import furl
from requests import Session


class MBServer:
    DEFAULT_RESPONSE = {
        'statusCode': 418,
        'body': 'No appropriate mock was found. '
        'Check whether request was changed or mocks definition were outdated',
    }

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = Session()

    @property
    def url(self):
        return f'http://{self.host}:{self.port}'

    def add_imposter(self, port, name, stubs, record_requests=True):
        url = furl(self.url, path='/imposters')
        payload = {
            'port': port,
            'name': name,
            'protocol': 'http',
            'stubs': stubs,
            'recordRequests': record_requests,
            'defaultResponse': self.DEFAULT_RESPONSE,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()

    def add_stub(self, port, stub):
        url = furl(self.url, path=f'/imposters/{port}/stubs')
        payload = {'stub': stub}
        response = self.session.post(url, json=payload)
        response.raise_for_status()

    def add_stubs(self, port, stubs):
        for stub in stubs:
            self.add_stub(port, stub)

    def remove_stub(self, port, index):
        url = furl(self.url, path=f'/imposters/{port}/stubs/{index}')
        response = self.session.delete(url)
        response.raise_for_status()

    def remove_stubs(self, port, indices):
        for index in reversed(indices):
            self.remove_stub(port, index)

    def overwrite_stubs(self, port, stubs):
        url = furl(self.url, path=f'/imposters/{port}/stubs')
        payload = {'stubs': stubs}
        response = self.session.put(url, json=payload)
        response.raise_for_status()
        return response

    def update_stubs(self, port, stubs):
        for stub in stubs:
            self.add_stub(port, stub)

    def all_imposters(self):
        url = furl(self.url, path='/imposters')
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_imposter_details(self, port):
        url = furl(self.url, path=f'/imposters/{port}')
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()

    def get_imposter_stubs(self, port):
        imposter_details = self.get_imposter_details(port)
        if imposter_details:
            return imposter_details['stubs']

    def delete_imposter(self, port):
        url = furl(self.url, path=f'/imposters/{port}')
        response = self.session.delete(url)
        response.raise_for_status()

    def delete_all_imposters(self):
        url = furl(self.url, path='/imposters')
        response = self.session.delete(url)
        response.raise_for_status()

    def all_imposters_details(self):
        all_imposters = self.all_imposters()
        all_details = dict()
        for imposter in all_imposters['imposters']:
            details = self.get_imposter_details(imposter['port'])
            name = imposter['name']
            all_details[name] = details
        return all_details

    def get_requests_on_port(self, port):
        mock_details = self.get_imposter_details(port)
        return mock_details['requests']
