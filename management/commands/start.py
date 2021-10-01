from zacoby.management.base import ProjectCommand

class Command(ProjectCommand):
    def create_parser(self):
        parser = super().create_parser()
        parser.add_argument('start', help='Run all the spiders within a project')

    def call_command(self, parser):
        pass
