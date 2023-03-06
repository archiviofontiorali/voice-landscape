class Container(dict):
    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(f"'Container' object has no attribute '{item}'")


class FrequencyDict(dict):
    def __init__(self, keys: list = None):
        super().__init__()

        if keys:
            for key in keys:
                self.setdefault(key, 0)

    def increment(self, key):
        try:
            self[key] += 1
        except KeyError:
            self[key] = 1
