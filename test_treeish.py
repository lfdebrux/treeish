import pytest

import treeish


@pytest.mark.parametrize("othertype", (tuple, list))
def test_treepath_can_be_compared_with_any_treeishpath_type(othertype):
    assert treeish.treepath() == othertype()
    assert treeish.treepath("a") == othertype("a")


def test_walk_returns_empty_list_for_empty_trees():
    assert list(treeish.walk({})) == []
    assert list(treeish.walk([])) == []
    assert list(treeish.walk([{}])) == []
    assert list(treeish.walk([[]])) == []
