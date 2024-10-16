import os
import time
from pydbus import SystemBus

# Povezivanje na System Bus
bus = SystemBus()

# Povezivanje na Bluetooth adapter
bluetooth_adapter = bus.get('org.bluez', '/org/bluez/hci0')

# Uključivanje Bluetooth-a
bluetooth_adapter.Powered = True
print("Bluetooth je uključen.")

# Uključivanje agent-a
os.system('bluetoothctl agent on')

# Uključivanje vidljivosti
os.system('bluetoothctl discoverable on')
print("Uređaj je sada vidljiv.")

# Opcionalno: Uključivanje skeniranja za povezivanje
os.system('bluetoothctl scan on')
print("Skeniranje je pokrenuto...")

# Držite program aktivnim da biste mogli primati veze
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Uklanjanje skeniranja i izlazak iz programa
    os.system('bluetoothctl scan off')
    print("Skeniranje je zaustavljeno.")
