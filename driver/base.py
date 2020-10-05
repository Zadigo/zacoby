import socket

from zacoby.browsers.capabilities import CHROME
from zacoby.driver.remote import RemoteConnection
from zacoby.driver.wait import Wait
from zacoby.exceptions import errors
from zacoby.service.base import Service
from zacoby.service.commands import BrowserCommands


class Zacoby(type):
    def __new__(cls, name, bases, cls_dict):
        new_class = super().__new__(cls, name, bases, cls_dict)
        if hasattr(new_class, 'capabilities'):
            capabilities = getattr(new_class, 'capabilities')
            if capabilities is None:
                # By default, if capabilities is not set
                # just use the default Chrome capabilities
                setattr(new_class, 'capabilities', CHROME)

        if hasattr(new_class, 'port'):
            if getattr(new_class, 'port') is None:
                setattr(new_class, 'port', cls.set_port())
        return new_class

    @classmethod
    def set_port(cls):
        # If no port was provided,
        # we have to try and find
        # an open port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 0))
        s.listen(5)
        available_port = s.getsockname()[1]
        s.close()
        return available_port

        

class BaseDriver(metaclass=Zacoby):
    """
    Controls the browser by sending commands to the
    remote server or connection

    Parameters
    ----------

        - executable (str): path to the driver executable

        - host (str, optional): . Defaults to None

        - port (int, optional): . Defaults to None
    """
    capabilities = None
    host = None
    port = None
    ssession_id = None

    def __init__(self, executable):
        BrowserCommands._construct()

        new_service = Service(executable, self.host, self.port)
        new_service.start()
        self.new_service = new_service

        remote_server_address = f'http://localhost:{self.port}'
        self.new_remote_connection = RemoteConnection.as_class(remote_server_address)

        self.start_session(self.capabilities, None)

    def __repr__(self):
        return f'< {self.__class__.__name__} ([{self.session_id}]) >'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def _run_command(self, command, **kwargs):
        response = self.new_remote_connection._execute_command(command, **kwargs)
        if response:
            return response
        return dict(success=0, value=None, sesssion_id=None)

    def start_session(self, capabilities, browser_profile=None):
        """
        Start a new browser session using the
        provided capabilities

        Parameters
        ----------

            - capabilities (dict): [description]

            - browser_profile (str): [description]
        """
        if browser_profile:
            pass

        extended_capabilities = self._fit_transform_capabilities(capabilities)
        print('New session was started using:', extended_capabilities)

        response = self._run_command(
            BrowserCommands.NEW_SESSION, capabilities=extended_capabilities
        )

        if 'sessionId' not in response:
            pass

        # self.session = response['sessionId']
        # self.capabilities = response.get('value')

        # if self.capabilities is None:
        #     self.capabilities = response.get('capabilities')

    def _fit_transform_capabilities(self, capabilities:dict, **kwargs):
        """In order to match the W3C capabilities, we have wrap it's values
        into something acceptable

        Parameters
        ----------

            capabilities (dict): a dictionnary of capabilities

        Returns:
            dict: a wrapped capabilities object
        """
        # desired_capabilities = capabilities.copy()
        # desired_capabilities['platform'] = desired_capabilities['platform'].lower()
        base = {
            'capabilities': {
                'alwaysMatch': capabilities,
                'firstMatch': [{}]
            }
            # 'desiredCapabilities': desired_capabilities
        }
        return base

    def get(self, url):
        """
        Url to get

        Parameters
        ----------

            url (str): a valid url string to get
        """
        self._run_command(BrowserCommands.GET)

    def quit(self):
        """
        Closes the session, the windows, the driver and the browser
        """
        self._run_command(BrowserCommands.QUIT)
        self.new_service.stop()

    def wait_until(self, func, timeout, frequency=None):
        klass = Wait(self, timeout)
        return klass.start_polling(func)
    
