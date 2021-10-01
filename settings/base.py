import os

DEBUG = True

# The current directory to the project

PROJECT_DIRECTORY = None


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
