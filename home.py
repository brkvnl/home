from Tkinter import *
import tkFont
import time
import RPi.GPIO as GPIO
import os
import glob
import time

# Made by:
# Burak Vanli
# 27 Jan 2018

# 0.8

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-0014229f4bff')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
time1= ''
win = Tk()

bf=open ('boilerfile.txt', 'r')
bf.seek(-1, 2)
boilerState=bf.read(1)
print('Boiler is ', boilerState)
bf.close()

wf=open ('waterfile.txt', 'r')
wf.seek(-1, 2)
waterState=wf.read(1)
print('Watering is ', waterState)
wf.close()

lf=open ('lampfile.txt', 'r')
lf.seek(-1, 2)
lampState = lf.read(1)
print('Lamp is ', lampState)
lf.close()

yf=open ('SICAKSUfile.txt', 'r')
yf.seek(-1, 2)
SICAKSUState=yf.read(1)
print('SICAKSU is ', SICAKSUState)
yf.close()

hf=open ('hidrofile.txt', 'r')
hf.seek(-1, 2)
hidroState=hf.read(1)
print('HIDROFOR is ', hidroState)
hf.close()


#Date and Time***********************
myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
clock = Label(win, font = myFont, height = 2, width = 20)
clock.grid(row = 1, column = 1)

def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c

#***************************************
def boilerON():
        print("BOILER button pressed")
        bf=open('boilerfile.txt', 'w')
        if GPIO.input(12) :
                GPIO.output(12,GPIO.LOW)
                GPIO.output(29,GPIO.LOW)
                GPIO.output(31,GPIO.LOW)
		bf.write('1')
		boilerButton["text"] = "ISITMA ON"
		print time1, 'BOILER ON'
		bf.close()
	else:
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(29,GPIO.HIGH)
                GPIO.output(31,GPIO.HIGH)
		bf.write('0')
		boilerButton["text"] = "ISITMA OFF"
		print time1, 'BOILER OFF'
		bf.close()


def rainbirdON():
	print("RAINBIRD button pressed")
	wf=open ('waterfile.txt', 'w')
	if GPIO.input(11) :
 		GPIO.output(11,GPIO.LOW)
		wf.write('1')
		waterButton["text"] = "SULAMA ON"
		print time1, 'WATER ON'
                wf.close()
	else:
		GPIO.output(11, GPIO.HIGH)
		wf.write('0')
		waterButton["text"] = "SULAMA OFF"
		print time1, 'WATER OFF'
		wf.close()

def lampON():
	print("LAMP button pressed")
	print int(int(time.strftime('%M'))%10)%2
	lf=open ('lampfile.txt', 'w')
	if GPIO.input(13) :
 		GPIO.output(13,GPIO.LOW)
		lf.write('1')
		lampButton["text"] = "LAMBA ON"
		print time1, 'LAMP ON'
		lf.close()
	else:
		GPIO.output(13, GPIO.HIGH)
		lf.write('0')
		lampButton["text"] = "LAMBA OFF"
		print time1, 'LAMP OFF'
		lf.close()




def SICAKSUON():
	print("SICAKSU button pressed")
	yf=open ('SICAKSUfile.txt', 'w')
	#testLabel['text']= time.strftime('%S')

	if GPIO.input(15) :
 		GPIO.output(15,GPIO.LOW)
		yf.write('1')
		SICAKSUButton["text"] = "SICAK SU ON"
		print time1, 'SICAKSU ON'
                yf.close()
	else:
		GPIO.output(15, GPIO.HIGH)
		yf.write('0')
		SICAKSUButton["text"] = "SICAK SU OFF"
		print time1, 'SICAKSU OFF'
		yf.close()




def hidroforON():
	print("HIDROFOR button pressed")
	hf=open ('hidrofile.txt', 'w')
	if GPIO.input(33) :
 		GPIO.output(33,GPIO.LOW)
		hf.write('1')
		hidroButton["text"] = "HIDRO ON"
		print time1, 'HIDROFOR ON'
                hf.close()
	else:
		GPIO.output(33, GPIO.HIGH)
		hf.write('0')
		hidroButton["text"] = "HIDRO OFF"
		print time1, 'HIDROFOR OFF'
		hf.close()




def exitProgram():
	print("Exit Button pressed")
	GPIO.cleanup()
	win.quit()

def lampturnON():

	if GPIO.input(13)==1:#TURN ON
		lampON()

