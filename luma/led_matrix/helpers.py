# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.


class mutable_string(object):

    def __init__(self, value):
        assert value.__class__ is str
        self.target = value

    def __getattr__(self, attr):
        return self.target.__getattribute__(attr)

    def __getitem__(self, key):
        return self.target[key]

    def __setitem__(self, key, value):
        assert value.__class__ is str
        tmp = list(self.target)
        tmp[key] = value
        self.target = "".join(tmp)

    def __delitem__(self, key):
        tmp = list(self.target)
        del tmp[key]
        self.target = "".join(tmp)

    def __len__(self):
        return len(self.target)

    def __iter__(self):
        return iter(self.target)

    def __str__(self):
        return str(self.target)

    def __repr__(self):
        return repr(self.target)

    def __eq__(self, other):
        return str(self.target) == str(other)

    def __hash__(self):
        return hash(self.target)


class observable(object):
    """
    Wraps any container object such that on inserting, updating or deleting,
    an observer is notified with a payload of the target. All other special name
    methods are passed through parameters unhindered.
    """
    def __init__(self, target, observer):
        self.target = target
        self.observer = observer
        self.observer(self.target)

    def __getattr__(self, attr):
        return self.target.__getattribute__(attr)

    def __getitem__(self, key):
        return self.target.__getitem__(key)

    def __setitem__(self, key, value):
        self.target.__setitem__(key, value)
        self.observer(self.target)

    def __delitem__(self, key):
        self.target.__delitem__(key)
        self.observer(self.target)

    def __len__(self):
        return self.target.__len__()

    def __iter__(self):
        return self.target.__iter__()

    def __str__(self):
        return self.target.__str__()

    def __repr__(self):
        return self.target.__repr__()
