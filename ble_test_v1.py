import asyncio
from aiobleserver import Server, Service, Characteristic, UUID

# Definišite UUID-ove za servis i karakteristiku
SERVICE_UUID = UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = UUID("12345678-1234-5678-1234-56789abcdef1")

# Kreirajte klasu za karakteristiku
class MyCharacteristic(Characteristic):
    def __init__(self):
        super().__init__(CHARACTERISTIC_UUID, ["read", "write"])
        self.value = b"Hello, BLE!"

    async def read(self):
        return self.value

    async def write(self, value):
        self.value = value

# Kreirajte klasu za servis
class MyService(Service):
    def __init__(self):
        super().__init__(SERVICE_UUID, [MyCharacteristic()])

# Definišite funkciju za pokretanje servera
async def main():
    # Kreirajte server
    server = Server()
    
    # Dodajte servis
    await server.add_service(MyService())

    # Pokrenite server
    await server.start()
    print("BLE server je pokrenut")

    # Očekujte veze
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

    # Zaustavite server kada se završi
    await server.stop()
    print("BLE server je zaustavljen")

# Pokrenite glavni događaj
if __name__ == "__main__":
    asyncio.run(main())
