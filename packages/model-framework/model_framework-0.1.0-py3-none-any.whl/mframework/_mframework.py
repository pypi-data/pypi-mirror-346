#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Model framework
===============

.. code::

    |   User space   |       Specification
    |   ----------   |       -------------
    |                |
    |     Model      |  <---   ModelSpec
    |       |        |             |
    |       |        |             |
    |    Feature     | (<---) FeatureSpec
    |       |        |
    |       |        |
    |  (Properties)  |
"""

from abc import abstractmethod, ABCMeta
from math import inf
from uuid import uuid4

from schemadict import schemadict, STANDARD_VALIDATORS

from ._log import logger
from ._utils import UniqueDict, ItemDict

PRIMITIVE_TYPES = (bool, int, float, str, dict, list, tuple)

SchemadictValidators = STANDARD_VALIDATORS


class S:
    pos_int = {'type': int, '>=': 0}


def is_primitve_type(obj):
    return obj in PRIMITIVE_TYPES


def check_type(var_name, var, exp_type):
    if not isinstance(var, exp_type):
        raise TypeError(
            f"invalid type for {var_name!r}: expected {exp_type}, got {type(var)}"
        )


class SpecDict(UniqueDict):
    """
    Specification dictionary.

    * Specification entries can only be defined once.
    """

    def __setitem__(self, key, value):
        if not isinstance(value, SpecEntry):
            raise ValueError(f"key {key!r}: value must be instance of 'SpecEntry'")
        super().__setitem__(key, value)


class SpecEntry:

    def __init__(self, schema, required=1, max_items=inf, doc='', uid_required=False):
        """
        Specification entry

        Sensible defaults
        -----------------

        * The number of required items is set to 1.
        * The maximum number of items is set to infinity. Setting 'max_items=1'
          would also be sensible. However, it is easier to define infinity here.
        """

        self.schema = schema
        self.required = required
        self.max_items = max_items
        self.doc = doc
        self.uid_required = uid_required

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, required):
        schemadict({'required': S.pos_int}).validate({'required': required})
        self._required = required

    @property
    def max_items(self):
        return self._max_items

    @max_items.setter
    def max_items(self, max_items):
        if max_items != inf:
            schemadict({'max_items': S.pos_int}).validate({'max_items': max_items})
            if max_items < self.required:
                raise ValueError("'max_items' must be larger than the number of required items")
        self._max_items = max_items

    @property
    def singleton(self):
        return self.max_items == 1

    @property
    def uid_required(self):
        return self._uid_required

    @uid_required.setter
    def uid_required(self, uid_required):
        check_type('uid_required', uid_required, bool)
        if uid_required and self.singleton:
            raise ValueError("'uid_required' does only apply if item is singleton")
        self._uid_required = uid_required

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        check_type('doc', doc, str)
        self._doc = doc


class _BaseSpec:

    def __init__(self):
        """
        Base class to store a collection of item specifications.

        The term 'item' may refer to a property (e.g. the number 5) if this
        class describes a feature, or it may also refer to a feature itself if
        this class describes a model.

        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """

        self.uid = str(uuid4())
        self._specs = SpecDict()

    @property
    def keys(self):
        """Return all spec keys"""
        return list(self._specs.keys())

    def __repr__(self):
        return f"<Specification for {tuple(self._specs.keys())!r}>"

    def _add_item_spec(self, key, schema, *, required=1, max_items=inf, doc='', uid_required=False):
        """
        Add a specification entry

        Args:
            :key: (str) name of item to specify
            :schema: (obj) specification
            :required: (int) number of required items
            :max_items: (int) maximum number of items
            :doc: (str) documentation
            :uid_required: (str) if True, UID must be set

        Note:
            * 'schema' should be a primitive type or a 'schemadict' if a this
               class describes a feature. It should be an instance of
               'FeatureSpec' if this class describes a model.
            * When calling from subclass, add a user input check for 'schema'
        """

        self._specs[key] = SpecEntry(schema, required, max_items, doc, uid_required)

    def _provide_user_class_from_base(self, base):
        """
        Return a user space class which subclasses from 'base'

        Args:
            :base: (obj) base class

        Returns:
            :UserSpace: (obj) user space class with specification reference
        """

        class UserSpace(base):
            _parent_specs = self._specs
            _parent_uid = self.uid

        return UserSpace

    def get_docs(self):
        """
        Return user documentation

        Returns:
            :docs: (dict) full documentation
        """

        docs = {}
        for key, spec in self._specs.items():
            subdocs = None
            if isinstance(getattr(spec, 'schema', None), _BaseSpec):
                subdocs = spec.schema.get_docs()

            docs[key] = {
                'main': self._specs[key].doc,
                'sub': subdocs,
                'schema': self._specs[key].schema,
                'required': self._specs[key].required,
                'max_items': self._specs[key].max_items,
                'uid_required': self._specs[key].uid_required,
            }
        return docs


class _UserSpaceBase:

    _level = '$NONE'
    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        Base class for user space functionality for 'model' or 'feature'.

        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """

        self.uid = str(uuid4())
        self._items = ItemDict()

    def __repr__(self):
        return f"<User space for {tuple(self._parent_specs.keys())!r}>"

    @property
    def keys(self):
        """Return all item keys"""
        return self._items.keys()

    def singleton(self, key):
        """
        Return True if 'key' specifies singleton items

        Args:
            :key: (str) name of item
        """

        return self._parent_specs[key].singleton

    def from_dict(self, d):
        """
        Add user values from a dictionary

        Args:
            :d: (dict) key-value pairs

        Returns:
            :self: (obj) reference to self
        """

        check_type(f'{d!r}', d, dict)

        for key, value in d.items():
            if key.startswith('$'):
                continue
            self._check_key_in_spec(key)
            if self.singleton(key):
                self.set(key, value[0])
            else:
                self.add_many(key, *value)
        return self

    def to_dict(self):
        """
        Represent model/feature as a dictionary

        Returns:
            :dictionary: (dict) key-value pairs
        """

        return {
            '$level': self._level,
            '$uid': self.uid,
            **{k: list(v.values()) for k, v in self._items.items()}
        }

    def get_default(self, key):
        """
        Return the model/feature default values
        """

        raise NotImplementedError

    def set(self, key, value):
        """
        Set a value (singleton)

        Args:
            :key: (str) name of item to specify
            :value: (obj) value of the item to specify
        """

        self._check_key_in_spec(key)
        self._check_against_schema(key, value)

        if not self.singleton(key):
            raise RuntimeError(f"key {key!r}: method 'set()' does not apply, try 'add()'")

        logger.debug(f"Set property {key!r} = {value!r} in {self!r}")
        del self._items[key]
        self._items[key] = value

    def add(self, key, value, uid=None):
        """
        Add a value (non-singleton)

        Args:
            :key: (str) name of item to specify
            :value: (obj) value of the item to specify
        """

        self._check_key_in_spec(key)
        self._check_below_max_items(key)
        self._check_uid_required(key, uid)
        self._check_against_schema(key, value)

        if self.singleton(key):
            raise RuntimeError(f"key {key!r}: method 'add()' does not apply, try 'set()'")

        logger.debug(f"Add property {key!r} = {value!r} (num: {len(self._items[key])+1}) in {self!r}")
        # "Append" values to dictionary
        self._items[key] = value
        if uid is not None:
            self._items.assign_uid(key, uid)

    def add_many(self, key, *values):
        """
        Add multiple items (non-singleton)

        * Method does not support keys which require UIDs

        Args:
            :key: (str) name of property to specify
            :values: (obj) values of the item to specify
        """

        for value in values:
            self.add(key, value)

    def get(self, key, default=None, *, uid=None):
        """
        Return a value (singleton/non-singleton)

        Args:
            :key: (str) name of item
            :uid: (str) return a named item
            :default: (obj) value returned if value is not found in items

        Returns:
            :value: (obj) value of the item
        """

        # Always throw error if key is not in specification
        self._check_key_in_spec(key)

        # Return the default value if the key is not in the '_items' dict. Note
        # that '_items' returns an empty list if the key is not in the dict.
        if not self._items[key]:
            return default

        if self.singleton(key):
            logger.warning(f"ignoring UID {uid!r} since not applicable for singletons")
            return self._items[key][0]
        else:
            if uid is not None:
                return self._items.get_by_uid(key, uid)
            else:
                return list(self._items[key].values())

    def iter(self, key):
        """
        Return an iterator for values of 'key' (non-singleton)

        Args:
            :key: (str) name of item
        """

        if self.singleton(key):
            raise KeyError(f"Method 'iter()' not supported for item {key!r}, try 'get()'")

        yield from list(self._items[key].values())

    def iter_uids(self, key):
        """
        Return an iterator for values of 'key' (non-singleton)

        Args:
            :key: (str) name of item
        """

        if self.singleton(key):
            raise KeyError(f"Method 'iter()' not supported for item {key!r}, try 'get()'")

        # TODO !!!

        yield from self._items.iter_uids(key)

    def get_uid(self, key, idx):
        return self._items.get_uid(key, idx)

    def len(self, key):
        return len(self._items[key])

    def clear(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def _check_key_in_spec(self, key):
        if key not in self._parent_specs.keys():
            raise KeyError(f"key {key!r} is not in specification")

    def _check_below_max_items(self, key):
        if not len(self._items[key].values()) < self._parent_specs[key].max_items:
            raise RuntimeError(f"maximum number of items for key {key!r} has been set")

    def _check_uid_required(self, key, uid):
        if self._parent_specs[key].uid_required and uid is None:
            raise RuntimeError(f"key {key!r} requires a UID")

    def _check_against_schema(self, key, value):
        # TODO: look over logic
        if isinstance(self._parent_specs[key].schema, dict):
            if not isinstance(value, dict):
                schemadict(
                    {key: self._parent_specs[key].schema},
                    validators=SchemadictValidators,
                ).validate({key: value})
            else:
                # Schema has schemadict format
                schemadict(
                    self._parent_specs[key].schema,
                    validators=SchemadictValidators
                ).validate(value)
        else:  # Schema is of primitive type
            schemadict(
                {key: {'type': self._parent_specs[key].schema}},
                validators=SchemadictValidators
            ).validate({key: value})


class FeatureSpec(_BaseSpec):

    def add_prop_spec(self, key, schema, *, required=1, max_items=inf, doc='', uid_required=False):
        """
        Add a property specification entry

        Args:
            :key: (str) name of property to specify
            :schema: (obj) specification (primitive type, or 'schemadict')
            :required: (int) number of required items
            :max_items: (int) maximum number of items
            :doc: (str) documentation
            :uid_required: (str) if True, UID must be set
        """

        if not (is_primitve_type(schema) or isinstance(schema, dict)):
            raise TypeError(f"'schema' must be a primitive type or a 'schemadict'")

        # Always use a schemadict
        if is_primitve_type(schema):
            schema = {'type': schema}

        super()._add_item_spec(
            key,
            schema,
            required=required,
            max_items=max_items,
            doc=doc,
            uid_required=uid_required,
        )

    @property
    def user_class(self):
        """Return a 'Feature' class with user and user methods"""
        return super()._provide_user_class_from_base(_FeatureUserSpace)


class _FeatureUserSpace(_UserSpaceBase):
    _level = '$feature'


class ModelSpec(_BaseSpec, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

        # The model specification also includes a specification of the result
        # object which should be returned from the user space method 'run()'.
        # The result object must be an instance of this class.
        self._results = None

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        check_type('results', results, self.__class__)
        self._results = results

    def add_feature_spec(self, key, feature_spec, *, required=1, max_items=inf, doc='', uid_required=False):
        """
        Add a feature specification entry

        Args:
            :key: (str) name of feature to specify
            :schema: (obj) specification (instance of FeatureSpec)
            :required: (int) number of required items
            :max_items: (int) maximum number of items
            :doc: (str) documentation
            :uid_required: (str) if True, UID must be set
        """

        if not isinstance(feature_spec, FeatureSpec):
            raise TypeError(f"'feature_spec' must be instance of 'FeatureSpec'")

        super()._add_item_spec(
            key,
            feature_spec,
            required=required,
            max_items=max_items,
            doc=doc,
            uid_required=uid_required,
        )

    @property
    def user_class(self):
        """Return a 'Model' class with user and user methods"""

        class Model(_ModelUserSpace):
            # If the result user space is specified, pass it down to the model
            # user space
            _result_user_class = getattr(self.results, 'user_class', None)

        return super()._provide_user_class_from_base(Model)


class _ModelUserSpace(_UserSpaceBase, metaclass=ABCMeta):
    _level = '$model'
    _result_user_class = None  # Specification of the result object

    def __init__(self):
        super().__init__()
        self.results = None
        self._check_required = True

    def from_dict(self, dictionary):
        """
        Add user values from a dictionary

        Args:
            :dictionary: (dict) key-value pairs

        Returns:
            :self: (obj) reference to self
        """

        for key, fdicts in dictionary.items():
            if key.startswith('$'):
                continue

            self._check_key_in_spec(key)

            for fdict in fdicts:
                if self.singleton(key):
                    feature = self.set_feature(key)
                else:
                    feature = self.add_feature(key)
                feature.from_dict(fdict)
        return self

    def to_dict(self):
        """
        Represent model as a dictionary

        Returns:
            :dictionary: (dict) key-value pairs
        """

        model_dict = {
            '$level': self._level,
            '$uid': self.uid,
        }
        for key, features in self._items.items():
            model_dict[key] = []
            for feature in features.values():
                model_dict[key].append(feature.to_dict())
        return model_dict

    def set(self, key, _):
        return NotImplementedError

    def add(self, key, _):
        return NotImplementedError

    def set_feature(self, key):
        """
        Make a singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        if not self.singleton(key):
            raise RuntimeError(f"key {key!r}: method 'set_feature()' does not apply, try 'add_feature()'")

        logger.debug(f"Set feature {key!r} in {self!r}")
        f_instance = self._parent_specs[key].schema.user_class()
        self._items[key] = f_instance  # Store instance as list of length 1
        return f_instance

    def add_feature(self, key, *, uid=None):
        """
        Add a non-singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        if self.singleton(key):
            raise RuntimeError(f"key {key!r}: method 'add_feature()' does not apply, try 'set_feature()'")

        self._check_uid_required(key, uid)

        logger.debug(f"Add feature {key!r} (num: {len(self._items[key]) + 1}) in {self!r}")
        f_instance = self._parent_specs[key].schema.user_class()
        self._items[key] = f_instance
        if uid is not None:
            self._items.assign_uid(key, uid)
        return f_instance

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        The 'run()' method is the main entry point for evaluating the user
        model. This method needs to be overridden in the subclass. The 'run()'
        method should return an instance of '_result_user_class'. When
        implementing 'run()' in the subclass, the superclass 'run()' method
        should first be called with 'super().run()'.
        """

        # Instantiate the RESULT user if defined
        if self._result_user_class is not None:
            class Results(self._result_user_class):
                def run(self):
                    raise NotImplementedError
            self.results = Results()

        # Check model definition
        if self._check_required:
            self._check_required_items()

    def _check_required_items(self):
        """
        Check if user model instance defines all required features and properties
        """

        # Check features
        for f_key, f_spec in self._parent_specs.items():
            f_defined = self._items
            if int(f_spec.required) > len(f_defined[f_key]):
                raise RuntimeError(
                    f"model error: feature {f_key!r} required >= {int(f_spec.required)} times"
                )

            # Check properties
            for prop in f_defined[f_key].values():
                for p_key, p_spec in prop._parent_specs.items():
                    p_defined = prop._items
                    if int(p_spec.required) > len(p_defined[p_key]):
                        raise RuntimeError(
                            f"model error: property '{f_key}/{p_key}' required >= {int(p_spec.required)} times"
                        )
