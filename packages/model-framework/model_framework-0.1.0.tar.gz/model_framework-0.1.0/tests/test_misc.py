#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test various building blocks
"""

import pytest

import mframework._mframework as mf
import mframework._utils as mfu
from mframework import log as log
log.on


def test_log():
    log.off
    log.on


def test_is_primitive_type():
    assert mf.is_primitve_type(bool)
    assert mf.is_primitve_type(int)

    class MyType:
        pass

    assert not mf.is_primitve_type(MyType)


def test_check_type():
    assert mf.check_type('x', 11, int) is None
    assert mf.check_type('y', 11.2, float) is None
    assert mf.check_type('z', 'abc', str) is None

    with pytest.raises(TypeError):
        mf.check_type('x', 55.5, int)


def test_DictLike():
    d = mfu.DictLike()
    d['x'] = 2
    d['y'] = 3
    d['z'] = 77

    assert str(d) == "{'x': 2, 'y': 3, 'z': 77}"
    assert repr(d) == "DictLike({'x': 2, 'y': 3, 'z': 77})"

    assert len(d) == 3

    assert d['x'] == 2
    assert d.pop('x')
    with pytest.raises(KeyError):
        print(d['x'])


def test_SpecDict():
    d = mf.SpecDict()
    d['spec1'] = mf.SpecEntry(int)
    d['spec2'] = mf.SpecEntry(bool)

    # Cannot redefine a specification
    with pytest.raises(KeyError):
        d['spec2'] = mf.SpecEntry(str)

    # Value must be SpecEntry
    with pytest.raises(ValueError):
        d['spec3'] = 3

    assert d['spec1'].schema == int
    assert d['spec2'].schema == bool


def test_ItemDict():
    d = mf.ItemDict()
    assert d['x'] == {}

    d['y'] = 1
    d['y'] = 2
    d['y'] = 3
    assert len(d['y']) == 3
    assert list(d['y'].values()) == [1, 2, 3]

    # Test assigning UIDs
    d.assign_uid('y', 'special_entry')
    assert 3 == d.get_by_uid('y', 'special_entry')

    d.assign_uid('y', 'another_special_entry', 1)
    assert 2 == d.get_by_uid('y', 'another_special_entry')

    # ----- Test -----
    d = mf.ItemDict()
    d['a'] = 'one'
    d['a'] = 'two'
    d['a'] = 'three'

    assert d['a'] == {0: 'one', 1: 'two', 2: 'three'}

    d.assign_uid('a', 'myUID', 1)
    # Cannot assign same UID twice
    with pytest.raises(KeyError):
        d.assign_uid('a', 'myUID', 1)
    assert d.get_by_uid('a', 'myUID') == 'two'
    d.assign_uid('a', 'myUID2')

    exp_uids = ('myUID', 'myUID2')
    exp_values = ('two', 'three')
    for i, (uid, value) in enumerate(d.iter_uids('a')):
        assert exp_uids[i] == uid
        assert exp_values[i] == value


def test_SpecEntry():
    s = mf.SpecEntry(schema=int, required=0, max_items=1, doc='abc')
    assert s.schema is int
    assert s.max_items == 1
    assert s.singleton is True
    assert s.required == 0
    assert s.doc == 'abc'

    with pytest.raises(TypeError):
        s.max_items = 'FALSE'

    with pytest.raises(TypeError):
        s.doc = 123
