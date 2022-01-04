from argparse import ArgumentParser, Namespace
from typing import Any


class BaseCommand:
    requires_checks = False
    description = ''

    def create_parser(self):
        parser = ArgumentParser(description=self.description)
        parser.add_argument('command', help='Command to run', type=str)
        self.add_arguments(parser)
        return parser
    
    def add_arguments(self, parser: ArgumentParser):
        """
        Adds additional arguments in addition with
        the ones that were already implemented above. Each
        subclass can implement additional arguments
        """
        pass

    def execute(self, namespace: Namespace=None) -> Any:
        """
        Represents the main logic behind an argument passed
        using the command line. Each Command should override
        this definition to implement their custom logic so that
        when this is called, the logic is run
        """
        pass


class ProjectCommand(BaseCommand):
    requires_checks = True
