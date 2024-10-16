from bluepy.btle import Peripheral, UUID, Characteristic

class MyService(Peripheral):
    def __init__(self):
        Peripheral.__init__(self)
        self.service_uuid = UUID("12345678-1234-5678-1234-56789abcdef0")
        self.characteristic_uuid = UUID("12345678-1234-5678-1234-56789abcdef1")
        self.addService(self.service_uuid)
        self.addCharacteristic(self.characteristic_uuid, properties=["notify", "read"])

    def addService(self, uuid):
        service = self.addService(uuid)
        return service

    def addCharacteristic(self, uuid, properties):
        characteristic = Characteristic(uuid, properties)
        return characteristic

if __name__ == "__main__":
    server = MyService()
    server.start()
    print("Bluetooth GATT server pokrenut...")
    server.run()
