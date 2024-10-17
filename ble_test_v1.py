from bluepy import btle

# Definiši UUID za uslugu
UUID_SERVICE = "12345678-1234-5678-1234-56789abcdef0"

class MyBLEServer(btle.Peripheral):
    def __init__(self):
        super().__init__()
        
        # Dodaj uslugu
        self.service = btle.Service(UUID_SERVICE)
        self.addService(self.service)

    def advertise(self):
        self.setAdvertisingData(b'\x02\x01\x06' + self.service.getHandle())
        self.advertiseStart()

def main():
    server = MyBLEServer()

    # Oglasi se
    server.advertise()
    print("BLE server je sada vidljiv.")

    # Održavaj program u radu
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Zaustavljam server...")
    finally:
        server.disconnect()

if __name__ == "__main__":
    main()
