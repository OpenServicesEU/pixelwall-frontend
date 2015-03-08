# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import os
import ConfigParser

from gi.repository import Gtk, Gdk

from .webview import Browser
from .servers import ServerView
from .dbus import Avahi
from .serial import JsonReader
from .config import Config

class Display(Gtk.Window):

    def __init__(self, loop, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)

        self.config = Config('/apps/pixelwall')
        print("%s:%s"% (self.config.tty, self.config.baud))
        if self.config.tty and self.config.baud:
            serial = JsonReader(self.config.tty, self.config.baud)
            serial.start()
        self.set_title("Pixelwall")
        self.connect("delete-event", Gtk.main_quit)
        self.fullscreen()

        if self.config.uri:
            self.load_uri(self.config.uri)
        else:
            avahi = Avahi('_pixelwall._tcp', loop)
            avahi.connect('newServer', self.add_server)
            avahi.connect('removeServer', self.remove_server)
            self.serverview = ServerView()
            self.serverview.connect("item-activated", self.selected_server)
            self.add(self.serverview)
            self.show_all()

    def selected_server(self, widget, item):
        model = widget.get_model()

        name = model[item][1]
        address = model[item][2]
        port = model[item][3]

        uri = "http://%s:%i/" % (address, port)
        print("You selected", name, uri)

        self.config.uri = uri

        self.serverview.hide()
        self.remove(self.serverview)
        self.serverview.destroy()

        self.load_uri(uri)

    def load_uri(self, uri):
        self.webview = Browser()
        self.add(self.webview)

        self.show_all()
        self.webview.load_uri(uri)

    def add_server(self, sender, name, address, port):
        print("Adding %s (%s:%i)" % (name, address, port))
        self.serverview.add_server(name, address, port)

    def remove_server(self, sender, name):
        print("Removing %s" % name)
        #TODO


