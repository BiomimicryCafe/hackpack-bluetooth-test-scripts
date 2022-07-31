from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
from bluez_peripheral.gatt.service import ServiceCollection
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
import asyncio

my_service_ids = ["BEEF"] # The services that we're advertising.
my_appearance = 0 # The appearance of my service.
# See https://specificationrefs.bluetooth.com/assigned-values/Appearance%20Values.pdf
my_timeout = 60 # Advert should last 60 seconds before ending (assuming other local
# services aren't being advertised).

# Define a service like so.
class MyService(Service):
   def __init__(self):
      self._some_value = None
      # Call the super constructor to set the UUID.
      super().__init__("BEEF", True)

   # Use the characteristic decorator to define your own characteristics.
   # Set the allowed access methods using the characteristic flags.
   @characteristic("BEF0", CharFlags.READ)
   def my_readonly_characteristic(self, options):
      # Characteristics need to return bytes.
      return bytes("Hello World!", "utf-8")

   # This is a write only characteristic.
   @characteristic("BEF1", CharFlags.WRITE)
   def my_writeonly_characteristic(self, options):
      # This function is a placeholder.
      # In Python 3.9+ you don't need this function (See PEP 614)
      pass

   # In Python 3.9+:
   # @characteristic("BEF1", CharFlags.WRITE).setter
   # Define a characteristic writing function like so.
   @my_readonly_characteristic.setter
   def my_writeonly_characteristic(self, value, options):
      # Your characteristics will need to handle bytes.
      self._some_value = value

   # Associate a descriptor with your characteristic like so.
   # Descriptors have largely the same flags available as characteristics.
   @descriptor("BEF2", my_readonly_characteristic, DescFlags.READ)
   # Alternatively you could write this:
   # @my_writeonly_characteristic.descriptor("BEF2", DescFlags.READ)
   def my_readonly_descriptors(self, options):
      # Descriptors also need to handle bytes.
      return bytes("This characteristic is completely pointless!", "utf-8")

async def mainasync():
   while (True):
      # This needs running in an awaitable context.
      bus = await get_message_bus()

      # Instance and register your service.
      service = MyService()
      await service.register(bus)
      
if __name__ == '__main__':
   advert = Advertisement("HACKPACK", my_service_ids, my_appearance, my_timeout)
   asyncio.run(mainasync())