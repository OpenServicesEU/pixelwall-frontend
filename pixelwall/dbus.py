# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import dbus
import dbus.service
import avahi

from gi.repository import GObject

class Avahi(GObject.GObject):

    def __init__(self, stype, loop, *args, **kwargs):
        super(Avahi, self).__init__(*args, **kwargs)
        bus = dbus.SystemBus(mainloop=loop)
        self.server = dbus.Interface(
            bus.get_object(
                avahi.DBUS_NAME,
                avahi.DBUS_PATH_SERVER
            ),
            avahi.DBUS_INTERFACE_SERVER
        )
        browser = dbus.Interface(
            bus.get_object(
                avahi.DBUS_NAME,
                self.server.ServiceBrowserNew(
                    avahi.IF_UNSPEC,
                    avahi.PROTO_UNSPEC,
                    stype,
                    '',
                    dbus.UInt32(0)
                )
            ),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER
        )
        browser.connect_to_signal("ItemNew", self.handle_item_new)
        browser.connect_to_signal("ItemRemove", self.handle_item_remove)

    @GObject.Signal(arg_types=(str, str, int))
    def newServer(self, name, address, port):
        pass

    @GObject.Signal(arg_types=(str,))
    def removeServer(self, name, address, port):
        pass

    def handle_service_resolved(self, *args):
        self.emit("newServer", args[2], args[7], args[8])

    def handle_item_new(self, interface, protocol, name, stype, domain, flags):
        self.server.ResolveService(
            interface,
            protocol,
            name,
            stype,
            domain,
            avahi.PROTO_UNSPEC,
            dbus.UInt32(0),
            reply_handler=self.handle_service_resolved,
            error_handler=self.handle_error
        )

    def handle_item_remove(self, interface, protocol, name, stype, domain, flags):
        self.emit("removeServer", name)

    def handle_error(self, *args, **kwargs):
        pass

class Serial(dbus.service.Object):

    def __init__(self, device, loop):
        bus = dbus.SessionBus(mainloop=loop)
        bus_name = dbus.service.BusName('at.openservices.pixelwall.serial', bus)
        super(Serial, self).__init__(bus_name, '/at/openservices/pixelwall/serial')

    @dbus.service.signal('at.openservices.pixelwall.serial')
    def dataReady(self, data):
        print("Data signal: %s" % data)
