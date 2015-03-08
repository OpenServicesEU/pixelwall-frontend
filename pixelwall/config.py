# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from gi.repository import GObject, GConf

class Config(GObject.GObject):

    type_map = {
        int: lambda client, key, value: client.set_int(key, value),
        str: lambda client, key, value: client.set_string(key, value),
    }

    def __init__(self, path):
        super(Config, self).__init__()
        self.path = path
        self.client = GConf.Client.get_default();
        self.client.add_dir(self.path, GConf.ClientPreloadType.PRELOAD_NONE)

    def key(self, value):
        path = "{path}/{key}".format(path=self.path, key=value)
        print(path)
        return path

    @property
    def uri(self):
        return self.client.get_string(self.key('uri'))

    @uri.setter
    def uri(self, value):
        self.client.set_string(self.key('uri'), value)

    @property
    def tty(self):
        return self.client.get_string(self.key('tty'))

    @tty.setter
    def tty(self, value):
        self.client.set_string(self.key('tty'), value)

    @property
    def baud(self):
        return self.client.get_int(self.key('baud'))

    @baud.setter
    def baud(self, value):
        self.client.set_int(self.key('baud'), value)
