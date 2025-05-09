#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework import FeatureSpec, ModelSpec
from mframework import log
log.on


def test_basic():
    """
    Test basic functionality of 'ModelSpec'
    """
    print()

    # ===== Specifications =====

    fspec_beam = FeatureSpec()
    fspec_beam.add_prop_spec('A', int, max_items=1)
    fspec_beam.add_prop_spec('B', int)

    fspec_study = FeatureSpec()
    fspec_study.add_prop_spec('static', bool, max_items=1)

    mspec = ModelSpec()
    mspec.add_feature_spec('beam', fspec_beam)
    mspec.add_feature_spec('study', fspec_study, required=1, max_items=1)

    class Model(mspec.user_class):
        def run(self):
            pass
    beam_model = Model()

    # ===== User logic =====

    beam1 = beam_model.add_feature('beam')
    beam1.set('A', 1)
    beam1.add('B', 2)
    beam1.add('B', 3)

    beam2 = beam_model.add_feature('beam')
    beam2.set('A', 2)
    beam2.add('B', 4)
    beam2.add('B', 6)

    study = beam_model.set_feature('study')
    study.set('static', True)

    # Beam 1 and 2 have different values for the same property
    assert beam1.get('A') == 1
    assert beam2.get('A') == 2

    # Beams are different, but the parent specification is the same
    assert beam1.uid != beam2.uid
    assert beam1._parent_uid == beam2._parent_uid


def test_from_dict():
    fspec1 = FeatureSpec()
    fspec1.add_prop_spec('a', int, max_items=1)
    fspec1.add_prop_spec('b', str, max_items=1)
    fspec1.add_prop_spec('c', {'type': bool}, max_items=1)

    fspec2 = FeatureSpec()
    fspec2.add_prop_spec('one', int, max_items=1)
    fspec2.add_prop_spec('two', str, max_items=1)
    fspec2.add_prop_spec('three', {'type': bool}, max_items=1)

    mspec = ModelSpec()
    mspec.add_feature_spec('A', fspec1, max_items=1)
    mspec.add_feature_spec('B', fspec2, max_items=1)

    class Model(mspec.user_class):
        def run(self):
            pass

    props1 = {
        'a': [42, ],
        'b': ['snake', ],
        'c': [True, ],
    }

    props2 = {
        'one': [43, ],
        'two': ['Snake', ],
        'three': [False, ],
    }

    model_dict = {
        'A': [props1, ],
        'B': [props2, ],
    }

    m = Model().from_dict(model_dict)
    m_fa = m.get('A')
    m_fb = m.get('B')

    assert m_fa.get('a') == 42
    assert m_fa.get('b') == 'snake'
    assert m_fa.get('c') is True

    assert m_fb.get('one') == 43
    assert m_fb.get('two') == 'Snake'
    assert m_fb.get('three') is False


def test_errors_add_feature_spec():
    """
    Test 'add_feature_spec()' method
    """

    fspec_door = FeatureSpec()
    fspec_door.add_prop_spec('color', str)

    fspec_motor = FeatureSpec()
    fspec_motor.add_prop_spec('type', str)

    mspec_car = ModelSpec()

    # ----- Wrong type: key -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec(22, fspec_door)

    # ----- Wrong type: feature_spec -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door.user_class)

    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door.user_class())

    # ----- Wrong type: max_items -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door, max_items='yes')

    # Cannot add property twice...
    mspec_car.add_feature_spec('motor', fspec_motor)
    with pytest.raises(KeyError):
        mspec_car.add_feature_spec('motor', fspec_motor)


def test_error_set_feature():
    """

    """
    print()

    fspec = FeatureSpec()
    mspec = ModelSpec()

    fspec.add_prop_spec('a', int, max_items=1)
    fspec.add_prop_spec('b', int)
    mspec.add_feature_spec('A', fspec, max_items=1)

    fspec.add_prop_spec('1', str, max_items=1)
    fspec.add_prop_spec('2', str)
    mspec.add_feature_spec('B', fspec)

    class Model(mspec.user_class):
        def run(self):
            pass
    m = Model()

    # Feature 'A' is non-singleton
    with pytest.raises(RuntimeError):
        m.add_feature('A')
    m.set_feature('A')

    # Feature 'B' is singleton
    with pytest.raises(RuntimeError):
        m.set_feature('B')
    m.add_feature('B')
    m.add_feature('B')
    m.add_feature('B')

    fa = m.get('A')
    fa.set('a', 2)

    fb = m.get('B')
    assert len(fb) == 3

    with pytest.raises(KeyError):
        for _ in m.iter('A'):
            pass

    for _ in m.iter('B'):
        pass
