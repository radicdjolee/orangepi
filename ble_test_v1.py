from bluepy.btle import Peripheral, UUID, Advertisement

def advertise_ble_device():
    # Kreiraj oglas (Advertisement) za BLE uređaj
    advertisement = Advertisement()
    
    # Definiši UUID koji će uređaj oglašavati
    service_uuid = UUID("12345678-1234-5678-1234-56789abcdef0")  # Nasumičan UUID
    advertisement.addServiceUUID(service_uuid)
    
    # Podešavanje informacija o uređaju
    advertisement.addName("OrangePiBLE")  # Ime uređaja koji će biti vidljiv
    
    # Startuj oglašavanje
    print("Oglašavam BLE uređaj...")
    advertisement.start()
    
    # Oglašavaj neograničeno dugo
    try:
        while True:
            pass  # Uređaj ostaje vidljiv dok se ne prekine
    except KeyboardInterrupt:
        print("Zaustavljam oglašavanje BLE uređaja...")
        advertisement.stop()

if __name__ == "__main__":
    advertise_ble_device()
