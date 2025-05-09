#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mframework import FeatureSpec, ModelSpec, doc2rst
from mframework._serialize import dump_pretty_json
from mframework import log
log.on


def test_feature_doc():
    fspec = FeatureSpec()
    fspec.add_prop_spec('E', {'type': float, '>': 0}, doc="Young's modulus")
    fspec.add_prop_spec('A', {'type': float, '>': 0}, doc="Area")
    docs = fspec.get_docs()

    assert len(docs) == 2
    assert docs['E']['main'] == "Young's modulus"
    assert docs['A']['main'] == "Area"

    assert docs['E']['sub'] is None
    assert docs['A']['sub'] is None


def test_model_doc():
    cross_section = FeatureSpec()
    cross_section.add_prop_spec('E', {'type': float, '>': 0}, doc="Young's modulus")
    cross_section.add_prop_spec('A', {'type': float, '>': 0}, doc="Area")

    geom = FeatureSpec()
    geom.add_prop_spec('point1', list, doc="Coordinates of point 1")
    geom.add_prop_spec('point2', list, doc="Coordinates of point 2")

    mspec = ModelSpec()
    mspec.add_feature_spec('CrossSection', cross_section, doc="Beam cross section")
    mspec.add_feature_spec('Geom', geom, doc="Beam geometry")

    docs = mspec.get_docs()

    assert docs['CrossSection']['main'] == "Beam cross section"
    assert docs['Geom']['main'] == "Beam geometry"

    assert docs['CrossSection']['sub']['E']['main'] == "Young's modulus"
    assert docs['CrossSection']['sub']['A']['main'] == "Area"
    assert docs['Geom']['sub']['point1']['main'] == "Coordinates of point 1"
    assert docs['Geom']['sub']['point2']['main'] == "Coordinates of point 2"


exp_rst = \
"""Feature: beam
-------------

**Description**: A beam carries load
**Singleton**: False

**Required**: True

Property: A [Parent feature: beam]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Description**: Something about property A

**Singleton**: True

**Required**: False

**Schema**:

* *type*: <class 'int'>
* *>*: 0

Property: B [Parent feature: beam]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Description**: Property B is also great

**Singleton**: False

**Required**: False

**Schema**:

* *type*: <class 'int'>

Feature: study
--------------

**Description**: Specify the type of study to run
**Singleton**: True

**Required**: True

Property: static [Parent feature: study]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Singleton**: True

**Required**: False

**Schema**:

* *type*: <class 'bool'>

"""


def test_to_dict_and_documentation():
    """
    Test basic functionality of 'ModelSpec'
    """
    print()

    # ===== Specifications =====

    fspec_beam = FeatureSpec()
    fspec_beam.add_prop_spec('A', {'type': int, '>': 0}, doc='Something about property A', max_items=1)
    fspec_beam.add_prop_spec('B', int, doc='Property B is also great')

    fspec_study = FeatureSpec()
    fspec_study.add_prop_spec('static', bool, max_items=1)

    mspec = ModelSpec()
    mspec.add_feature_spec('beam', fspec_beam, doc='A beam carries load')
    mspec.add_feature_spec('study', fspec_study, max_items=1, doc='Specify the type of study to run')

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

    # ----- Serialization -----
    model_dict = beam_model.to_dict()
    with open('test.json', 'w') as fp:
        dump_pretty_json(model_dict, fp)

    beam_model = Model().from_dict(model_dict)
    beam1 = beam_model.get('beam')[0]
    assert beam1.get('A') == 1
    assert beam1.get('B') == [2, 3]

    # ----- Documentation -----
    # gen_rst = doc2rst(mspec)

    # TODO: add asserts...

    # print(gen_rst)
    # assert gen_rst == exp_rst
