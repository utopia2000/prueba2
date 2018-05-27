import RPi.GPIO as GPIO
import sys, tty, termios, time
import serial, os

state=0
ipAddress = '192.168.0.1'
#ipAddress = '172.17.91.1'
response = 0
sensor=0
RED=1
#------------------------------------------------------------------------------#
#----------------------------CONFIGURACIONES-----------------------------------# 
#------------------------------------------------------------------------------#

#------------------------Configuracion Puertos---------------------------------#

GPIO.setmode(GPIO.BCM)
#GPIO.setup(Number_Pin,GPIO.IN_OUT)
#GPIO.output(Number_Pin,1_0)

EN1 = 22
EN2 = 27
EN3 = 24
EN4 = 25
LEDS = 5
NET = 6

GPIO.setup(EN1,GPIO.OUT)
GPIO.setup(EN2,GPIO.OUT)
GPIO.setup(EN3,GPIO.OUT)
GPIO.setup(EN4,GPIO.OUT)
GPIO.setup(LEDS,GPIO.OUT)
GPIO.setup(NET,GPIO.OUT)

GPIO.output(EN1,0)
GPIO.output(EN2,0)
GPIO.output(EN3,0)
GPIO.output(EN4,0)
GPIO.output(LEDS,0)
GPIO.output(NET,0)
#-----------------------------------FIN----------------------------------------#

#--------------------------Configuracion Serial--------------------------------#

#ls /dev/tty*
Arduino=serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=5)
#Limpia el puerto serial
Arduino.flushInput() 
#-----------------------------------FIN----------------------------------------#


#------------------------------------------------------------------------------#
#------------------------------Funciones---------------------------------------#
#------------------------------------------------------------------------------#

#Separa y muestra la informacion recivida por serial
def separar(data):
    if ("Distancia" in data):
	label = data.split(":") #Separa Distancia del numero
	dist = float(label[1])
	print "Distancia US: " +str(dist)

	
#Determina que tecla se oprimio y la retorna 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

#Retorna un string con el estado de conexion
def check_ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus

# Infinite loop that will not end until the user presses the
# exit key

if __name__ == '__main__':
   
    while (True):

        #Verifica conexion
        while(RED==1):
            response = os.system("ping -c 1 " + ipAddress)
            # and then check the response...
            if response == 0:
                print("Conectado")
                GPIO.output(NET,0)
                RED=0
                
                #Limpia la pantalla
                os.system("clear")

                # Instrucciones de uso
                print("1: Luces")
                print("2: Sensores")
                print("3: Bateria")
                print("w/s: Adelante/Atras")
                print("a/d: Izquierda/Derecha")
                print("t: Detener")
                print("x: Salir")
                
            else:
                print("Error en la conexion")
                GPIO.output(NET,1)
                time.sleep(0.5)
                GPIO.output(NET,0)
                time.sleep(0.5)
                GPIO.output(NET,1)
                #Prender led de advertencia

        #Guarda la tecla presionada en 'tecla'
        RED=1
        tecla = getch()
        
        #Prender LED's
        if(tecla=="1"):
            #Prender luces
            if(state==0):
                state=1
                GPIO.output(LEDS,1)
                print("LED's prendidos")
            #Apagar Luces    
            else:
                state=0
                GPIO.output(LEDS,0)
                print("LED's apagados")
                            
        #Habilitar lectura de los sensores            
        elif(tecla=="2"):
            print('Inicializando Sensores...')

            if(sensor==0):
                Arduino.write('c')
                sensor=1
            else:
                Arduino.write('v')
                sensor=0
                        
            data=Arduino.readline()
            print(data)
            time.sleep(0.5)
            
        #nivel de la bateria
        elif(tecla=="3"):
            Arduino.write('x')
            time.sleep(0.5)
            print(Arduino.readline())
                
        #Salir del programa
        elif(tecla=="x"):
            print ("Programa finalizado")
            break
                    
        elif (tecla == "s"):
            print("Atras")
            GPIO.output(EN1,1)
            GPIO.output(EN2,0)
            GPIO.output(EN3,1)
            GPIO.output(EN4,0)
            Arduino.write('z')
                    
        elif (tecla == "w"):
            print("Adelante")
            GPIO.output(EN1,0)
            GPIO.output(EN2,1)
            GPIO.output(EN3,0)
            GPIO.output(EN4,1)
            Arduino.write('z')
                    
        elif (tecla == "a"):
            print("Izquierda")
            GPIO.output(EN1,1)
            GPIO.output(EN2,0)
            GPIO.output(EN3,0)
            GPIO.output(EN4,1)
            Arduino.write('n')
                    
        elif (tecla == "d"):
            print("Derecha")
            GPIO.output(EN1,0)
            GPIO.output(EN2,1)
            GPIO.output(EN3,1)
            GPIO.output(EN4,0)
            Arduino.write('n')

        elif (tecla == "t"):
            print("Parar")
            GPIO.output(EN1,0)
            GPIO.output(EN2,0)
            GPIO.output(EN3,0)
            GPIO.output(EN4,0)
            Arduino.write('z')

        else:
            print (tecla)
