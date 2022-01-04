from zacoby.management.base import ProjectCommand
from zacoby.service import get_default_service_class
from zacoby.settings import lazy_settings


class Command(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('--name', help='Run a specific spider within a project', type=str)

    def execute(self, namespace):
        # x. Start the default Service module
        # which will be executing the .exe file
        service = get_default_service_class()
        
        host = lazy_settings.SERVICE['settings']['host']
        port = lazy_settings.SERVICE['settings']['port']
        
        service_instance = service('', host, port)
        
        lazy_settings['service_instance'] = service_instance
        service_instance.start()

        # x. Load the project's spider file. This should
        # execute the whole sequence
        
        