from importlib import import_module


def load_module(python_path: str):
    try:
        module = import_module(python_path)
    except ModuleNotFoundError:
        raise

    return module
