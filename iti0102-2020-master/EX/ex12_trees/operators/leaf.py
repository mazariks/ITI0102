"""."""

from default_operator import DefaultOperator
from tree_node import TreeNode


class Leaf(TreeNode):
    """Leaf node."""

    def __init__(self, value):
        """default constructor."""
        super().__init__(value)
        self.__value = value

    @property
    def priority(self):
        """:return the value of the operation."""
        return 1

    @property
    def associativity(self):
        """Nothing fancy here."""
        return False if self.default_operator.__str__() == "-" or self.default_operator.__str__() == "/" or \
                        self.default_operator.__str__() == "**" else True

    @property
    def default_operator(self):
        """Nothing fancy here."""
        return DefaultOperator(lambda x: x, "")

    def apply(self):
        """:return the value."""
        return self.__value

    def __str__(self):
        """String form of leaf value."""
        return str(self.__value)

    def class_str(self):
        """:return class string representation of the object."""
        return f"Leaf({str(self.__value)})"
