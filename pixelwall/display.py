from __future__ import print_function

from gi.repository import Gtk, Gdk, WebKit, GObject, Soup

from .webview import WebView
from .servers import ServerView

class Display(Gtk.Window):

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        self.set_title("Pixelwall")
        #self.set_gravity(Gdk.Gravity.CENTER)
        #self.set_position(Gtk.WindowPosition.CENTER)
        #self.set_default_size(640, 480)
        self.connect("delete-event", Gtk.main_quit)
        self.fullscreen()
        #inspector = webview.get_inspector()
        #inspector.connect("inspect-web-view", self.activate_inspector, splitter)
        self.serverview = ServerView()
        self.serverview.connect("item-activated", self.selected_server)
        self.add(self.serverview)
        self.show_all()

    def selected_server(self, widget, item):
        model = widget.get_model()

        name = model[item][1]
        address = model[item][2]
        port = model[item][3]

        url = "http://%s:%i/" % (address, port)
        print("You selected", name, url)
        #proxy_uri = Soup.URI.new("http://127.0.0.1:8080")
        #session = WebKit.get_default_session().set_property("proxy-uri")
        #session.set_property("proxy-uri",proxy_uri)
        props= {}
        for key in Gtk.ContainerClass.list_child_properties(type(self)):
            props[key.name]= self.child_get_property(self.serverview, key.name)

        self.serverview.hide()
        self.remove(self.serverview)
        self.webview = WebView()
        self.add(self.webview)

        for name, value in props.iteritems():
            self.child_set_property(self.webview, name, value)
        self.show_all()
        self.webview.open("http://www.google.at")

    def add_server(self, sender, name, address, port):
        print("Adding %s (%s:%i)" % (name, address, port))
        self.serverview.add_server(name, address, port)

    def remove_server(self, sender, name):
        print("Removing %s" % name)


