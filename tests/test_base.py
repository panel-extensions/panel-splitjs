import pytest

from panel.layout import Spacer
from panel_splitjs import HSplit, Split, VSplit


def test_split_objects():
    split = Split('A', 'B')

    assert len(split.objects) == 2
    s1, s2 = split
    assert s1.object == 'A'
    assert s2.object == 'B'

    root = split.get_root()
    assert len(root.data.objects) == 2

def test_split_objects_too_many():
    with pytest.raises(ValueError, match='Split component must have at most two children.'):
        Split('A', 'B', 'C')

def test_split_objects_one():
    split = Split('A')

    assert len(split.objects) == 1
    s1 = split[0]
    assert s1.object == 'A'

    root = split.get_root()
    assert len(root.data.objects) == 1

def test_split_objects_none():
    split = Split()
    assert split.objects == []

    root = split.get_root()
    assert root.data.objects == []
