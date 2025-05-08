from __future__ import annotations

from ._scene import Scene


class EngineMixinSorter(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, object],
    ) -> type:
        def sorter(base: type) -> bool:
            # TODO?: Add extra point for being the exact type `Engine`
            return isinstance(base, Engine)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Engine(metaclass=EngineMixinSorter):
    # using setter and getter to prevent subclass def overriding
    _is_running: bool = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, run_state: bool) -> None:
        self._is_running = run_state

    def process(self) -> None:
        self.update()
        Scene.current.process()

    def update(self) -> None:
        """Called each frame"""

    def run(self) -> None:  # main loop function
        self.is_running = True
        while self.is_running:  # main loop
            self.process()
