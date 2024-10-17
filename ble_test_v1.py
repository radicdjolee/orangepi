from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

def main():
    # Kreiranje BLE uređaja
    peripheral = btle.Peripheral()
    peripheral.setDelegate(MyDelegate())

    # Konfiguracija oglašavanja
    advertising_data = btle.AdvertiseData()
    advertising_data.addServiceUUID(btle.UUID("180F"))  # UUID za Battery Service
    advertising_data.addLocalName("MyBLEDevice")  # Ime uređaja
    peripheral.advertiseStart(advertising_data)

    print("BLE uređaj je sada vidljiv!")

    try:
        while True:
            pass  # Održavanje procesa
    except KeyboardInterrupt:
        pass
    finally:
        peripheral.advertiseStop()
        peripheral.disconnect()

if __name__ == "__main__":
    main()
