import json
import socket

from zacoby.browsers.capabilities import CHROME
from zacoby.driver.remote import RemoteConnection
from zacoby.driver.wait import Wait
from zacoby.exceptions import errors
from zacoby.logging.logger import default_logger
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

        default_logger(self.__class__.__name__).info('Remote connection created')

        self.start_session(self.capabilities, None)

    def __repr__(self):
        return f'< {self.__class__.__name__} ([{self.session_id}]) >'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def start_session(self, capabilities, browser_profile=None):
        """
        Start a new browser session using the
        provided capabilities

        Parameters
        ----------

            - capabilities (dict): [description]

            - browser_profile (str): [description]
        """
        extended_capabilities = self._fit_transform_capabilities(capabilities)
        default_logger(None).info(f"New session started at {self.new_remote_connection.remote_server_address} for {capabilities['browserName']}")
        # print('New session was started using:', extended_capabilities)

        response = self.new_remote_connection._execute_command(
            BrowserCommands.NEW_SESSION, capabilities=extended_capabilities
        )

        response_value = response.get('value', None)
        self.session = response_value.get('sessionId', response_value)
        # Get the new capabilities that was returned
        # in the response which includes things like
        # timeouts etc.
        self.capabilities = response_value.get('capabilities', extended_capabilities)

    def _fit_transform_capabilities(self, capabilities:dict, **kwargs):
        """In order to match the W3C capabilities, we have wrap it's values
        into something acceptable

        Parameters
        ----------

            capabilities (dict): a dictionnary of capabilities

        Returns:
            dict: a wrapped capabilities object
        """
        base = {
            'capabilities': {
                'alwaysMatch': capabilities,
                'firstMatch': [{}]
            }
        }
        return base

    def get(self, url):
        """
        Url to get

        Parameters
        ----------

            url (str): a valid url string to get
        """
        self.new_remote_connection._execute_command(
            BrowserCommands.GET, 
            session=self.session, 
            url_to_get=url
        )

    def quit(self):
        """
        Closes the session, the windows, the driver and the browser
        """
        self.new_remote_connection._execute_command(
            BrowserCommands.QUIT, session=self.session
        )
        self.new_service.stop()

    def wait_until(self, func, timeout, frequency=None):
        klass = Wait(self, timeout)
        return klass.start_polling(func)
    
    def validation(self, *validators, all_of=True):
        results = []
        for validator in validators:
            results.append(validator())
        if all_of:
            return all(results)
        return any(results)

        
