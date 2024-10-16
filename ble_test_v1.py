import asyncio
from bleak import BleakServer
import subprocess

# UUID-ovi za BLE uslugu i karakteristike
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Funkcija za dobijanje dostupnih Wi-Fi mreža
def get_available_wifi():
    wifi_list = []
    try:
        # Koristi iwlist da dobije dostupne mreže (potreban sudo pristup)
        result = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
        result = result.decode('utf-8')
        # Parsiranje rezultata i pronalazak SSID-ova
        networks = result.split("Cell ")
        for network in networks[1:]:
            if "ESSID:" in network:
                ssid = network.split("ESSID:")[1].strip().replace('"', '')
                wifi_list.append(ssid)
    except Exception as e:
        print(f"Greška prilikom dobijanja Wi-Fi mreža: {e}")
    return wifi_list

# Callback funkcija za rukovanje BLE zahtevima
async def read_wifi(characteristic):
    wifi_list = get_available_wifi()
    return "\n".join(wifi_list).encode("utf-8")

# Main funkcija za pokretanje BLE servera
async def main():
    # Kreiraj BLE server
    server = BleakServer(SERVICE_UUID)
    print("BLE server pokrenut")

    # Dodaj karakteristiku za Wi-Fi listu
    server.add_characteristic(CHARACTERISTIC_UUID, properties=["read"], value=read_wifi)

    # Start servera
    await server.start()
    print(f"Server je aktivan sa UUID {SERVICE_UUID}")

    # Očekuj povezivanje
    try:
        await asyncio.Event().wait()  # Očekuje dok je server aktivan
    except KeyboardInterrupt:
        print("Zaustavljanje servera...")
        await server.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Greška: {e}")
