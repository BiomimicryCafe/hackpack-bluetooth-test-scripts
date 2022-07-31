from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio

class CommsService(Service):
   def __init__(self):
      # Base 16 service UUID, This should be a primary service.
      super().__init__("180D", True)

   @Characteristic("2A37", CharFlags.READ)
   def TxCharacteristic(self, options):
      # Characteristics need to return bytes.
      pass
   def send_data(self, new_data):
      # Note that notification is asynchronous (you must await something at some point after calling this).
      self.TxCharacteristic.changed(bytes(new_data, "utf-8"))

   @Characteristic("2A38", CharFlags.WRITE)
   def RxCharacteristic(self, options):
      # This function is called when the characteristic is read.
      # Since this characteristic is notify only this function is a placeholder.
      # You don't need this function Python 3.9+ (See PEP 614).
      # You can generally ignore the options argument 
      # (see Advanced Characteristics and Descriptors Documentation).
      pass



async def main():
   # Alternativly you can request this bus directly from dbus_next.
   bus = await get_message_bus()

   service = CommsService()
   await service.register(bus)

   # An agent is required to handle pairing 
   agent = NoIoAgent()
   # This script needs superuser for this to work.
   await agent.register(bus)

   adapter = await Adapter.get_first(bus)

   # Start an advert that will last for 60 seconds.
   advert = Advertisement("HackPack", ["180D"], 0x0340, 60)
   await advert.register(bus, adapter)

   while True:
   # Update the heart rate.
      service.send_data("hello")
      # Handle dbus requests.
      await asyncio.sleep(5)

      await bus.wait_for_disconnect()

if __name__ == "__main__":
    asyncio.run(main())