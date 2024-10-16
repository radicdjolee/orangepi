import asyncio
from bleak import BleakServer, BleakGATTCharacteristic, BleakGATTService
import subprocess

# UUID za uslugu i karakteristike (promeni ako je potrebno)
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Funkcija za pretragu dostupnih WiFi mreža
def get_wifi_networks():
    # Koristi nmcli za pretragu dostupnih WiFi mreža
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
    networks = result.stdout.decode().split('\n')
    # Filtriraj prazne linije
    networks = [network for network in networks if network]
    return networks

# Callback funkcija kada telefon zatraži podatke
async def on_read_wifi_data(characteristic: BleakGATTCharacteristic):
    wifi_networks = get_wifi_networks()
    # Spajanje dostupnih mreža u jedan string
    wifi_data = "\n".join(wifi_networks)
    print(f"Sending WiFi networks: {wifi_data}")
    return wifi_data.encode('utf-8')

# Kreiraj BLE server i uslugu
async def run_ble_server():
    server = BleakServer()

    # Kreiraj BLE uslugu
    wifi_service = BleakGATTService(SERVICE_UUID)
    
    # Kreiraj karakteristiku za slanje WiFi mreža
    wifi_characteristic = BleakGATTCharacteristic(CHARACTERISTIC_UUID, ["read"], on_read=on_read_wifi_data)
    
    # Dodaj karakteristiku usluzi
    wifi_service.add_characteristic(wifi_characteristic)
    
    # Dodaj uslugu serveru
    server.add_service(wifi_service)

    # Pokreni BLE server
    print("Starting BLE server...")
    await server.start("OrangePi WiFi Scanner")
    print("BLE server started and advertising.")

    # Drži server aktivnim
    await asyncio.sleep(3600)  # Server će raditi 1 sat

# Glavna funkcija
if __name__ == "__main__":
    asyncio.run(run_ble_server())
