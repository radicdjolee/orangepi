from bluepy.btle import Peripheral, Service, Characteristic, UUID, Descriptor

# Definisanje UUID za servis i karakteristiku
service_uuid = UUID("12345678-1234-5678-1234-56789abcdef0")
char_uuid = UUID("abcdef01-1234-5678-1234-56789abcdef0")

# Kreiranje klase za BLE server
class BLEServer(Peripheral):
    def __init__(self):
        Peripheral.__init__(self)

        # Kreiraj BLE servis
        service = Service(service_uuid, True)
        self.addService(service)

        # Kreiraj karakteristiku unutar servisa
        characteristic = Characteristic(
            char_uuid, Characteristic.PROPERTY_READ | Characteristic.PROPERTY_WRITE, 
            Characteristic.PERM_READ | Characteristic.PERM_WRITE
        )
        service.addCharacteristic(characteristic)

        # Dodaj karakteristiku servisu
        descriptor = Descriptor(UUID(0x2901), "Description")
        characteristic.addDescriptor(descriptor)

        # Aktiviraj server
        self.advertise(True)
        print("BLE server aktivan!")

# Pokreni BLE server
server = BLEServer()
