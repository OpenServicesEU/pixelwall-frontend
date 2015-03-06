from __future__ import print_function

import sys

from gi.repository import Gtk, GObject

from pixelwall.display import Display

VERSION = '0.0.1'

def run_display():
    Gtk.init(sys.argv)
    GObject.threads_init()
    display = Display()
    Gtk.main()

if __name__ == '__main__':
    run_display()
