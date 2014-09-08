import sys
import time
import argparse
import json
import logging

from PyQt5.QtCore import QUrl, QMargins, QObject, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtSerialPort import QSerialPort

class SerialReader(QObject):

    message_received = pyqtSignal(str)

    def __init__(self, tty, hub):
        super(SerialReader).__init__(self)
        self.hub = hub
        self.serial = QSerialPort(tty)
        self.serial.readyRead.connect(self.read)
        self.serial.setBaudRate(115200)

    @pyqtSlot()
    def read(self):
        print("Got data")
        self.ser.close()
        self.flash_done.emit(0, 0)

    @pyqtSlot()
    def start(self):
        self.serial.open(QIODevice.ReadWrite)

class Hub(QObject):

    on_client_event = pyqtSignal(str)
    on_actor_event = pyqtSignal(str)
    on_connect = pyqtSignal(str)
    on_disconnect = pyqtSignal(str)
    on_temperature = pyqtSignal(float)

    def __init__(self):
        super(Hub, self).__init__()

    @pyqtSlot(str)
    def connect(self, data):
        payload = json.loads(data)
        print(payload)
        self.on_client_event.emit(json.dumps(payload))

    @pyqtSlot(str)
    def disconnect(self, config):
        print(config)

class Page(QWebPage):

    def __init__(self, parent=None):
        super(Page, self).__init__(parent)

    def userAgentForUrl(self, url):
        return "Evitor Public Display Client"

class FrontEnd(QWidget):
    def __init__(self, url, tty, parent=None):
        super(FrontEnd, self).__init__(parent)
        self.setWindowTitle('Evitor')
        self.page = Page()
        self.page.mainFrame().loadFinished.connect(self.loadFinished)
        self.page.mainFrame().javaScriptWindowObjectCleared.connect(self.javaScriptWindowObjectCleared)

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
        hub = Hub()
        self.page.mainFrame().addToJavaScriptWindowObject("Evitor", hub)
        print('javaScriptWindowObjectCleared has finished')

    def loadFinished(self):
        self.page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        print('loadFinished has finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simplistic browser frontend for EviTor.')
    parser.add_argument('--verbose', action='store_true', help='Be verbose')
    parser.add_argument('url', type=QUrl, help='The URL for the Evitor master server')
    parser.add_argument('tty', type=str, default='/dev/ttymxc3', help='TTY on which the SAM is connected')

    args = parser.parse_args()
    app = QApplication(sys.argv)
    basic = FrontEnd(args.url, args.tty)
    #basic.showFullScreen()
    basic.show()
    sys.exit(app.exec_())
