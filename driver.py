import socket
from typing import Callable

from wait import Pause
from zacoby import exceptions, global_logger
from zacoby.browsers.capabilities import CHROME
from zacoby.page import browser_commands
from zacoby.page.navigation import Location
from zacoby.remote import RemoteConnection
from zacoby.service import Service
from zacoby.settings import lazy_settings
# from zacoby.signals import signal
from zacoby.wait import Wait


class Base(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__
        if bases:
            capabilities = attrs.get('capabilities', None)
            if capabilities is None:
                # attrs.update({'capabilities': CHROME})
                attrs.update({'capabilities': lazy_settings.CAPABILITIES.get('CHROME')})
        return new_class(cls, name, bases, attrs)


class BaseSpider(metaclass=Base):
    capabilities  = None
    host = None
    port = None

    SESSION_ID = None

    manager = None

    def __init__(self, executable_or_dir: str, **kwargs):
        self._set_port()

        remote_server_address = f'http://localhost:{self.port}'
        service = Service(executable_or_dir, self.host, self.port, filename=None)
        service.start(host=remote_server_address, debug_mode=lazy_settings.DEBUG)

        # Creates a new connection so that we can send commands
        # to the browser -; this is the main interface to use
        # for example when trying to get an http address etc.
        self.remote_connection = RemoteConnection(remote_server_address)

        if lazy_settings.DEBUG:
            self.remote_connection.SESSION_ID = self.SESSION_ID = 'TEST-SESSION'
            self.manager = Location(remote_connection=self.remote_connection)
        else:
            self._new_session()            
            self.manager = Location(remote_connection=self.remote_connection)

        # signal.send(sender=self, remote_connection=self.remote_connection)

        # self.listeners = None

    def _set_port(self):
        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        s.bind(('0.0.0.0', 0))
        s.listen(5)
        self.port = s.getsockname()[1]
        s.close()

    def _build_capabilities(self):
        return {
            'capabilities': {
                'alwaysMatch': self.capabilities,
                'firstMatch': [{}]
            }
        }

    # def register_events(self, *funcs: Callable):
    #     """
    #     Register an event listener on the driver

    #     Event listeners are pieces of codes that will execute 
    #     before or after certain specific driver events

    #     Example
    #     -------

    #             from zacoby.events.listeners import before_navigate_to

    #             @before_navigate_to
    #             def my_custom_listener(sender, signal, instance):
    #                 print("An event was fired")

    #             driver = Zacoby("executable")
    #             driver.register_events(my_custom_listener)
    #             driver.get("http://example.com")

    #         You can also use this code for the same effect:

    #             driver.register(before_navigate_to(my_custom_listener))

    #     Returns
    #     -------

    #         bool: whether the listeners were correctly mapped
    #     """
    #     base = None
    #     events = list(funcs)
    #     if events:
    #         for event in events:
    #             base, signal_name = event()
    #         self.listeners = base
    #     signal.connect(self.listeners, 'ListenerSignal', self)
    #     return True if self.listeners is not None else False

    def _new_session(self, browser_profile=None):
        global_logger.info(f"Starting new session...")
        capabilities = self._build_capabilities()
        # This sends the specific command to start a new
        # session. Note, this is the classic way to send
        # commands to the browser using the remote connection
        # response = self.remote_connection._execute_command(
        #     browser_commands.NEW_SESSION, 
        #     **capabilities
        # )
        command = browser_commands.get_command('new_session')
        response = self.remote_connection._execute_command(command, **capabilities)
        
        response_value = response.get('value', None)
        if response_value is not None:
            error = response_value.get('error', None)
            if error is not None:
                raise exceptions.SpiderError(response_value['message'])
                
            # This is an important step for urls that
            # require a session ID!
            self.SESSION_ID = response_value.get('sessionId', response_value)
            self.remote_connection.SESSION_ID = self.SESSION_ID

            # Store some generic but global elements
            # in the settings for easy access in the
            # rest of the application
            lazy_settings['session'] = {
                'id': self.SESSION_ID,
                'driver': self,
                'remote': self.remote_connection
            }

            # signal.send('RemoteSignal', self)

            # Get the new capabilities that was returned
            # in the response which includes things like
            # timeouts etc.
            self.capabilities = response_value.get('capabilities', capabilities)

    def get(self, url:str):
        """
        Navigate to an url

        Parameters
        ----------

            url (str): an url to navigate to
        """
        command = browser_commands.get_command('get')
        self.remote_connection._execute_command(command, requires_session_id=True, url=url)

    def conditional_get(self, url: str, default: str=None):
        """Navigate to an url and if it fails try a default"""
        command = browser_commands.get_all_commands('get')
        command_execution = self.remote_connection._execute_command

        attrs = {
            'command': command,
            'requires_session_id': True
        }
        try:
            command_execution(**attrs, url=url)
        except:
            command_execution(**attrs, url=default)

    def quit(self, callback: Callable=None):
        command = browser_commands.get_command('quit')
        self.remote_connection._execute_command(command, requires_session_id=True)
        if callback is not None:
            if not callable(callback):
                raise TypeError('Callback should be a callable function')
            return callback(self.remote_connection)


class Zacoby(BaseSpider):
    """
    This is a the base entrypoint for creating a Zacoby
    web scrapper. To create a new scrapper, simply do:

            driver = Zacoby('path/to/driver.exe')
            driver.get('http://example.com')

    From a general standpoint, you would not be using this
    class directly. You would use the browsers provided
    in `zacoby.browsers`
    """

    @property
    def current_url(self):
        """
        The current page URL
        """
        pass

    @property
    def window_handles(self):
        pass

    def wait(self, name, timeout = 10):
        """
        Wait for an element on the web page to have a certain state

        Parameters
        ----------

            name (str): the element's name
            timeout (int, optional): waiting time. Defaults to 10.
        """
        instance = Wait(name, self, timeout=timeout)
        return instance

    def run_sequence(self, sequence: Callable):
        sequence.driver = self
        sequence.build_sequences()
        sequence.resolve()

    def pause(self, callback: Callable[[RemoteConnection], RemoteConnection] = None, timeout: int = 10):
        """
        Pause the execution of the driver for a specific
        period of time

        Parameters
        ----------

            callback (callable, optional): a function to call after the pause. Defaults to None.
            timeout (int, optional): pause duration in seconds. Defaults to 10.

        """
        instance = Pause(self, timeout=timeout)
        instance._start_pause(callback=callback)
        return instance
    
