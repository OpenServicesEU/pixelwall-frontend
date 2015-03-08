# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import json
import serial

from gi.repository import Gtk, GObject

class JsonReader(GObject.GObject):

    line = ''

    def __init__(self, tty, baud, *args, **kwargs):
        super(JsonReader, self).__init__(*args, **kwargs)
        print("Init serial reader")
        self.serial = serial.Serial(tty, baud)
        self.serial.flushInput()

    def start(self):
        print("Start serial reader")
        self.watch = GObject.io_add_watch(
            self.serial.fileno(),
            GObject.IO_IN | GObject.IO_PRI,
            self.handle_data
        )

    def stop(self):
        print("Stop serial reader")
        GObject.remove_source(self.watch)

    def handle_data(self, source, condition):
        data = self.serial.read(1)
        self.line += data
        if data == "\n":
            try:
                json.loads(self.line)
            except ValueError:
                # Ignore malformed JSON
                pass
            else:
                self.emit("jsonData", self.line)
            finally:
                self.line = ''
        return True

    @GObject.Signal(arg_types=(str,))
    def jsonData(self, data):
        print("Sending JSON data: %s" % data)
