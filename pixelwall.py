import sys
import time
import argparse
import json
import serial
import logging

from PySide.QtCore import QUrl, QMargins, QObject, Signal, Slot, QThread
from PySide.QtGui import QApplication, QGridLayout, QWidget
from PySide.QtWebKit import QWebPage, QWebView, QWebSettings

logger = logging.getLogger(__name__)

class SerialJsonReader(QThread):

    message = Signal(str)

    def __init__(self, tty):
        super(SerialJsonReader).__init__(self)
        self.connected = False
        self.serial = serial.Serial(tty, 115200, timeout=1)

    def run(self):
        while self.connected:
            try:
                text = self.serial.read(1)
                if text != '':
                    self.message.emit(text)
            except serial.SerialException as e:
                self.connected = False

class MockSerialJsonReader(QThread):

    on_message = Signal(str)

    def run(self):
        while True:
            QThread.sleep(5)
            print('Sending mock JSON data ...')
            self.on_message.emit(json.dumps({'temperature': 23.5}))

class DemoHub(QObject):

    on_client_event = Signal(str)
    on_actor_event = Signal(str)
    on_connect = Signal(str)
    on_disconnect = Signal(str)
    on_serial = Signal(str)

    def __init__(self):
        super(DemoHub, self).__init__()

    @Slot(str)
    def connect(self, data):
        print(data)
        payload = json.loads(data)
        print(payload)
        self.on_client_event.emit(json.dumps(payload))

    @Slot(str)
    def disconnect(self, config):
        print(config)

class Page(QWebPage):

    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

    def userAgentForUrl(self, url):
        return "PixelWall Public Display Client"

class FrontEnd(QWidget):

    bridges = {}

    def __init__(self, url, tty=None, parent=None):
        super(FrontEnd, self).__init__(parent)
        self.setWindowTitle('PixelWall')
        self.page = Page()
        self.page.mainFrame().loadFinished.connect(self.loadFinished)
        self.page.mainFrame().javaScriptWindowObjectCleared.connect(self.javaScriptWindowObjectCleared)

        self.bridges['pixelWallDemoHub'] = DemoHub()
        if tty:
            reader = SerialJsonReader(tty)
        else:
            reader = MockSerialJsonReader()
        reader.finished.connect(reader.deleteLater)
        reader.start()
        self.bridges['pixelWallSerialJsonReader'] = reader

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
        for objname, bridge in self.bridges.items():
            logger.info('Adding bridge: {0}', objname)
            print('Adding bridge: {0}'.format(objname))
            self.page.mainFrame().addToJavaScriptWindowObject(objname, bridge)
        print('javaScriptWindowObjectCleared has finished')

    def loadFinished(self):
        self.page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        print('loadFinished has finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simplistic browser frontend for PixelWall.')
    parser.add_argument('url', type=QUrl, help='The URL for the PixelWall master server')
    parser.add_argument('tty', nargs='?', type=str, default=None, help='TTY on which the SAM is connected')

    parser.add_argument('-d','--debug',
                           help='Print lots of debugging statements',
                           action="store_const",dest="loglevel",const=logging.DEBUG,
                           default=logging.WARNING
                       )
    parser.add_argument('-v','--verbose',
                           help='Be verbose',
                           action="store_const",dest="loglevel",const=logging.INFO
                       )
    args = parser.parse_args()
    logger.setLevel(args.loglevel)
    app = QApplication(sys.argv)
    basic = FrontEnd(args.url, args.tty)
    if args.loglevel == logging.DEBUG:
        basic.show()
    else:
        basic.showFullScreen()
    sys.exit(app.exec_())
