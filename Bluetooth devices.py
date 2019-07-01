
# coding: utf-8

# In[1]:


#find my phone

import bluetooth

nearby_devices = bluetooth.discover_devices()
nearby_devices


# In[34]:


target_name = "ASUS_X008DA"
target_address = None

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print ("found target bluetooth device with address ", target_address)
else:
    print ("could not find target bluetooth device nearby")


# In[1]:


# Asynchronous device discovery
import bluetooth
import select

class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
    def pre_inquiry(self):
        self.done = False
    
    def device_discovered(self, address, device_class, name):
        print ("%s - %s" % (address, name))

    def inquiry_complete(self):
        self.done = True


# In[5]:


d = MyDiscoverer()
d.find_devices(lookup_names = True)

d


# In[6]:


readfiles = [ d, ]

readfiles

while True:
    rfds = select.select( readfiles, [], [] )[0]

    if d in rfds:
        d.process_event()

    if d.done: break


# In[12]:


# d.device_discovered
d.names_found


# In[1]:


# bluetooth low energy scan
from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))


# In[5]:


# simple inquiry example
import bluetooth
from pprint import pprint

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print (nearby_devices)

print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))


# In[6]:


# find services of the device
service = find_service(address=nearby_devices [0] [0])
pprint(service)


# In[8]:


# Example 3-6. rfcomm-server-sdp.py - Dynamically allocating port numbers and using the Service Discovery 
# Protocol (SDP) to search for and advertise services is a simple process in PyBluez. The get_available_port 
# method finds available L2CAP and RFCOMM ports, advertise_service advertises a service with the local 
# SDP server, and find_service searches Bluetooth devices for a specific service.

from bluetooth import *

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# port = bluetooth.get_available_port(bluetooth.RFCOMM)
port = 3
server_sock.bind(("",port))
server_sock.listen(1)
print ("listening on port %d" % port)

uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
bluetooth.advertise_service( server_sock, "FooBar Service", uuid )

client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock.close()


# In[ ]:


# Example 3-7. rfcomm-client-sdp.py

import sys
import bluetooth

uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
service_matches = bluetooth.find_service( uuid = uuid )

if len(service_matches) == 0:
    print "couldn't find the FooBar service"
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s" % (name, host)

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((host, port))
sock.send("hello!!")
sock.close()

