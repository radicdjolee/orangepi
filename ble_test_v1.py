import time
from bluepy import btle
from wifi import Cell, Scheme

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID_SSID = "4fafc202-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID_PASSWORD = "4fafc203-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID_WIFI_LIST = "4fafc204-1fb5-459e-8fcc-c5c9c331914b"  # Karakteristika za Wi-Fi listu

class MyBLEServer(btle.Peripheral):
    def __init__(self):
        super().__init__()

        self.deviceConnected = False

        # Dodavanje servisa
        self.service = btle.Service(SERVICE_UUID)
        self.addService(self.service)

        # Dodavanje karakteristika
        self.ssidCharacteristic = btle.Characteristic(CHARACTERISTIC_UUID_SSID,
                                                      properties=btle.Characteristic.prop_read | btle.Characteristic.prop_write)
        self.passwordCharacteristic = btle.Characteristic(CHARACTERISTIC_UUID_PASSWORD,
                                                          properties=btle.Characteristic.prop_read | btle.Characteristic.prop_write)
        self.wifiListCharacteristic = btle.Characteristic(CHARACTERISTIC_UUID_WIFI_LIST,
                                                          properties=btle.Characteristic.prop_read)

        self.service.addCharacteristic(self.ssidCharacteristic)
        self.service.addCharacteristic(self.passwordCharacteristic)
        self.service.addCharacteristic(self.wifiListCharacteristic)

        self.addService(self.service)

        # Pokretanje BLE servera
        self.startAdvertising()
        print("BLE Server je pokrenut, čeka na klijenta...")

    def onConnect(self):
        self.deviceConnected = True

    def onDisconnect(self):
        self.deviceConnected = False

    def scanWiFiNetworks(self):
        print("Skeniram Wi-Fi mreže...")
        wifi_list = ""
        
        for cell in Cell.all('wlan0'):
            wifi_list += cell.ssid + "\n"
            print(cell.ssid)

        self.wifiListCharacteristic.setValue(wifi_list.encode('utf-8'))

    def connectToWiFi(self):
        while self.deviceConnected:
            ssid = self.ssidCharacteristic.getValue().decode('utf-8')
            password = self.passwordCharacteristic.getValue().decode('utf-8')

            if ssid and password:
                print(f"Povezujem se na WiFi: {ssid}")
                try:
                    # Priključivanje na WiFi
                    scheme = Scheme.for_cell('wlan0', ssid, password)
                    scheme.save()
                    scheme.activate()
                    print("Povezan na WiFi!")
                except Exception as e:
                    print(f"Greška prilikom povezivanja: {e}")

                # Resetovanje BLE karakteristika
                self.deviceConnected = False
                self.ssidCharacteristic.setValue(b"")
                self.passwordCharacteristic.setValue(b"")

if __name__ == "__main__":
    server = MyBLEServer()

    while True:
        server.scanWiFiNetworks()
        server.connectToWiFi()
        time.sleep(1)
