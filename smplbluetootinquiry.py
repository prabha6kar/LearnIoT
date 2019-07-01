# simple inquiry example
import bluetooth
from pprint import pprint

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print (nearby_devices)

print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))

