"""Custom wrapper for function with a string representation."""


class DefaultOperator:
    """Default operator is a wrapper to a mathematical function with a string form."""

    def __init__(self, function, function_representation):
        """Constructor of default operator."""
        self.function = function
        self.function_representation = function_representation

    def __call__(self, *args):
        """Call default operator."""
        return self.function(*args)

    def __str__(self):
        """String form of default operator."""
        return self.function_representation
