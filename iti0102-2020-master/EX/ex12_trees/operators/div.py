"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Div(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """default constructor."""
        super().__init__((left, right))

    @property
    def priority(self):
        """priority of the operation."""
        return 3

    @property
    def default_operator(self):
        """Make use of the 'operator' library or use a lambda function."""
        return DefaultOperator(lambda x, y: x / y, "/")

    @property
    def actions(self):
        """:return a dictionary of custom operations."""
        return {
            (set, set): lambda x, y: frozenset(x - y),  # set exclusion
            (set, int): lambda x, y: {a for a in x if a != y},  # remove from set
            (int, int): lambda x, y: int(x / y)  # integer division
        }
