# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

class ServerView(Gtk.IconView):

    store = Gtk.ListStore(Pixbuf, str, str, int)

    def __init__(self, *args, **kwargs):
        super(ServerView, self).__init__(*args, **kwargs)
        self.set_model(self.store)
        self.set_pixbuf_column(0)
        self.set_text_column(1)
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

    def add_server(self, name, address, port):
        pixbuf = Gtk.IconTheme.get_default().load_icon('gtk-network', 64, 0)
        self.store.append((pixbuf, name, address, port))

    def remove_Server(self, name):
        # TODO
        pass
