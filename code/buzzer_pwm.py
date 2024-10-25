#CLASSE PER BUZZER

import gpio
import pwm
import time

class buzzer:

    def __init__(self, buzzerPin):
        self.buzzerPin = buzzerPin
        gpio.mode(self.buzzerPin, OUTPUT)

    def allarme(self): #gestione di un allarme temporizzato
        tempo = time.time()
        timeout = tempo + 15
        while tempo <= timeout:
            for x in range(2272,1000,-25): #440hrz a 1000hrz
                pwm.write(self.buzzerPin,x,100, MICROS)
                sleep(50)
            for x in range(1000,2272,25):# 1000hrz a 440hrz
                pwm.write(self.buzzerPin,x,100,MICROS)
                sleep(50)
            tempo = time.time() 
    
    def stop_allarme(self):
        pwm.write(self.buzzerPin, 0,0)
   




