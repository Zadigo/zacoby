from collections import defaultdict
from collections.abc import Mapping
from typing import OrderedDict
from zacoby.settings import lazy_settings as settings
import datetime
import pytz

class History(Mapping):
    def __init__(self):
        timezone = pytz.timezone(settings.TIMEZONE)
        self.current_date = datetime.datetime.now(tz=timezone)
        self.containers = defaultdict(list)

    def __call__(self, sender, **kwargs):
        self.add(**kwargs)

    def __getitem__(self, key):
        return self.containers[key]

    def __iter__(self):
        return iter(self.containers)

    def __len__(self):
        return len(self.containers)

    def add(self, name, value):
        container = self.containers[name]
        container.append((self.current_date.timestamp(), name, value))
