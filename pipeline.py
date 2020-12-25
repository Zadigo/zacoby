class Pipeline:
    _resolutions = []

    def __init__(self, *funcs):
        self._funcs = list(funcs)

    @property
    def resolved_to_true(self):
        return all(self._resolutions)

    def resolve(self, driver, name):
        for func in self._funcs:
            self._resolutions.append(
                func(driver, name)
            )
        return self._resolutions
