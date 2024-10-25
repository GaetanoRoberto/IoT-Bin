#CLASSE PER SENSORE A ULTRASUONI

import gpio
import time

class HCSR04:

    def __init__(self, echoPin, triggerPin):
        self.echoPin = echoPin
        self.triggerPin = triggerPin
        gpio.mode(self.echoPin, INPUT)
        gpio.mode(self.triggerPin, OUTPUT)

    def distance(self):   
        #fase di inizializzazione per stabilizzare il sensore
        gpio.set(self.triggerPin, LOW)
        sleep(500, MILLIS)
        #invio un impulso di 10 microsecondi dal triggePin
        gpio.set(self.triggerPin, HIGH)
        sleep(10, MICROS)
        gpio.set(self.triggerPin, LOW)

        start = time.time()
        end = time.time()

        #calcolo tempo durante il quale echoPin è settato ad HIGH
        while gpio.get(self.echoPin) == 0:
            start = time.time() 
        while gpio.get(self.echoPin) == 1:
            end = time.time()

        #tempo che impiega il segnale ad arrivare 
        duration = end - start
        #343 m/s   34300 cm/s
        distance = duration * 34300 / 2 #andata e ritorno
        distance = round(distance, 2)
        return distance

  