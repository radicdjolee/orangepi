import dbus
import dbus.mainloop.glib
from gi.repository import GLib

class Characteristic(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + f"/char{index}"
        self.uuid = uuid
        self.flags = flags
        self.service = service
        self.value = []
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="", out_signature="ay")
    def ReadValue(self):
        return self.value

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="ay", out_signature="")
    def WriteValue(self, value):
        self.value = value
        print(f"Data written to characteristic: {value}")

class Service(dbus.service.Object):
    def __init__(self, bus, index, uuid, primary):
        self.path = f"/org/bluez/example/service{index}"
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

def register_app_cb():
    print("GATT server successfully registered.")

def register_app_error_cb(error):
    print(f"Failed to register application: {error}")

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    # Create service and characteristic
    service = Service(bus, 0, "12345678-1234-5678-1234-56789abcdef0", True)
    characteristic = Characteristic(bus, 0, "12345678-1234-5678-1234-56789abcdef1", ["read", "write"], service)

    service.add_characteristic(characteristic)

    # Register service
    obj = bus.get_object('org.bluez', '/org/bluez/hci0')
    gatt_manager = dbus.Interface(obj, 'org.bluez.GattManager1')

    gatt_manager.RegisterApplication('/', {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)

    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
