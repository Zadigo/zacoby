import os

# Absolute path to the current project

PROJECT_DIRECTORY = os.path.abspath(__file__)


# Sets of middlewares that execute every time
# an action is accomplished

MIDDLEWARES = [
    'zacoby.middlewares.History'
]


# Set the general timezone to the current
# project

USE_TZ = True

TIMEZONE = 'America/Chicago'
