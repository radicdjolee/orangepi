from bluepy.btle import Peripheral, UUID, Characteristic, Service

class MyBluetoothServer(Peripheral):
    def __init__(self):
        Peripheral.__init__(self)
        
        # Definišite UUID servisa i karakteristika
        self.service_uuid = UUID("12345678-1234-5678-1234-56789abcdef0")
        self.characteristic_uuid = UUID("12345678-1234-5678-1234-56789abcdef1")
        
        # Dodajte servis
        self.service = self.addService(self.service_uuid)
        
        # Dodajte karakteristiku
        self.characteristic = self.addCharacteristic(
            self.characteristic_uuid,
            properties=["read", "notify"],
            permissions=["readable"]
        )
        
        self.setValue("Hello, Bluetooth!".encode('utf-8'))

    def start(self):
        self.advertiseService(self.service_uuid)
        print("Bluetooth server pokrenut...")
        self.run()

if __name__ == "__main__":
    server = MyBluetoothServer()
    server.start()
