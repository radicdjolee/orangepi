import pygatt
from pygatt.backends import GATTToolBackend

# Inicijalizacija GATT servera
adapter = GATTToolBackend()

# UUID servisa i karakteristike
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Funkcija za rukovanje vezivanjem
def on_connect(device):
    print(f"Connected to {device}")

# Funkcija za rukovanje odbacivanjem
def on_disconnect(device):
    print(f"Disconnected from {device}")

try:
    adapter.start()
    
    # Dodajte servis i karakteristiku
    adapter.add_service(SERVICE_UUID)
    adapter.add_characteristic(CHARACTERISTIC_UUID, properties=['notify', 'read'], initial_value=b'Hello, Bluetooth!')

    print("Bluetooth server pokrenut...")
    
    # U petlji, čekajte na veze
    adapter.run()

except Exception as e:
    print(f"Error: {e}")
finally:
    adapter.stop()
