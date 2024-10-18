import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def register_app_cb():
    print("GATT server je uspešno registrovan.")

def register_app_error_cb(error):
    print(f"Neuspešno registrovanje GATT servera: {error}")

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    # Interfejs za GATT server
    obj = bus.get_object('org.bluez', '/org/bluez/hci0')
    gatt_manager = dbus.Interface(obj, 'org.bluez.GattManager1')

    # Definiši servise, karakteristike ovde
    gatt_manager.RegisterApplication('/', {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)
    
    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
