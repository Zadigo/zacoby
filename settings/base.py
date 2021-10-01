import os

DEBUG = True

# The current directory to the project

PROJECT_DIRECTORY = None


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

USE_TZ = True

TIMEZONE = 'America/Chicago'
