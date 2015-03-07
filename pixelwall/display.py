# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import ConfigParser

from gi.repository import Gtk, Gdk
from dbus.mainloop.glib import DBusGMainLoop

from .webview import Browser
from .servers import ServerView
from .dbus import Avahi

class Display(Gtk.Window):

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        loop = DBusGMainLoop(set_as_default=True)
        avahi = Avahi('_pixelwall._tcp', loop)
        avahi.connect('newServer', self.add_server)
        avahi.connect('removeServer', self.remove_server)
        self.set_title("Pixelwall")
        #self.set_gravity(Gdk.Gravity.CENTER)
        #self.set_position(Gtk.WindowPosition.CENTER)
        #self.set_default_size(640, 480)
        self.connect("delete-event", Gtk.main_quit)
        self.fullscreen()

        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.expanduser('~/.pixelwall.cfg'))
        if self.config.has_section('Connection'):
            uri = self.config.get('Connection', 'uri')
            if uri:
                self.load_uri(uri)
                return
        self.show_server_view()

    def show_server_view(self):
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
        if not self.config.has_section('Connection'):
            self.config.add_section('Connection')
        self.config.set('Connection', 'uri', uri)
        with open(os.path.expanduser('~/.pixelwall.cfg'), 'wb') as configfile:
            self.config.write(configfile)

        props= {}
        #for key in Gtk.ContainerClass.list_child_properties(type(self)):
            #props[key.name]= self.child_get_property(self.content, key.name)

        self.serverview.hide()
        self.remove(self.serverview)
        self.serverview.destroy()

        self.load_uri(uri)

    def load_uri(self, uri):
        self.webview = Browser()
        self.add(self.webview)

        #for name, value in props.iteritems():
            #self.child_set_property(self.content, name, value)
        self.show_all()
        self.webview.load_uri(uri)

    def add_server(self, sender, name, address, port):
        print("Adding %s (%s:%i)" % (name, address, port))
        self.serverview.add_server(name, address, port)

    def remove_server(self, sender, name):
        print("Removing %s" % name)
        #TODO


