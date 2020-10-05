import base64
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from zacoby.exceptions import errors
from zacoby.utils.utils import (get_available_ip, join_host_and_port,
                                test_socket_connection)


class RemoteConnection:
    """ 
    Create a new remote connection to control
    the given browser by sending commands for
    the current web driver

    Description
    -----------

    By calling the `run_commands` method, a request
    is sent to the browser using a specific command
    based on a W3C compliant path e.g. /get/sessionId
    """
    url = None
    parsed_url = None
    remote_server_address = None

    @classmethod
    def as_class(cls, remote_server_address):
        """Create a new RemoteConnection instance

        Parameters
        ----------

            - remote server address (str): the http url to use
              for the remote connection

        Returns
        -------

            - type: a new instanciated remote connection
        """
        cls.remote_server_address = remote_server_address
        cls._init(cls)
        return cls()

    @classmethod
    def _run_command(cls, command, **kwargs):
        """
        Run a command with the remote which sends
        a request using a W3C complient path
        -----

        Parameters
        ----------

            - command (list, tuple): the command to send to the remote server
              which should be of form (name, (method, path))

        Returns
        -------

            - dict:  the status code with the reponse data
        """
        command_name, method_and_path = command
        print("Running the following command", command_name, method_and_path)
        return cls._request(cls, method_and_path[-0], cls._build_url(cls, method_and_path[-1]))

    def _get_headers(self, keep_alive=False):
        base = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Zacoby (python)'
        }

        if self.parsed_url.username:
            authentication = f'{self.parsed_url.username}:{self.parsed_url.password}'.encode()
            base.update(
                {
                    'Authorization': f'Basic {authentication}'
                }
            )

        if keep_alive:
            base.update(
                {
                    'Connection': 'keep-alive'
                }
            )

        return base

    def _request(self, method, url, body:dict = {}, **kwargs):
        """
        Send an HTTP request to the remote server and
        return a valid response

        -----

        Parameters
        ----------

            - method (str): GET or POST

            - url (str): the url to use for the request

            - headers (dict): extra headers to use with the
              base headers

        Returns
        -------

            - dict:  the status code with the reponse data
        """
        print('Trying to send request to', method, 'to', url)

        response = None
        headers = self._get_headers()

        if 'capabilities' in kwargs:
            capabilities = kwargs.pop('capabilities')
            body = {**capabilities, **body}

        if 'headers' in kwargs:
            headers = {**headers, **kwargs['headers']}


        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)

            if method == 'POST':
                response = requests.post(url, body=body, headers=headers)
        except:
            pass
        else:
            if response is not None:
                response_data = response.content.decode('utf-8')
                if 300 <= response.status_code <= 304:
                    return self._request('GET', response.headers.get('locaton'))

                if 399 < response.status_code <= 500:
                    return dict(status=response.status_code, value=response_data)

                return dict(status=0, value=response_data)
        finally:
            if response is None:
                raise errors.NoResponseError()
            response.close()

    def _init(self, resolve_ip=True):
        """Initializes the remote connection in
        order for it to be used

        Parameters
        ----------

            resolve_ip (bool, optional): [description]. Defaults to True.
        """
        if self.remote_server_address is not None:
            parsed_url = urlparse(self.remote_server_address)

            if parsed_url.hostname and resolve_ip:
                port = parsed_url.port or None
                ip_address = None

                if parsed_url.scheme == 'https':
                    ip_address = parsed_url.hostname
                elif port and not test_socket_connection(parsed_url.hostname, port):
                    print('Could not connect to port on host >> LOG')
                else:
                    ip_address = get_available_ip(parsed_url.hostname, port=port)
                
                netloc = join_host_and_port(ip_address, port)

                authentication = ''
                if parsed_url.username:
                    pass
                   
                remote_server_address = urlunparse(
                    (
                        parsed_url.scheme, 
                        netloc, 
                        parsed_url.path,
                        parsed_url.params, 
                        parsed_url.query,
                        parsed_url.fragment
                    )
                )
                self.url = remote_server_address
                self.parsed_url = parsed_url
    
    def _build_url(self, path_or_command):
        """
        Join the url with W3C complient path

        Parameters
        ----------

            - path (list, str): the command as list or the
              W3C complient path as a string

        Returns
        -------

            str: the joined url
        """
        if isinstance(path_or_command, list):
            path_or_command = path_or_command[-1]
        return urljoin(self.url, path_or_command)
