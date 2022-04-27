from zacoby.conditions import element_visibility
from zacoby.page import browser_commands
from zacoby.page.navigation import Location
from zacoby.remote import RemoteConnection
from zacoby.service import Service
from zacoby.wait import Wait


class SpiderOptions:
    capabilities = {
        'chrome': {
            'browserName': 'chrome',
            'browserVersion': 'latest',
            'platformName': 'windows'
        },
        'edge': {
            'browserName': 'MicrosoftEdge',
            'browserVersion': 'latest',
            'platformName': 'windows'
        }
    }
    
    def __init__(self):
        self.spider = None
        self.name = None
        self.capability = 'chrome'
        self.default_capability = None
        self.host = None
        self.port = None
        
    def __repr__(self):
        return f"<{self.__class__.__name__} for {self.name}>"
    
    def add_meta_attribute(self, name, value):
        if name == 'capabilities':
            if value is None:
                value = self.capabilities
        setattr(self, name, value)
    
    def update_class(self, name, cls):
        self.spider = cls
        self.name = name

    def set_port(self):
        self.port = 0
        
    def build_capabilities(self):
        self.default_capability = self.capabilities[self.capability]
        return {
            'capabilities': {
                'alwaysMatch': self.default_capability,
                'firstMatch': [{}]
            }
        }
    
    def prepare(self):
        self.build_capabilities()
        self.set_port()
        remote_server_address = f'http://localhost:{self.port}'


class BaseSpider(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        
        # parents = [base for base in bases if not isinstance(base, Spider)]
        # if not parents:
        #     return super_new(cls, name, bases, attrs)
        
        meta = SpiderOptions()
        
        new_class = super_new(cls, name, bases, attrs)
        meta.update_class(name, new_class)
        setattr(new_class, 'meta', meta)
        cls.prepare(new_class)
        return new_class
        
    @classmethod
    def prepare(cls, new_class):
        new_class.meta.prepare()

        # Load all the commands to
        # be used for the browser
    
class Spider(metaclass=BaseSpider):
    SESSION_ID = None
    _browser_commands = browser_commands
    
    def __init__(self, executable_or_dir, **kwargs):
        service = Service(executable_or_dir, self)
        service.start()
        
        self.remote_connection = RemoteConnection(self)
        
        self.new_session()
        
        manager = Location()
        manager.update_class(self)
        self.manager = manager
        
    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.remote_connection}]>"
    
    def new_session(self, browser_profile=None):
        command = self._browser_commands.get_command('new_session')
        response = self.remote_connection.execute_command(command)
        print(response)
        response_value = response.get('value', None)
        if response_value is not None:
            pass
        if response_value is not None:
            self.SESSION_ID = response_value.get('sessionId', None)
            self.meta.add_meta_attribute(self, 'capabilities', response_value.get('capabilities', None))
        
    def get(self, url):
        pass
    
    def conditional_get(self, url, default=None):
        pass
    
    def wait(self, name, timeout=10):
        return Wait(name, self, timeout=timeout)
    
    def quit(self, callback=None):
        pass


spider = Spider('')
spider.get('http://example.com')
element = spider.manager.get_element_by_id('some_id')
element.is_visible
wait_instance = spider.wait('div')
wait_instance.until(element_visibility, selector='id')
spider.quit()
