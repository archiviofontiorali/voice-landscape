class FrequencyDict:
    def __init__(self, addresses=None):
        self._addresses = addresses if addresses is not None else []
        self._data = None
        self.init_addresses(self._addresses)

    def init_addresses(self, addresses: list):
        self._addresses = addresses
        self._data = {key: dict(afor=1) for key in self._addresses}

    @property
    def addresses(self) -> list:
        return self._addresses

    def fetch_address(self, address) -> dict:
        return self._data[address]

    def increment(self, address, key):
        try:
            self._data[address][key] += 1
        except KeyError:
            self._data[address][key] = 1
