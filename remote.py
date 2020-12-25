import json
from string import Template

import requests
from w3lib.url import urljoin
from zacoby import exceptions
from zacoby.logger import create_default_logger


class RemoteConnection:
    parsed_url = None
    remote_server_address = None
    session_id = None

    def __init__(self, remote_server_address, resolve_ip=False):
        self.logger = create_default_logger(self.__class__.__name__)
        self.remote_server_address = remote_server_address
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Zacoby (python)'
        }

    def __call__(self, sender, signal):
        self.session_id = sender.session_id

    def _precheck_command(self, command):
        if not isinstance(command, list):
            raise TypeError('The command should be a list')
        
        if not isinstance(command[-1], list):
            raise TypeError('The command carachteristics should be a list')

        if not command[-1][-1].startswith('/'):
            raise ValueError(f"{command[-1][-1]} is not a valid path")

        return command
    
    def _execute_command(self, command, **kwargs):
        # A command should contain a name and an additional
        # list with a http method and a path to which the 
        # command has to be sent
        name, characteristics = self._precheck_command(command)

        method, path = characteristics
        if 'session' in kwargs:
            path_to_substitute = Template(path)
            session = kwargs.pop('session') or self.session_id
            path = path_to_substitute.substitute(
                **{'sessionId': session}
            )

        request_url = urljoin(self.remote_server_address, path)
        self.logger.info(f'Executing command: {name.title()}')
        return self._http_request(method, request_url, **kwargs)

    def _http_request(self, method, request_url, **kwargs):
        kwargs_keys = kwargs.keys()

        capabilities = {}
        if 'capabilities' in kwargs_keys:
            # Reconstruct the dictionnary because
            # W3C compliance requires that the key 'capabilities'
            # be in the list of parameters
            capabilities = {'capabilities': kwargs.pop('capabilities')}
        else:
            # In certain cases (e.g. get()) we want to pass
            # certain specific commands like *url* so just
            # pass these elements as capabilities in order
            # to be able to exit these specific requests
            capabilities = kwargs.copy()

            if 'element' in kwargs:
                capabilities.update({'id': kwargs.pop('element')})

        headers = {}
        if 'headers' in kwargs_keys:
            headers = {**headers, **kwargs.pop('headers')}
        
        response = None

        try:
            if method == 'GET':
                response = requests.get(request_url, headers=headers)

            if method == 'POST':
                # IMPORTANT: The capabilities should be passed as a
                # string to the POST request otherwise the service
                # will raise a missing command parameters error
                response = requests.post(
                    request_url, data=json.dumps(capabilities), headers=headers
                )

            if method == 'DELETE':
                response = requests.delete(request_url)
        except Exception as e:
            raise ConnectionError('Could not send request to the browser', e.args)
        else:
            if response is not None:
                response_data = response.content.decode('utf-8')

                if 300 <= response.status_code <= 304:
                    return self._request('GET', response.headers.get('location'))

                try:
                    response_json = response.json()
                except json.JSONDecodeError:
                    self.logger.error('Response does not contain a JSON object')
                    # Technically a valid response should return a JSON
                    # object containing stuff such as the capabilities,
                    # the session ID etc
                    return {'value': None}
                else:
                    if 399 < response.status_code <= 500:
                        return dict(status=response.status_code, data=response_data, **response_json)
                    
                    return dict(status=response.status_code, data=response_data, **response_json)
        finally:
            if response is None:
                raise exceptions.NoReponseError()
            response.close()
