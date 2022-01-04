from importlib import import_module
from zacoby.utils.characters import LazyFormat


def import_from_module(dotted_path: str):
    """
    Imports a module, gets an object then
    tries to return it
    """
    try:
        path, klass = dotted_path.rsplit('.', maxsplit=1)
    except:
        raise ImportError(
            LazyFormat("Module at path {path} does not exist.", path=dotted_path)
        )

    module = import_module(path)

    try:
        return getattr(module, klass)
    except AttributeError:
        raise ImportError(LazyFormat("Could not find attribute '{klass}' "
        "in module {dotted_path}.", klass=klass, dotted_path=dotted_path))
