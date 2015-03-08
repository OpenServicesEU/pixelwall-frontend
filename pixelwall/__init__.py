# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys

from gi.repository import Gtk, GObject
from dbus.mainloop.glib import DBusGMainLoop

from .display import Display

VERSION = '0.0.1'

def run_display():
    Gtk.init(sys.argv)
    GObject.threads_init()
    loop = DBusGMainLoop(set_as_default=True)
    display = Display(loop)
    Gtk.main()

if __name__ == '__main__':
    run_display()
