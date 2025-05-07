from __future__ import annotations
from typing import Optional
from abc import abstractmethod, ABC

# -------------------------------------------


class TreeNode(ABC):
    def get_subnodes(self, *args, **kwargs) -> list[TreeNode]:
        _, __ = args, kwargs
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current.get_parent():
            ancestors.append(current.get_parent())
            current = current.get_parent()
        return ancestors

    def get_root(self) -> TreeNode:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_child_nodes(self, *args, **kwargs) -> list[TreeNode]:
        pass

    @abstractmethod
    def get_parent(self) -> Optional[TreeNode]:
        pass

    def __str__(self):
        return self.get_name()