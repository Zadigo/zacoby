from string import Template

def subsitute_keys(path: str, values: dict):
    """
    Substitute keys in a given path by their
    respective values
    """
    try:
        return Template(path).substitute(**values)
    except:
        return path
