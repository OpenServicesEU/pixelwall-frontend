import sys
import time
import argparse
import json
import serial
import logging

from PySide.QtCore import QUrl, QMargins, QObject, Signal, Slot, QThread
from PySide.QtGui import QApplication, QGridLayout, QWidget
from PySide.QtWebKit import QWebPage, QWebView, QWebSettings

class SerialReader(QThread):

    data_ready = Signal(str)

    def __init__(self, tty):
        self.connected = False
        self.serial = serial.Serial(tty, 115200, timeout=1)
        super(SerialReader).__init__(self)

    def run(self):
        while self.connected:
            try:
                text = self.serial.read(1)
                if text != '':
                    self.data_ready.emit(text)
            except serial.SerialException as e:
                self.connected = False

class Hub(QObject):

    on_client_event = Signal(str)
    on_actor_event = Signal(str)
    on_connect = Signal(str)
    on_disconnect = Signal(str)
    on_serial = Signal(str)

    def __init__(self):
        super(Hub, self).__init__()

    @Slot(str)
    def connect(self, data):
        payload = json.loads(data)
        print(payload)
        self.on_client_event.emit(json.dumps(payload))
        self.on_temperature.emit(23.99)

    @Slot(str)
    def disconnect(self, config):
        print(config)

    @Slot(str)
    def serial(self, data):
        self.on_serial.emit(data)

class Page(QWebPage):

    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

    def userAgentForUrl(self, url):
        return "PixelWall Public Display Client"

class FrontEnd(QWidget):
    def __init__(self, url, tty, parent=None):
        super(FrontEnd, self).__init__(parent)
        self.setWindowTitle('PixelWall')
        self.page = Page()
        self.page.mainFrame().loadFinished.connect(self.loadFinished)
        self.page.mainFrame().javaScriptWindowObjectCleared.connect(self.javaScriptWindowObjectCleared)

        self.serial = SerialReader(tty)
        self.hub = Hub()
        self.serial.data_ready.connect(self.hub.serial)

        webView = QWebView()
        webView.setPage(self.page)
        webView.setUrl(url)

        margins = QMargins(0, 0, 0, 0)

        layout = QGridLayout()
        layout.setContentsMargins(margins)
        layout.addWidget(webView)

        self.setLayout(layout)
        self.setAutoFillBackground(True);

    def javaScriptWindowObjectCleared(self):
        self.page.mainFrame().addToJavaScriptWindowObject("PixelWall", hub)
        print('javaScriptWindowObjectCleared has finished')

    def loadFinished(self):
        self.page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        print('loadFinished has finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simplistic browser frontend for PixelWall.')
    parser.add_argument('--verbose', action='store_true', help='Be verbose')
    parser.add_argument('url', type=QUrl, help='The URL for the PixelWall master server')
    parser.add_argument('tty', type=str, default='/dev/ttymxc3', help='TTY on which the SAM is connected')

    args = parser.parse_args()
    app = QApplication(sys.argv)
    basic = FrontEnd(args.url, args.tty)
    #basic.showFullScreen()
    basic.show()
    sys.exit(app.exec_())
