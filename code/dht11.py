#CLASSE PER SENSORE DI UMIDITA E TEMPERATURA

from components.dht11 import dht11
import gpio

class DHT11:
    
    def __init__(self,pin):
        self.dhtPin = pin
        gpio.mode(self.dhtPin, INPUT)
    
    def hum_temp(self):
        return dht11.read(self.dhtPin)
