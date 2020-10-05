
class Enum:
    enumerations = {}

    def __setattr__(self, name, value):
        if not isinstance(value, list):
            raise TypeError(f'The value you provided for {name} should be a list. Got {type(value)}')
        super().__setattr__(name, value)

    @classmethod
    def _construct(cls):
        """
        Build a dictionnary from a class' attributes
        written in uppercase

            class MyClass(Enum):
                KENDALL = (a, (b, c))

        Will construct a dictionnary of enumerations
        where {a: (a, (b, c)} with `MyClass.enumerations` 

        Returns
        -------

            type: return a non instantiated version
            of the class
        """
        klass_dict = cls.__dict__
        for key, value in klass_dict.items():
            if not key.startswith('__') and key.isupper():
                cls.enumerations.setdefault(value[0], value[1])
        return cls

    @classmethod
    def get(self, name, index: int=None):
        try:
            full_value = self.enumerations[name]
        except KeyError:
            raise
        else:
            if index is None:
                return full_value
            else:
                try:
                    return full_value[index]
                except IndexError:
                    raise

    @property
    def keys(self):
        return list(self.enumerations.keys())
