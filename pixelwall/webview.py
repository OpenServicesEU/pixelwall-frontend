# -*- coding: utf-8 -*-
from __future__ import print_function

from gi.repository import Gtk, WebKit2, Soup

from .inspector import InspectorWindow

class Browser(WebKit2.WebView):

    settings = {
        'allow-modal-dialogs': False,
        'enable-developer-extras': True,
        'enable-html5-local-storage': True,
        'enable-java': False,
        'enable-javascript': True,
        'enable-page-cache': True,
        'enable-write-console-messages-to-stdout': True,
        'javascript-can-access-clipboard': False,
        'javascript-can-open-windows-automatically': False,
        'user-agent': 'Pixelwall'
    }

    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)
        settings = self.get_settings()
        for key, value in self.settings.items():
            settings.set_property(key, value)
        #self.settings.set_property("enable-file-access-from-file-uris", False)
        #self.settings.set_property("enable-private-browsing", False)
        #self.settings.set_property("enable-spell-checking", False)
        #self.settings.set_property("enable-universal-access-from-file-uris", False)
        #self.settings.set_property("enable-dns-prefetching", True)
        #self.settings.set_property("enable-webaudio", True)
        #self.settings.set_property("enable-webgl", True)
        #self.settings.set_property("enable-fullscreen", True)
        #self.settings.set_property("enable-xss-auditor", False)
        #self.set_full_content_zoom(True)
        #self.set_border_width(0)
        #self.set_custom_encoding('UTF-8')
        #self.set_double_buffered(True)
        #self.set_transparent(True)
        #self.set_editable(False)
        #self.set_view_mode(False)
        #self.set_view_source_mode(False)
        #InspectorWindow(self.get_inspector())
        #proxy_uri = Soup.URI.new("http://127.0.0.1:8080")
        #session = WebKit.get_default_session().set_property("proxy-uri")
        #session.set_property("proxy-uri",proxy_uri)
