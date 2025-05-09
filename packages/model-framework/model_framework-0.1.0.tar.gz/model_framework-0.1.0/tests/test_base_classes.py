#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test base classes

from math import inf

import pytest

from mframework._mframework import _BaseSpec, _UserSpaceBase
from mframework import log
log.on


def test_BaseSpec():
    """
    Test base class '_BaseSpec'
    """

    class Spec(_BaseSpec):
        pass

    spec = Spec()
    spec._add_item_spec('a', int, max_items=42, doc='3987**12 + 4365**12 = 4472**12')
    spec._add_item_spec('b', int, doc=':(){ :|:& };:')

    with pytest.raises(KeyError):
        spec._add_item_spec('a', int)
    with pytest.raises(TypeError):
        spec._add_item_spec(0, int)
    with pytest.raises(ValueError):
        spec._add_item_spec('c', int, required=-2)
    with pytest.raises(ValueError):
        spec._add_item_spec('d', int, max_items=-1)
    with pytest.raises(TypeError):
        spec._add_item_spec('e', int, doc=1)
    with pytest.raises(TypeError):
        spec._add_item_spec('f', int, uid_required='OK')

    assert repr(spec) == "<Specification for ('a', 'b')>"
    assert spec.keys == ['a', 'b']

    docs = spec.get_docs()
    assert docs == {
        'a': {
            'main': '3987**12 + 4365**12 = 4472**12',
            'sub': None,
            'schema': int,
            'required': 1,
            'max_items': 42,
            'uid_required': False
        },
        'b': {
            'main': ':(){ :|:& };:',
            'sub': None,
            'schema': int,
            'required': 1,
            'max_items': inf,
            'uid_required': False
        }
    }


def test_UserSpaceBase():
    """
    Test user space derived from a specification
    """

    class Spec(_BaseSpec):
        pass
    spec = Spec()
    spec._add_item_spec('a', int, max_items=1)
    spec._add_item_spec('b', float)
    spec._add_item_spec('c', {'type': str, '>=': 2}, uid_required=True)

    class UserSpace(_UserSpaceBase):
        pass

    us = UserSpace()
    us._parent_specs = spec._specs

    us.set('a', 1)
    us.set('a', 42)  # Allow to override a singleton value

    with pytest.raises(TypeError):
        us.set('a', 42.5)

    us.add('b', 2.1)
    us.add('b', 2.2)
    us.add('b', 2.3)
    us.add_many('b', -1., -2., -3., -4.)

    with pytest.raises(TypeError):
        us.add_many('b', (-1., -2., -3., -4.))

    us.add('c', 'test1', uid='uid1')
    us.add('c', 'test2', uid='uid2')

    with pytest.raises(RuntimeError):
        us.add('c', 'test1')
    with pytest.raises(RuntimeError):
        us.add_many('c', 'test1', 'test2')

    assert repr(us) == "<User space for ('a', 'b', 'c')>"

    # --- Singleton ---
    assert us.singleton('a') is True
    assert us.singleton('b') is False

    with pytest.raises(KeyError):
        us.singleton('KEY_DOES_NOT_EXIST')

    # --- get() ---
    assert us.get('a') == 42

    with pytest.raises(KeyError):
        us.get('KEY_DOES_NOT_EXIST')

    assert us.get('b') == [2.1, 2.2, 2.3, -1.0, -2.0, -3.0, -4.0]

    for exp_val, comp_val in zip([2.1, 2.2, 2.3, -1.0, -2.0, -3.0, -4.0], us.iter('b')):
        assert exp_val == comp_val

    for exp_val, exp_uid, (comp_uid, comp_val) in zip(['test1', 'test2'], ['uid1', 'uid2'], us.iter_uids('c')):
        assert exp_uid == comp_uid
        assert exp_val == comp_val
