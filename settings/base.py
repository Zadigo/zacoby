import os

DEBUG = True

# The current directory to the project

PROJECT_DIRECTORY = None


GLOBAL_ZACOBY_PATH = os.path.dirname(os.path.dirname(__file__))


# Main dependencies that need to be
# loaded on project startup

SERVICE = {
    'default': 'zacoby.service.Service',
    'settings': {
        'host': '127.0.0.1',
        'port': 0,
        'server_address': 'http://localhost'
    }
}


# Sets of middlewares that execute every time
# an action is accomplished

MIDDLEWARES = [
    'zacoby.middlewares.History'
]

# List of browser capabilities to use with
# the project

CAPABILITIES = {
    'CHROME': {
        'browserName': 'chrome',
        'browserVersion': 'latest',
        'platformName': 'windows'
    },
    'EDGE': {
        'browserName': 'MicrosoftEdge',
        'browserVersion': 'latest',
        'platformName': 'windows'
    }
}


# Set the general timezone to the current
# project

USE_TZ = True

TIMEZONE = 'America/Chicago'
