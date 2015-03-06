from __future__ import print_function

import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gtk, GObject

from pixelwall.display import Display
from pixelwall.discoverer import Discoverer

class Pixelwall(object):

    def __init__(self):
        Gtk.init(sys.argv)
        loop = DBusGMainLoop(set_as_default=True)
        GObject.threads_init()
        discoverer = Discoverer("_pixelwall._tcp", loop)
        display = Display()
        discoverer.connect('newServer', display.add_server)
        discoverer.connect('removeServer', display.remove_server)
        Gtk.main()

if __name__ == "__main__":
    Pixelwall()
