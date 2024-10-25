import i2c

#istruzioni lcd(1byte), pag.24-25 datasheet HD44780U
CLEAR=0x01
RETURN_HOME=0x02
ENTRY_MODE_SET=0x04
DISPLAY_CONTROL=0x08
CURSOR_SHIFT=0x10
FUNCTION_SET=0x20
SET_CGR_ADDRESS=0x40
SET_DDR_ADDRESS=0x80

#formato messaggi(1 byte), ogni bit setta valore logico pin lcd
#DB7|DB6|DB5|DB4|A|E|(R/W)|RS (datasheet LCD1602 pag.10)
#possiamo inviare 4 bit dati alla volta
#quindi dobbiamo settare interfaccia a 4bit su lcd
#di conseguenza ci servono 2 write per scrivere un'istruzione

INIZIALIZATION=0x30 # istruzione per fase inizializzazione display
CONFIGURATION=0x20 #configura interfaccia 4 bit
ENABLE=0x04 #0b0000 0100
BACKLIGTH_ON=0x08 #0B00001000

DATA_MODE=0x01
COMMAND_MODE=0x00
LINE_1_ADDRESS=0x00
LINE_2_ADDRESS=0x40

class lcd_i2c():

    def __init__(self,port):
        self.porta=port #porta i2c
        self.backup=0

        #inizializzazione display 
        #possiamo inviare 4bit dati alla volta, quindi dobbiamo
        #settare l'interfaccia lcd a 4bit (pag.46 datasheet HD44780U)
        self.invia(INIZIALIZATION)
        self.toggle_enable()
        sleep(5)
        self.invia(INIZIALIZATION)
        self.toggle_enable()
        sleep(2)
        self.invia(INIZIALIZATION)
        self.toggle_enable()
        sleep(2)

        self.invia(CONFIGURATION)
        self.toggle_enable()

        self.invia_istruzione(FUNCTION_SET | 0x08, COMMAND_MODE) #settiamo 2 linee con font 5x8 dots
        self.invia_istruzione(DISPLAY_CONTROL | 0x04, COMMAND_MODE)#accendiamo display
        self.invia_istruzione(ENTRY_MODE_SET | 0x02, COMMAND_MODE)# autoincremento cursore
        self.invia_istruzione(CLEAR, COMMAND_MODE)
    
        sleep(5)

    def invia(self,data):
        self.backup=data
        self.porta.write(bytearray([data]))


    def toggle_enable(self): #pag58 HD44780U
        sleep(5)
        self.invia(self.backup | ENABLE)
        sleep(5)
        self.invia(self.backup & ~ENABLE)
        sleep(5)

    def invia_istruzione(self,data,mode):
        #formato messaggi(1 byte), ogni bit setta valore logico pin lcd
        #DB7|DB6|DB5|DB4|A|E|(R/W)|RS (datasheet LCD1602 pag.10)
        #possiamo inviare 4 bit istruzione alla volta
        #quindi ci servono 2 write per scrivere un'istruzione
        #inviamo prima la parte alta, poi la parte bassa(pag.22 datasheet HD44780)
        # mode = 1 (RS = 1) inviamo dati
        # mode = 0 (RS = 0) inviamo un comando 

        #parte alta istruzione
        high = data & 0xF0
        message = high | mode | BACKLIGTH_ON
        
        self.invia(message)
        self.toggle_enable()

        #parte bassa istruzione
        low = ((data<<4) & 0xF0)
        message = low | mode | BACKLIGTH_ON
        
        self.invia(message)
        self.toggle_enable()

        sleep(2) #istruzione più lunga impiega 1.52 ms

    def clear(self):
        self.invia_istruzione(CLEAR,COMMAND_MODE)

    def stampa(self,text):
        msg=bytearray(text)
        # Stampa stringa su display
        for char in msg:
            # \n in binario è 10
            if char == 10:
                self.invia_istruzione(SET_DDR_ADDRESS | LINE_2_ADDRESS, COMMAND_MODE) # va a capo
            else:
                self.invia_istruzione(char, DATA_MODE)

    def set_address(self,address):
        #settiamo un indirizzo DDRam 
        self.invia_istruzione(SET_DDR_ADDRESS | address,COMMAND_MODE)


    
