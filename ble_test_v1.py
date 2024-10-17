from pydbus import SystemBus
from gi.repository import GLib

# Put do BlueZ servisa na D-Bus-u
BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_CHR_IFACE = 'org.bluez.GattCharacteristic1'

# Definišemo naš servis
class Application:
    def __init__(self):
        self.bus = SystemBus()
        self.adapter_path = '/org/bluez/hci0'  # Adapter path, proveri sa hcitool dev
        self.service_manager = self.bus.get(BLUEZ_SERVICE_NAME, self.adapter_path)
        self.services = []

    def register_app(self):
        # Registrovanje servisa u BlueZ
        self.service_manager.RegisterApplication(self.get_path(), {}, reply_handler=self.on_registered, error_handler=self.on_error)

    def get_path(self):
        return '/myapp/service'

    def on_registered(self):
        print("GATT aplikacija registrovana!")

    def on_error(self, error):
        print(f"Greška pri registrovanju GATT aplikacije: {error}")

class TestService:
    def __init__(self, index):
        self.path = f"/myapp/service{index}"
        self.uuid = '0000180a-0000-1000-8000-00805f9b34fb'  # Primer UUID-a
        self.characteristics = []

    def get_path(self):
        return self.path

class TestCharacteristic:
    def __init__(self, service, index):
        self.path = f"{service.get_path()}/char{index}"
        self.uuid = '00002a29-0000-1000-8000-00805f9b34fb'  # Primer UUID-a
        self.value = []

    def get_path(self):
        return self.path

# Pokretanje servisa
app = Application()
service = TestService(0)
char = TestCharacteristic(service, 0)

app.services.append(service)
service.characteristics.append(char)

# Pokreni aplikaciju
app.register_app()

# Pokrećemo glavni loop
loop = GLib.MainLoop()
loop.run()
