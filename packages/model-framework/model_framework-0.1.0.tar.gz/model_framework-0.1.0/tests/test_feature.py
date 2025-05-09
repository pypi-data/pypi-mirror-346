#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework import FeatureSpec
from mframework import log
log.on


def test_basic():
    """
    Test basic functionality of 'FeatureSpec'
    """
    print()

    # ===== Specifications =====

    fspec = FeatureSpec()
    fspec.add_prop_spec('A', int, max_items=1)
    fspec.add_prop_spec('B', int, max_items=1)
    fspec.add_prop_spec('C', int)
    fspec.add_prop_spec('D', {'type': int, '>': 0}, max_items=1)

    # Check that schemas cannot be defined twice
    with pytest.raises(KeyError):
        fspec.add_prop_spec('D', str)

    Feature = fspec.user_class
    f = Feature()

    # ===== User logic =====

    # ----- set() method -----
    f.set('A', 5)
    f.set('B', 8)
    f.set('B', 9)

    # Check the added values
    assert f.get('A') == 5
    assert f.get('B') == 9

    # Property 'B' can only have one entry
    assert f.len('B') == 1

    # Check that keys which are not allowed cannot be set
    with pytest.raises(KeyError):
        f.set("PROPERTY_DOES_NOT_EXIST", 10)

    # Value for 'D' can only be positive (see specification)
    f.set('D', 4)
    with pytest.raises(ValueError):
        f.set('D', -4)

    # ----- add() method -----
    f.add('C', 11)
    f.add('C', 22)
    f.add('C', 33)

    # Property 'C' has three entries
    assert f.len('C') == 3

    # Check that keys which are not allowed cannot be added
    with pytest.raises(KeyError):
        f.add("PROPERTY_DOES_NOT_EXIST", 10)

    # Check the added values
    assert f.get('C') == [11, 22, 33]

    exp_items = [11, 22, 33]
    for i, item in enumerate(f.iter('C')):
        assert item == exp_items[i]

    # Cannot iterate over unique property
    with pytest.raises(KeyError):
        for _ in f.iter('A'):
            pass


def test_complex_schema():
    """
    Test variations of more complex property schemas
    """
    print()

    # ===== Specifications =====

    schema_global = {
        'name': {'type': str, 'min_len': 1},
        'mass': {'type': float, '>': 0},
    }

    schema_wing = {
        'id': {'type': str, 'min_len': 3},
        'span': {'type': float, '>': 0},
        'area': {'type': float, '>': 0},
    }

    fspec_aircraft = FeatureSpec()
    fspec_aircraft.add_prop_spec('global', schema_global, max_items=1)
    fspec_aircraft.add_prop_spec('wing', schema_wing)

    Aircraft = fspec_aircraft.user_class
    aircraft = Aircraft()

    # ===== User logic =====

    aircraft.set('global', {'name': 'AD42', 'mass': 50e3})

    aircraft.add('wing', {'id': 'MainWing', 'span': 32.4, 'area': 55.0})
    aircraft.add('wing', {'id': 'HorizTail', 'span': 7.5, 'area': 18.2})

    # Overwrite 'global'
    aircraft.set('global', {'name': 'AD8888', 'mass': 49.9e3})

    # Add method does not apply to 'global'
    with pytest.raises(RuntimeError):
        aircraft.add('global', {'name': 'abc', 'mass': 1.0})

    # Set method does not apply to 'wing'
    with pytest.raises(RuntimeError):
        aircraft.set('wing', {'id': 'abc', 'span': 1.0, 'area': 1.0})

    # Cause schemadict error
    with pytest.raises(TypeError):
        aircraft.set('wing', {'id': 'abc', 'span': 'WRONG_VALUE', 'area': 1.0})


def test_from_dict():
    fspec = FeatureSpec()
    fspec.add_prop_spec('a', int, max_items=1)
    fspec.add_prop_spec('b', str, max_items=1)
    fspec.add_prop_spec('c', {'type': bool}, max_items=1)

    Feature = fspec.user_class

    props = {
        'a': [42, ],
        'b': ['snake', ],
        'c': [True, ],
    }

    f = Feature().from_dict(props)

    assert f.get('a') == 42
    assert f.get('b') == 'snake'
    assert f.get('c') is True


def test_error_add_property_spec():
    """
    Test method 'add_prop_spec()'
    """

    fspec = FeatureSpec()

    # ----- Wrong type: key -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec(44, int)

    # ----- Wrong type: schema -----
    class MySpecialNumber:
        pass
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', MySpecialNumber)

    # ----- Wrong type: max_items -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', int, max_items='yes')

    # ----- Wrong type: required -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', int, required='yes', max_items=1)

    # Cannot add property twice...
    fspec.add_prop_spec('color', str)
    with pytest.raises(KeyError):
        fspec.add_prop_spec('color', str)


def test_error_provide_user_class():
    """
    Test method 'user_class'
    """
    print()

    fspec = FeatureSpec()
    fspec.add_prop_spec('a', int, max_items=1)
    fspec.add_prop_spec('b', int)
    Feature = fspec.user_class

    f = Feature()
    f.set('a', 12)
    f.add_many('b', 11, 22, 33)

    with pytest.raises(KeyError):
        f.set('x', 55)

    with pytest.raises(RuntimeError):
        f.add('a', 55)

    with pytest.raises(RuntimeError):
        f.set('b', 55)

    assert f.len('a') == 1
    assert f.len('b') == 3
    assert f.get('a') == 12
    assert f.get('b') == [11, 22, 33]
