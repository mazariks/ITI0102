"""."""

import pytest

from operators.leaf import Leaf
from operators.add import Add


@pytest.mark.timeout(1.0)
def test_leaf_equals_leaf_when_same_value():
    """."""
    assert Leaf(1) == Leaf(1)


@pytest.mark.timeout(1.0)
def test_leaf_doesnt_equal_leaf_when_different_value():
    """."""
    assert Leaf(1) != Leaf(2)


@pytest.mark.timeout(1.0)
def test_addition_equals_addition_when_same_value():
    """."""
    assert Add(Leaf(1), Leaf(2)) == Add(Leaf(1), Leaf(2))


@pytest.mark.timeout(1.0)
def test_addition_doesnt_equal_addition_when_different_value():
    """."""
    assert Add(Leaf(2), Leaf(1)) != Add(Leaf(1), Leaf(2))
