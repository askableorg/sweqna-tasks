"""Key/value store with a monotonic generation counter.

The generation counter exists so that a response which was already in flight
when an invalidation happened cannot be written back into the store. Callers
capture the generation before they start work and hand it back on insert.
"""


class Store:
    def __init__(self):
        self._entries = {}
        self._generation = 0
        self.rejected_inserts = 0

    @property
    def generation(self):
        """The current generation. Bumped by every invalidation."""
        return self._generation

    def get(self, key):
        return self._entries.get(key)

    def insert(self, key, value, generation):
        """Insert value under key, unless the store has moved on.

        `generation` is the value of `self.generation` observed by the caller
        when it began the work that produced `value`.
        """
        if generation != self._generation:
            self.rejected_inserts += 1
            return False
        self._entries[key] = value
        return True

    def invalidate(self, prefix):
        """Drop every entry whose key starts with `prefix`."""
        doomed = [key for key in self._entries if key.startswith(prefix)]
        for key in doomed:
            del self._entries[key]
        self._generation += 1
        return len(doomed)

    def keys(self):
        return sorted(self._entries)
