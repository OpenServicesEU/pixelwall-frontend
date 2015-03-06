from __future__ import print_function

from gi.repository import Gtk, Gdk, WebKit, GObject, Soup

from .inspector import InspectorWindow

class WebView(WebKit.WebView):

    user_agent = "Pixelwall"

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.settings = self.get_settings()
        self.settings.set_property("enable-java-applet", False)
        self.settings.set_property("enable-plugins", False)
        self.settings.set_property("enable-scripts", True)
        #self.settings.set_property("enable-file-access-from-file-uris", False)
        #self.settings.set_property("enable-private-browsing", False)
        #self.settings.set_property("enable-spell-checking", False)
        #self.settings.set_property("enable-universal-access-from-file-uris", False)
        #self.settings.set_property("enable-dns-prefetching", True)
        #self.settings.set_property("enable-webaudio", True)
        #self.settings.set_property("enable-webgl", True)
        #self.settings.set_property("enable-fullscreen", True)
        #self.settings.set_property("enable-xss-auditor", False)
        self.settings.set_property("javascript-can-open-windows-automatically", False)
        self.settings.set_property("user-agent", self.user_agent)
        self.settings.set_property("enable-developer-extras", True)
        self.set_full_content_zoom(True)
        self.set_border_width(0)
        #self.set_custom_encoding('UTF-8')
        #self.set_double_buffered(True)
        #self.set_transparent(True)
        #self.set_editable(False)
        #self.set_view_mode(False)
        #self.set_view_source_mode(False)
        InspectorWindow(self.get_inspector())


