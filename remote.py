import json
from typing import Callable

import requests
from w3lib.url import urljoin

from zacoby import exceptions, global_logger


class Response:
    def __init__(self, response, **kwargs):
        self._response = response
        # self.json = response.json()
        # self.response_data = response.content.decode('utf-8)
        self.response_data = {'data': ''}
        self.json = {'a': 1}
        self.status = 200
        self.kwargs = kwargs

    def __str__(self):
        return self.response_data

    def __repr__(self):
        return f'{self.__class__.__name__}({self.response_data})'

    def __getitem__(self, key):
        return self.json[key]

    @property
    def data(self):
        return self.response_data['data']

    def decompose(self):
        keys = list(self.json.keys())[0]
        value = list(self.json.values())[0]
        return keys, value


class RemoteConnection:
    """
    Class that encapsulates functionnalities for sending
    requests to the browser
    """
    parsed_url = None
    remote_server_address = None

    SESSION_ID = None

    def __init__(self, remote_server_address: str, resolve_ip: bool=False):
        # signal.connect(self)

        self.remote_server_address = remote_server_address
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Zacoby (python)'
        }

    def _execute_command(self, command: Callable, requires_session_id: bool=False, **kwargs):
        """
        Send a command to the browser

        Parameters
        ----------

            command (Callable): [description]

        Returns
        -------

            [type]: [description]
        """
        # if 'session' in kwargs:
        if requires_session_id:
            # self.SESSION_ID = kwargs.pop('session')
            command.implement_attribute(session_id=self.SESSION_ID)
            
        global_logger.info(f'Executing command: {command.name}')

        request_url = urljoin(self.remote_server_address, command.path)
        return self._http_request(command.method, request_url, **kwargs)

    def _http_request(self, method, request_url, **kwargs):
        capabilities = {}
        if 'capabilities' in kwargs:
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
        if 'headers' in kwargs:
            headers = {**headers, **kwargs.pop('headers')}
        
        response = None
        # return dict(status=200, data={}, response_json=None)
        return Response(response, method=method, request_url=request_url)
        # try:
        #     # signal.send('Navigate.Before', self)
            
        #     if method == 'GET':
        #         response = requests.get(request_url, headers=headers)

        #     if method == 'POST':
        #         # IMPORTANT: The capabilities should be passed as a
        #         # string to the POST request otherwise the service
        #         # will raise a missing command parameters error
        #         response = requests.post(
        #             request_url, data=json.dumps(capabilities), headers=headers
        #         )

        #     if method == 'DELETE':
        #         response = requests.delete(request_url)
        # except ConnectionError:
        #     raise
        # except Exception as e:
        #     message = 'Could not send request to the browser'
        #     global_logger.error(message, stack_info=True)
        #     raise ConnectionError(message, e.args)
        # else:
        #     if response is not None:
        #         response_data = response.content.decode('utf-8')

        #         # signal.send('Navigate.After', sender=self, method=method, request_url=request_url)

        #         if 300 <= response.status_code <= 304:
        #             return self._request('GET', response.headers.get('location'))

        #         try:
        #             response_json = response.json()
        #         except json.JSONDecodeError:
        #             global_logger.error('Response does not contain a JSON object')
        #             # Technically a valid response should return a JSON
        #             # object containing stuff such as the capabilities,
        #             # the session ID etc
        #             return {'value': None}
        #         else:
        #             if 399 < response.status_code <= 500:
        #                 return dict(status=response.status_code, data=response_data, **response_json)
                    
        #             return dict(status=response.status_code, data=response_data, **response_json)
        # finally:
        #     if response is None:
        #         global_logger.error('No response was returned.', stack_info=True)
        #         raise exceptions.NoReponseError()
        #     response.close()
