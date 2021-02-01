"""."""

import pytest

from operators.leaf import Leaf
from operators.add import Add
from operators.mul import Mul


@pytest.mark.timeout(1.0)
def test_set_leaf_apply_yields_set_when_given_a_set():
    """."""
    assert Leaf({6}).apply() == {6}


@pytest.mark.timeout(1.0)
def test231():
    """."""
    assert Mul(Leaf(2), Leaf({1, 3})).apply() == {frozenset({2, 1}), frozenset({2, 3})}


@pytest.mark.timeout(1.0)
def test_set_add_adds_when_given_leaves_with_sets():
    """."""
    assert Add(Leaf({5}), Leaf({6})).apply() == {5, 6}


@pytest.mark.timeout(1.0)
def test_set_multiply_multiplies_when_given_leaves_with_sets__second_single_element():
    """."""
    assert Mul(Leaf({5, 6}), Leaf({3})).apply() == {frozenset({5, 3}), frozenset({6, 3})}


@pytest.mark.timeout(1.0)
def test_set_multiply_multiplies_when_given_leaves_with_sets__second_multiple_elements():
    """."""
    assert Mul(Leaf({5, 6}), Leaf({3, 4})).apply() == {frozenset({5, 3}), frozenset({6, 3}), frozenset({5, 4}),
                                                       frozenset({6, 4})}
