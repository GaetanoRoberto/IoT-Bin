#CLASSE DI UTILITA PER IL DISPLAY

import LCD_I2C

class lcd():
    def __init__(self,port):
        self.display=LCD_I2C.lcd_i2c(port)
        self.stady=True
        
    def default(self):
        self.display.clear()
        self.display.stampa("Temperatura\nUmidita")
        self.stady=True
    
    def aggiorna_valori(self,temp,hum):
        if self.stady:
            self.display.set_address(0x0C)
            self.display.stampa(str(int(temp)))
            self.display.stampa("C")
            self.display.set_address(0x4C)
            self.display.stampa(str(int(hum)))
            self.display.stampa("%")
    
    def allarme_temperatura(self):
        self.stady=False
        self.display.clear()
        self.display.stampa("Temperatura alta\nRischio incendio")

    def allarme_pieno(self):
        self.stady=False
        self.display.clear()
        self.display.stampa("Sono pieno\nSvuotami!")