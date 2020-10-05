from urllib.parse import urljoin, urlparse, urlunparse

import requests


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
        method, path = command
        print(cls, method, path)
        return cls._request(cls, method, cls._build_url(cls, path))

    def _request(self, method, url):
        """
        Send an HTTP request to the remote server and
        return a valid response

        -----

        Parameters
        ----------

            - method (str): GET or POST

            - url (str): the url to use for the request

        Returns
        -------

            - dict:  the status code with the reponse data
        """
        headers = None
        response = None
        try:
            from requests.models import Response
            response = Response()
            response.headers = {
                'Content-Type': 'text/html'
            }
            response.status_code = 200
            with open('D:\\coding\\personnal\\zacoby\\response.html', 'rb') as f:
                response.content = f.read()
                
            print('A request was sent using', method, 'to', url)

            # if method == 'GET':
            #     response = requests.get(url, body={}, headers={})

            # if method == 'POST':
            #     response = requests.post(url, body={}, headers={})
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
            response.close()
            print('Response was closed')


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
                ip = None
                if parsed_url.scheme == 'https':
                    ip = parsed_url.hostname
                elif ip == 'is not connectable':
                    pass
                else:
                    ip = 'find an IP to which we can connect'

                netloc = 'join ip and parsed_url.port'

                authentication = ''
                if parsed_url.username:
                    authentication = parsed_url.username
                    if parsed_url.password:
                        authentication += f':{parsed_url.password}'
                    netloc = f'{authentication}@{netloc}'
                remote_server_address = urlunparse(
                    (parsed_url.scheme, netloc, parsed_url.path,
                        parsed_url.params, parsed_url.query,
                        parsed_url.fragment)
                )
                self.url = remote_server_address
            else:
                pass
        else:
            pass
    
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
