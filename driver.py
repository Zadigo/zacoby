import socket

from zacoby import exceptions
from zacoby.browsers.capabilities import CHROME
from zacoby.dom import commands
from zacoby.dom.mixins import LocationMixins
from zacoby.logger import create_default_logger
from zacoby.remote import RemoteConnection
from zacoby.service import Service
from zacoby.signals import signal
from zacoby.wait import Pause, Wait


class Base(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__
        capabilities = attrs.get('capabilities', None)
        if capabilities is None:
            attrs.update({'capabilities': CHROME})

        port = attrs.get('port', None)
        if port is None:
            attrs.update({'port': cls.set_port()})
        return new_class(cls, name, bases, attrs)

    @classmethod
    def set_port(cls):
        s = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        s.bind(('0.0.0.0', 0))
        s.listen(5)
        available_port = s.getsockname()[1]
        s.close()
        return available_port




class BaseSpider(metaclass=Base):
    capabilities  = None
    host = None
    port = None
    session_id = None

    def __init__(self, executable):
        self.logger = create_default_logger(
            self.__class__.__name__
        )
        # Creates a new session by opening the broweser
        service = Service(executable, self.host, self.port)
        # signal.connect(service, 'ServiceSignal', self)

        remote_server_address = f'http://localhost:{self.port}'
        # remote_server_address = 'https://jsonplaceholder.typicode.com/todos'
        service.start(host=remote_server_address)
        # signal.send('ServiceSignal', self, name='start')
        # Creates a new connection so that we can send commands
        # to the browser -; this is the main interface to use
        # for example when trying to get an http address etc.
        self.remote_connection = RemoteConnection(remote_server_address)
        # Connect all signals here
        signal.connect(self.remote_connection, 'RemoteSignal', self)
        signal.connect(service, 'ServiceSignal', self)
        self.logger.info('Signals connected...')

        self._new_session()

    def _build_capabilities(self):
        base = {
            'capabilities': {
                'alwaysMatch': self.capabilities,
                'firstMatch': [{}]
            }
        }
        return base

    def _new_session(self, browser_profile=None):
        capabilities = self._build_capabilities()
        # This sends the specific command to start a new
        # session. Note, this is the classic way to send
        # commands to the browser using the remote connection
        response = self.remote_connection._execute_command(
            commands.NEW_SESSION, **capabilities
        )
        
        response_value = response.get('value', None)
        # response_value = response.get('value', {'value': 'For Testing'})
        if response_value is not None:
            error = response_value.get('error', None)
            if error is not None:
                raise exceptions.SpiderEerror(
                    response_value['message']
                )
                
            # This is an important step for urls that
            # require a session ID!
            self.session_id = response_value.get('sessionId', response_value)
            signal.send('RemoteSignal', self)
            # Get the new capabilities that was returned
            # in the response which includes things like
            # timeouts etc.
            self.capabilities = response_value.get('capabilities', capabilities)

    def get(self, url):
        self.remote_connection._execute_command(
            commands.GET, session=self.session_id, url=url
        )

    def quit(self, callback=None):
        self.remote_connection._execute_command(
            commands.QUIT, session=self.session_id
        )
        self.logger.info('Scrapper was terminated')
        if callback is not None:
            if callable(callback):
                return callback(self.remote_connection)


class Zacoby(BaseSpider, LocationMixins):
    """
    This is a the base entrypoint for creating a Zacoby
    web scrapper. To create a new scrapper, simply do:

            driver = Zacoby('path/to/driver.exe')
            driver.get('http://example.com')

    From a general standpoint, you would not be using this
    class directly. You would use the browsers provided
    in `zacoby.browsers`
    """
    def wait(self, name, timeout=10):
        instance = Wait(name, self, timeout=timeout)
        return instance

    def pause(self, callback=None, timeout=10):
        instance = Pause(self, timeout=timeout)
        return instance
