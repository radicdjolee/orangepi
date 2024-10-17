import os
import time

def main():
    # Podesite ime uređaja
    device_name = "MyBLEDevice"

    # Postavljanje oglašavanja
    os.system(f"sudo hciconfig hci0 up")
    os.system(f"sudo hciconfig hci0 noleadv")
    os.system(f"sudo hciconfig hci0 leadv 3")
    os.system(f"sudo hcitool -i hci0 cmd 0x08 0x0001 {device_name}")

    print(f"BLE uređaj '{device_name}' je sada vidljiv!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Zaustavljanje oglašavanja...")
        os.system("sudo hciconfig hci0 noleadv")
        os.system("sudo hciconfig hci0 down")

if __name__ == "__main__":
    main()