def lampturnOFF():

	if GPIO.input(13)==0:#TURN OFF
		lampON()


def tick():
	global time1
	time2 = time.strftime('%d:%m:%Y - %H:%M:%S')
	if time2 != time1:
		time1 = time2
		clock.config(text=time2)

                if int(time.strftime('%H')) < 6 and int(time.strftime('%S')) == 0 :

			if int(int(time.strftime('%M'))/15)%2 == 1:
                		lampturnOFF()
			else:
				lampturnON()


		if int(time.strftime('%H')) == 16 and int(time.strftime('%M')) < 1 and int(time.strftime('%S')) == 1:
			lampturnON()



                #4 YOLLU VANA SIKISMASINI ONLEYICI EGZERSIZ HAREKETI
		if GPIO.input(12) == 1:
                        # Isitma kapaliysa
                        if int(time.strftime('%H')) % 6 == 0 and GPIO.input(32) == 1:
                                GPIO.output(32, GPIO.LOW)
                                print time1, 'VANA AC'
                                # Vanayi ac

                        if int(time.strftime('%H')) % 6 == 1 and GPIO.input(32) == 0:
                                GPIO.output(32, GPIO.HIGH)
                                print time1, 'VANA KAPAT'
                                # Vanayi kapat
                        
                #4 YOLLU VANA EGZERSIZ HAREKETI








		#if int(time.strftime('%H')) == 0 and int(time.strftime('%M')) < 1:
		#	lampturnOFF()








	clock.after(200, tick)
win.title("Yazarlar 22")
win.geometry('520x600')


testLabel= Label(win, text="T FLOW "+ u'\u2103', font=myFont,heigh=1,width=20)
testLabel.grid(row=2,column=1)
boilerButton = Button(win, font = myFont, command = boilerON, height = 1, width =12 )
boilerButton.grid(row = 3, column = 1)
waterButton = Button(win, font = myFont, command = rainbirdON, height = 1, width =12 )
waterButton.grid(row = 4, column = 1)
lampButton = Button(win, font = myFont, command = lampON, height = 1, width =12 )
lampButton.grid(row = 5, column = 1)
SICAKSUButton = Button(win, font = myFont, command = SICAKSUON, height = 1, width =12 )
SICAKSUButton.grid(row = 6, column = 1)
hidroButton = Button(win, font = myFont, command = hidroforON, height = 1, width =12 )
hidroButton.grid(row = 7, column = 1)
exitButton  = Button(win, text = "SON", font = myFont, command = exitProgram, height =1 , width = 6)
exitButton.grid(row = 8, column = 1)

def updateTestLabel():
        ft=read_temp()
        rt=round(ft, 1)
        testLabel['text'] = 'T FLOW '+str(rt)+u'\u2103'
        #tempf=open ("tempfile.txt", "a")
        #tempf.write(str(rt)+' ' +time1 +'\n' )
        #tempf.close()

        testLabel.after(60000, updateTestLabel)

updateTestLabel();

if boilerState  == '1':
        GPIO.output(12, GPIO.LOW)
        GPIO.output(29,GPIO.LOW)
        GPIO.output(31,GPIO.LOW)
        boilerButton["text"] = "ISITMA ON"
if boilerState == '0':
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(29,GPIO.HIGH)
        GPIO.output(31,GPIO.HIGH)
        boilerButton["text"] = "ISITMA OFF"
if waterState  == '1':
        GPIO.output(11, GPIO.LOW)
        waterButton["text"] = "SULAMA ON"
if waterState == '0':
        GPIO.output(11, GPIO.HIGH)
        waterButton["text"] = "SULAMA OFF"
if lampState  == '1':
        GPIO.output(13, GPIO.LOW)
        lampButton["text"] = "LAMBA ON"
if lampState == '0':
        GPIO.output(13, GPIO.HIGH)
        lampButton["text"] = "LAMBA OFF"
if SICAKSUState  == '1':
        GPIO.output(15, GPIO.LOW)
        SICAKSUButton["text"] = "SICAK SU ON"
if SICAKSUState == '0':
        GPIO.output(15, GPIO.HIGH)
        SICAKSUButton["text"] = "SICAK SU OFF"
if hidroState  == '1':
        GPIO.output(33, GPIO.LOW)
        hidroButton["text"] = "HIDRO ON"
if hidroState == '0':
        GPIO.output(33, GPIO.HIGH)
        hidroButton["text"] = "HIDRO OFF"



tick()
mainloop()
