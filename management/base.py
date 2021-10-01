from argparse import ArgumentParser

class BaseCommand:
    requires_checks = False
    description = ''

    def create_parser(self):
        parser = ArgumentParser(description=self.description)
        return parser

    def call_command(self, parser):
        pass

class ProjectCommand(BaseCommand):
    requires_checks = True
