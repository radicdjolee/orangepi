import dbus
import dbus.mainloop.glib
import sys
from gi.repository import GLib

# Inicijalizacija DBus petlje
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Definiši osnovne DBus adrese za adapter i BLE oglašavanje
BUS_NAME = "org.bluez"
ADAPTER_IFACE = "org.bluez.Adapter1"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
ADVERT_PATH = "/org/bluez/example/advertisement0"

# DBus main loop
def main():
    bus = dbus.SystemBus()

    # Pronađi Bluetooth adapter
    adapter_path = None
    obj_manager = dbus.Interface(bus.get_object(BUS_NAME, "/"),
                                 "org.freedesktop.DBus.ObjectManager")

    objects = obj_manager.GetManagedObjects()
    for obj_path, interfaces in objects.items():
        if ADAPTER_IFACE in interfaces:
            adapter_path = obj_path
            break

    if not adapter_path:
        print("Bluetooth adapter nije pronađen")
        sys.exit(1)

    # Pokupi LEAdvertisingManager interfejs
    adapter = dbus.Interface(bus.get_object(BUS_NAME, adapter_path),
                             LE_ADVERTISING_MANAGER_IFACE)

    # Kreiraj oglas
    ad = Advertisement(bus, ADVERT_PATH, 0)

    # Registruj oglas
    try:
        adapter.RegisterAdvertisement(ad.get_path(), {}, reply_handler=register_cb, error_handler=register_error_cb)
    except dbus.exceptions.DBusException as e:
        print(f"Greška prilikom registracije oglasa: {str(e)}")
        sys.exit(1)

    # Main loop za DBus
    mainloop = GLib.MainLoop()
    mainloop.run()

# Callback funkcije za uspeh i greške
def register_cb():
    print("Oglas registrovan")

def register_error_cb(error):
    print(f"Greška prilikom registracije oglasa: {str(error)}")
    sys.exit(1)

# Klasa za BLE oglas
class Advertisement(dbus.service.Object):
    ADVERT_TYPE = "peripheral"

    def __init__(self, bus, path, index):
        self.path = path
        self.bus = bus
        dbus.service.Object.__init__(self, bus, path)
        self.index = index

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature="ss", out_signature="v")
    def Get(self, interface, property):
        if interface != LE_ADVERTISING_MANAGER_IFACE:
            raise dbus.exceptions.DBusException(
                "org.freedesktop.DBus.Error.UnknownProperty",
                "Unknown property")
        return self.ADVERT_TYPE

    @dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature="ssv", out_signature="")
    def Set(self, interface, property, value):
        raise dbus.exceptions.DBusException(
            "org.freedesktop.DBus.Error.PropertyReadOnly",
            "Property is read-only")

    @dbus.service.method(dbus.INTROSPECTABLE_IFACE,
                         in_signature="", out_signature="s")
    def Introspect(self):
        return ""

    @dbus.service.method("org.bluez.LEAdvertisement1",
                         in_signature="", out_signature="")
    def Release(self):
        print(f"Oglas {self.path} pušten")

    def get_path(self):
        return dbus.ObjectPath(self.path)

if __name__ == "__main__":
    main()
