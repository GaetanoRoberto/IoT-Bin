import dht11
import hcsr04
import buzzer_pwm
import lcd
import i2c
from bsp import board
from zdm import zdm
from networking import wifi

#sensore di temperatura e umidità dht11
dhtPin = D5
#sensore ad ultrasuoni 
triggerPin = D14
echoPin = D12
#buzzer
buzzerPin = D15
#porta lcd
lcd_port = i2c.I2c(0x27,I2C0,400000)
#altezza Bidone in cm
altezzaBidone = 18
#istanze sensori
dht = dht11.DHT11(dhtPin)
hcsr = hcsr04.HCSR04(echoPin, triggerPin)
buzzer = buzzer_pwm.buzzer(buzzerPin)
display = lcd.lcd(lcd_port)

#credenziali wi-fi
ssid = "TIM-29909881"
passwd = "gdKi7?bL3"

#job alert
#prende in ingresso: temperatura, riempimento o reset
def alert(agent, args):
    print("Job ricevuto!",args)
    if not "causa" in args:
        return {"msg": "Invalid argument for alert job"}
    c = args["causa"]
    if c == "temperatura": #temperatura critica
        display.allarme_temperatura()
        buzzer.allarme()
    elif c == "riempimento": #bidone pieno
        display.allarme_pieno()
    elif c == "reset": #reset display
        display.default()
    else:
        return {"msg": "Invalid argument for causa"}
    buzzer.stop_allarme() #spegnimento buzzer
    return {"msg": "allarme attivato: %s" % c}

#riempimento del bidone in percentuale
def bidoneRiemp():
    dist = hcsr.distance(echoPin,triggerPin)
    print('Distanza = ', dist)
    return 100 - (dist * 100) /altezzaBidone          

#connessione wi-fi
display.display.stampa("Connessione\nin corso")

try:
    print("configuring wifi...")
    wifi.configure(
        ssid=ssid,
        password=passwd)
    print("connecting to wifi...")
    wifi.start()
    print("connected!",wifi.info())

except WifiBadPassword:
    print("Bad Password")
except WifiBadSSID:
    print("Bad SSID")
except WifiException:
    print("Generic Wifi Exception")
except Exception as e:
    raise e

agent = zdm.Agent(jobs={"alert":alert})
agent.start()
print("publishing...")

display.default() #display mostra umidità e temperatura
hum = 60 #inizializzazione valori per primo errore?
temp = 20

while True:
    try: #dht11 può fallire nella lettura
        hum, temp = dht.hum_temp(dhtPin)
    except:
        print("---Dht11 fails to read---")
    riempimento = bidoneRiemp()
    display.aggiorna_valori(temp, hum)
    if(riempimento>=0 and riempimento<=100): #percentuale corretta per sensore a ultrasuoni
        agent.publish(payload={"temp": str(temp), "hum": str(hum), "riempimento": str(riempimento)}, tag = "bidone")
        print("published data: ", temp, hum, riempimento)
    else: #valori anomali del sensore ad ultrasuoni
        agent.publish(payload={"temp": str(temp), "hum": str(hum)}, tag = "bidone")
        print("published data: ", temp, hum)
    sleep(2500)

