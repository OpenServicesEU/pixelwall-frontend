from gi.repository import Gtk, Gdk, WebKit, GObject, Soup

class InspectorWindow(Gtk.Window):

    def __init__(self, inspector):
        super(InspectorWindow, self).__init__()
        self.set_default_size(800, 600)
        self._inspector = inspector
        self._inspector.connect('inspect-web-view', self._inspect_web_view_cb)
        self._inspector.connect('show-window', self._show_window_cb)

    def _inspect_web_view_cb(self, inspector, web_view):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        webview = WebKit.WebView()
        scrolled_window.add(webview)
        scrolled_window.show_all()
        self.add(scrolled_window)
        return webview

    def _show_window_cb(self, inspector):
        self.present()
        return True
