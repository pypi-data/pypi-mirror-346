from __future__ import annotations

from itertools import count
from typing import Any, ClassVar

from typing_extensions import Self

from ._grouping import Group, group
from ._scene import Scene
from ._annotations import NodeID


class NodeMixinSorter(type):
    """Node metaclass for initializing `Node` subclass after other `mixin` classes"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, object],
    ) -> type:
        def sorter(base: type) -> bool:
            # TODO?: Add extra point for being the exact type `Node`
            return isinstance(base, Node)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


@group(Group.NODE)
class Node(metaclass=NodeMixinSorter):
    _uid_counter: ClassVar[count[NodeID]] = count(0, 1)

    def __new__(cls, *_args: Any, **_kwargs: Any) -> Self:
        # NOTE: additional args and kwargs are ignored!
        instance = super().__new__(cls)
        instance.uid = next(Node._uid_counter)
        return instance

    uid: NodeID  # is set in `Node.__new__`
    parent: Node | None = None

    def __init__(self, parent: Node | None = None) -> None:
        if parent is not None:
            self.parent = parent

    def with_parent(self, parent: Node | None, /) -> Self:
        self.parent = parent
        return self

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(#{self.uid})"

    def update(self) -> None:
        """Called each frame"""

    def queue_free(self) -> None:
        if self not in Scene.current._queued_nodes:
            Scene.current._queued_nodes.append(self)

    def _free(self) -> None: ...  # overridden by using `@group`
