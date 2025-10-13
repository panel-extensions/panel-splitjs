import pytest

from panel.layout import Spacer
from panel_splitjs import HSplit, Split, VSplit


def test_split_objects_length():
    split = Split('A', 'B')

    assert len(split.objects) == 2
    s1, s2 = split
    assert s1.object == 'A'
    assert s2.object == 'B'


def test_split_objects_too_many():
    with pytest.raises(ValueError, match='Split component must have at most two children.'):
        Split('A', 'B', 'C')


def test_split_objects_one():
    split = Split('A', None)

    assert len(split.objects) == 2
    s1, s2 = split
    assert s1.object == 'A'
    assert isinstance(s2, Spacer)


def test_split_objects_none():
    split = Split()

    assert len(split.objects) == 2
    s1, s2 = split
    assert isinstance(s1, Spacer)
    assert isinstance(s2, Spacer)
