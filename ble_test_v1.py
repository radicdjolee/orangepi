import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import subprocess

# Funkcija za dobijanje liste dostupnih Wi-Fi mreža
def get_wifi_networks():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        networks = result.stdout.decode('utf-8').strip().split("\n")
        return networks
    except Exception as e:
        print(f"Greška prilikom dobijanja Wi-Fi mreža: {e}")
        return []

# BLE karakteristika
class WiFiCharacteristic:
    def __init__(self, bus, index, service):
        self.path = service.path + "/char" + str(index)
        self.uuid = '12345678-1234-5678-1234-56789abcdef1'
        self.service = service
        self.flags = ['read']
    
    def ReadValue(self, options):
        print("Pročitan zahtev za Wi-Fi mreže")
        networks = get_wifi_networks()
        networks_str = "\n".join(networks)
        return dbus.Array([dbus.Byte(c) for c in networks_str.encode()], signature=dbus.Signature('y'))

# BLE usluga
class WiFiService:
    def __init__(self, bus, index):
        self.path = f"/org/bluez/example/service{index}"
        self.uuid = '12345678-1234-5678-1234-56789abcdef0'
        self.characteristics = [WiFiCharacteristic(bus, 0, self)]

# BLE aplikacija
class BLEApplication:
    def __init__(self, bus):
        self.path = '/org/bluez/example'
        self.services = [WiFiService(bus, 0)]

    def get_service(self, index):
        return self.services[index]

# Main funkcija
def main():
    # Pokretanje DBus
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    # Kreiraj BLE aplikaciju
    app = BLEApplication(bus)

    # Uključivanje BLE periferije
    adapter = bus.get_object('org.bluez', '/org/bluez/hci0')
    adapter_props = dbus.Interface(adapter, dbus.PROPERTIES_IFACE)
    adapter_props.Set('org.bluez.Adapter1', 'Powered', dbus.Boolean(1))

    print("BLE server pokrenut i spreman za povezivanje...")
    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
