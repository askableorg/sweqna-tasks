"""Read-through fetcher.

A fetch is a generator so that tests can drive the interleaving explicitly
rather than depending on thread timing. Yielding marks the suspension point
where the slow origin call would block.
"""


class Fetcher:
    def __init__(self, store, origin):
        self.store = store
        self.origin = origin

    def fetch(self, key):
        cached = self.store.get(key)
        if cached is not None:
            return cached

        observed_generation = self.store.generation
        yield  # the origin call blocks here
        value = self.origin(key)
        self.store.insert(key, value, observed_generation)
        return value
