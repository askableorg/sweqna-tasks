"""Deterministic cooperative scheduler for the fetch generators.

No threads, no sleeps, no timing dependence: the test says exactly when each
suspended fetch resumes.
"""


class Scheduler:
    def __init__(self):
        self._pending = {}

    def start(self, name, generator):
        """Run `generator` up to its first suspension point."""
        try:
            next(generator)
        except StopIteration as finished:
            return finished.value
        self._pending[name] = generator
        return None

    def resume(self, name):
        """Run the named generator to completion."""
        generator = self._pending.pop(name)
        try:
            next(generator)
        except StopIteration as finished:
            return finished.value
        raise RuntimeError(f"{name} suspended more than once")
