import asyncio
from bleak import BleakServer

# Definiši karakteristiku
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef0"

async def read_characteristic_handler(sender: int, data: bytearray):
    print(f"Received data: {data}")

async def main():
    # Kreiraj BLE server
    server = BleakServer("MyBLEServer")

    # Dodaj karakteristiku
    server.add_characteristic(CHARACTERISTIC_UUID, read_characteristic_handler)

    # Pokreni server
    await server.start()
    print("BLE server started.")

    try:
        while True:
            await asyncio.sleep(1)  # Održavaj server aktivnim
    except KeyboardInterrupt:
        pass
    finally:
        await server.stop()
        print("BLE server stopped.")

if __name__ == "__main__":
    asyncio.run(main())
