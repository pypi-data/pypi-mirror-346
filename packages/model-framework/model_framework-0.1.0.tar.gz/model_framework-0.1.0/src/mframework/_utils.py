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
Utils
"""

from collections.abc import MutableMapping


class DictLike(MutableMapping):

    def __init__(self, *args, **kwargs):
        """
        Dictionary-like object.

        * Keys must be strings.
        """

        self.mapping = {}
        self.update(*args, **kwargs)

    def __str__(self):
        return f"{self.mapping!r}"

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.mapping!r})"

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"invalid key {key!r}: must be of type {str}, not {type(key)}")

        self.mapping[key] = value

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        del self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)


class UniqueDict(DictLike):
    """
    Values cannot be reassigned if a key is already in the dictionary.
    """

    def __setitem__(self, key, value):
        if key in self.mapping.keys():
            raise KeyError(f"key {key!r}: entry already defined")
        super().__setitem__(key, value)


class UIDDict(MutableMapping):

    def __init__(self, *args, **kwargs):
        """
        General purpose dictionary that groups items according to a 'type'
        (main key) in a sub-dictionary with integers as sub-keys. Note that
        multiple assignments to the same main key do not overwrite the previous
        value, but add a new entry in the sub-dictionary.

        Example:

            >>> from mframework._utils import ItemDict
            >>> t = ItemDict()
            >>> t['a'] = 'apple'
            >>> t['a'] = 'banana'
            >>> t
            ItemDict({'a': {0: 'apple', 1: 'banana'}})
            >>>

        Notes:

            * The main key (kmain) must be a string.
            * To easily find items, UIDs can be assigned to specific values.
        """

        self._map = dict()  # Maps [kmain][idx] --> value
        self._idx = dict()  # Maps [kmain][uid] --> idx
        self._uid = dict()  # Maps [kmain][idx] --> uid
        self.update(*args, **kwargs)

    def __str__(self):
        return f"{self._map!r}"

    def __repr__(self):
        return f"< {self.__class__.__qualname__}({self._map!r}) >"

    def __setitem__(self, kmain, value):
        if kmain not in self._map.keys():
            self.__missing__(kmain)
            self._map[kmain][0] = value
        else:
            self._map[kmain][len(self._map[kmain])] = value

    def __getitem__(self, kmain):
        if kmain not in self._map.keys():
            self.__missing__(kmain)
        return self._map[kmain]

    def __missing__(self, kmain):
        self._map[kmain] = dict()
        self._idx[kmain] = UniqueDict()  # A UID cannot be set twice
        self._uid[kmain] = dict()

    def __delitem__(self, kmain):
        # Do not throw an error if 'kmain' does not exist
        try:
            del self._map[kmain]
            del self._idx[kmain]
            del self._uid[kmain]
        except KeyError:
            pass

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def len_of_type(self, kmain):
        return len(self._map[kmain])

    def assign_uid(self, kmain, uid, idx=-1):
        """
        Assign a UID to a specific value

        Args:
            :kmain: (str) main key (= type)
            :uid: (str) unique identifier
            :idx: (int) item index

        Note:

            * By default, the UID will be assigned to the 'last' entry
        """

        # Get index of last entry
        if idx < 0:
            idx = self.len_of_type(kmain) - 1

        self._idx[kmain][uid] = idx
        self._uid[kmain][idx] = uid

    def get_by_uid(self, kmain, uid):
        """
        Return the value for a UID

        Args:
            :kmain: (str) main key (= type)
            :uid: (str) unique identifier
        """

        idx = self._idx[kmain][uid]
        return self._map[kmain][idx]

    def iter_uids(self, kmain):
        """
        Yield (uid, value) for a main key

        Args:
            :kmain: (str) main key (= type)
        """

        for idx in sorted(self._idx[kmain].values()):
            yield self._uid[kmain][idx], self._map[kmain][idx]

    def iter_from_to(self, kmain, uid1, uid2):
        """
        Yield values from a UID1 to UID2

        Args:
            :kmain: (str) main key (= type)
            :uid1: (str) first UID
            :uid2: (str) second UID
        """

        idx1 = self._idx[kmain][uid1]
        idx2 = self._idx[kmain][uid2]
        for idx in range(idx1, idx2+1):
            yield self._map[kmain][idx]

    def get_uid(self, kmain, idx, default=None):
        """
        Return the value for a UID

        Args:
            :kmain: (str) main key (= type)
            :idx: (int) item index
        """

        if idx == 'first':
            idx = 0
        elif idx == 'last':
            idx = max(self._uid[kmain].keys())

        try:
            return self._uid[kmain][idx]
        except KeyError:
            return default


class ItemDict(UIDDict):

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"invalid key {key!r}: must be of type {str}, not {type(key)}")
        super().__setitem__(key, value)
