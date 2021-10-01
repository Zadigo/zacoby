import os

DEBUG = True

# The current directory to the project

PROJECT_DIRECTORY = None

# The spiders to run within the project.
# All registered spiders will be exectued.

SPIDERS = []


# List of browser capabilities

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

