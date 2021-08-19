class Container:
    def __init__(self, **kwargs):
        self._items = dict()
        self._items.update(kwargs)

    def __getattr__(self, item):
        return self._items.get(item)


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
