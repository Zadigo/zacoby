import importlib
from collections import OrderedDict

from pydispatch import dispatcher
from zacoby.utils.functionnal import LazyObject
# from zacoby.signals import signal


class Settings:
    """ 
    Represents the settings file for the project
    """
    _settings = OrderedDict()

    def __init__(self):
        settings = importlib.import_module('zacoby.settings.base')
        modules_dict = settings.__dict__

        for key, value in modules_dict.items():
            if key.isupper():
                self._settings.setdefault(key, value)
                # Also allow something like
                # settings.MY_SETTING when using
                # the Settings instance
                self.__dict__[key] = value

    def __call__(self, **kwargs):
        self.__init__()
        self._settings.update(kwargs)
        # Alert all middlewares and registered
        # signals on Any that the settings
        # have changed
        # signal.send(dispatcher.Any, self)
        return self._settings

    def __str__(self):
        return str(self._settings)

    def __getitem__(self, key):
        return self._settings[key]

    def __setitem__(self, key, value):
        self.__dict__[key.upper()] = value

    def __iter__(self):
        return iter(self._settings)

    def copy(self):
        return self._settings.copy()

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def has_setting(self, key):
        return key in self._settings.keys()


settings = Settings()


class LazySettings(LazyObject):
    def _init(self):
        self.cached_object = settings


lazy_settings = LazySettings()
