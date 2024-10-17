from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

def main():
    # Postavljanje BLE uređaja
    peripheral = btle.Peripheral()

    # Postavljanje oglašavanja
    peripheral.setDelegate(MyDelegate())
    peripheral.setAdvertisingData(0x02, "MyBLEDevice", 0x01)

    # Pokretanje oglašavanja
    peripheral.advertiseStart()

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
