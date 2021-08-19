class Container:
    def __init__(self, **kwargs):
        self._items = dict()
        self._items.update(kwargs)

    def __getattr__(self, item):
        return self._items.get(item)


