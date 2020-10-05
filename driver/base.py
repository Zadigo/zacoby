import socket

from zacoby.browsers.capabilities import CHROME
from zacoby.dom.mixins import DomElementMixins
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
        return new_class
        

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
    def __init__(self, executable, host=None, port=None):
        self.host = host
        self.port = port
        self.session_id = None

        BrowserCommands._construct()

        new_service = Service(executable, self.host, self.port)
        new_service.start()
        self.new_service = new_service

        remote_server_address = f'http://localhost:{self.port}'
        self.new_remote_connection = RemoteConnection.as_class(remote_server_address)

        self.start_session(self.capabilities, None)

    def __repr__(self):
        return f'< {self.__class__.__name__} ([{self.session_id}]) >'

    def __setattr__(self, name, value):
        if name == 'port':
            if value is None or value == 0:
                # If no port was provided,
                # we have to try and find
                # an open port
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('0.0.0.0', 0))
                s.listen(5)
                port = s.getsockname()[1]
                s.close()
                value = port
        super().__setattr__(name, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def _run_command(self, command, **kwargs):
        response = self.new_remote_connection._run_command(command, **kwargs)
        if response:
            return response
        return dict(success=0, value=None, sesssion_id=None)

    def start_session(self, capabilities, browser_profile):
        """
        Start a new browser session using the
        provided capabilities

        Parameters
        ----------

            - capabilities (dict): [description]

            - browser_profile (str): [description]
        """
        print('New session was started using:', capabilities, browser_profile)
        if browser_profile:
            pass

        parameters = {
            'capabilities': capabilities
            # 'desiredCapabilities': capabilities
        }

        response = self._run_command(BrowserCommands.NEW_SESSION, kwargs=parameters)
        if 'sessionId' not in response:
            pass

        self.session = response['sessionId']
        self.capabilities = response.get('value')

        if self.capabilities is None:
            self.capabilities = response.get('capabilities')

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

    
class WebDriver(DomElementMixins, BaseDriver):
    """
    Classes should extend this clas to implement
    additional functionnalities

    Parameters
    ----------

        - executable (str): path to the driver executable

        - host (str, optional): . Defaults to None

        - port (int, optional): . Defaults to None
    """
    capabilities = None

    def __setattr__(self, name, value):
        if name == 'capabilities':
            if not isinstance(value, dict):
                raise errors.CapabilitiesTypeError(
                    'The browser capabilites should be a dictionnary'
                )

            if value is None:
                value = CHROME
        super().__setattr__(name, value)

    def wait_until(self, func, timeout, frequency=None):
        klass = Wait(self, timeout)
        return klass.start_polling(func)
