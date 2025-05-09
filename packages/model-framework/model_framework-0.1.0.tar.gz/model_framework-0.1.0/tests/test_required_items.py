#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework import FeatureSpec, ModelSpec
from mframework import log
log.on


def test_required_items():
    """
    Check that model can only be run if features and properties are
    well-defined
    """
    print()

    # ===== Specifications =====

    fspec_beam = FeatureSpec()
    fspec_beam.add_prop_spec('A', int, required=1, max_items=1)

    fspec_wing = FeatureSpec()
    fspec_wing.add_prop_spec('B', int, required=3, max_items=3)
    # fspec_wing.add_prop_spec('C', int, required=-1)

    mspec = ModelSpec()
    mspec.add_feature_spec('beam', fspec_beam, required=2)
    mspec.add_feature_spec('wing', fspec_wing, required=1)

    class Model(mspec.user_class):
        def run(self):
            super().run()
    beam_model = Model()

    # ===== User logic =====

    beam1 = beam_model.add_feature('beam')
    beam1.set('A', 2)

    beam2 = beam_model.add_feature('beam')
    beam2.set('A', 2)

    # Feature 'wing' needs to be defined
    with pytest.raises(RuntimeError):
        beam_model.run()

    wing1 = beam_model.add_feature('wing')

    # Property 'B' is needs to be defined
    with pytest.raises(RuntimeError):
        beam_model.run()

    wing1.add('B', 11)
    wing1.add('B', 22)
    wing1.add('B', 33)

    # Cannot add more items of type 'B'
    with pytest.raises(RuntimeError):
        wing1.add('B', 44)

    # Model is now well-defined
    beam_model.run()
