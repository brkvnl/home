# Made by:
# Burak Vanli
ModifDate="21 Sep 2020"


from tkinter import *
from tkinter import font
from tkinter import ttk
import RPi.GPIO as GPIO
import os
import glob
import time
import os
import requests

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
base_dir = "/sys/bus/w1/devices/"

device_folder = glob.glob(base_dir + "28-0014229f4bff")[0]
device_file = device_folder + "/w1_slave"

device1_folder = glob.glob(base_dir + "28-0517a1c633ff")[0]
device1_file = device1_folder + "/w1_slave"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  # Kazan
GPIO.setup(11, GPIO.OUT)  # Sulama
GPIO.setup(13, GPIO.OUT)  # Lamba
GPIO.setup(15, GPIO.OUT)  # Sicak Su
GPIO.setup(29, GPIO.OUT)  # Vana Kapama
GPIO.setup(31, GPIO.OUT)  # Vana Acma
GPIO.setup(32, GPIO.OUT)  # Egzersiz
GPIO.setup(33, GPIO.OUT)  # Hidrofor
GPIO.setup(35, GPIO.IN, GPIO.PUD_UP)   # Ev Kapısı
GPIO.setup(36, GPIO.IN, GPIO.PUD_UP)   # Bahçe Kapısı
GPIO.setup(37, GPIO.IN, GPIO.PUD_UP)   # PIR sensör 1
GPIO.setup(38, GPIO.IN, GPIO.PUD_UP)   # PIR sensör 2

win = Tk()
ex1 = True
ex2 = True
exheat = False
now = time.time()

GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)
GPIO.output(32, GPIO.HIGH)

bf = open("boilerfile.txt", "r")
boilerState = bf.read(1)
print("Boiler is ", boilerState)
bf.close()

wf = open("lastex.txt", "r")
wf.seek(0)
lastex = float(wf.read())
print(time.strftime("Last exercise was at %d:%m:%Y - %H:%M:%S.", time.localtime(lastex)))
wf.close()

wf = open("waterfile.txt", "r")
waterState = wf.read(1)
print("Watering is ", waterState)
wf.close()

lf = open("lampfile.txt", "r")
lampState = lf.read(1)
print("Lamp is ", lampState)
lf.close()

yf = open("SICAKSUfile.txt", "r")
SICAKSUState = yf.read(1)
print("SICAKSU is ", SICAKSUState)
yf.close()

hf = open("hidrofile.txt", "r")
hidroState = hf.read(1)
print("HIDROFOR is ", hidroState)
hf.close()
notifState = 1
# Date and Time***********************
myFont = font.Font(family="Helvetica", size=24, weight="bold")


#def post_request(bullet_msg):
# Your IFTTT URL with event name, key and json paramethttps://maker.ifttt.com/trigger/gate_opened/with/key
#r = requests.post('https://maker.ifttt.com/trigger/'+bullet_msg+'/with/key/bgpeGDDB2101-7ibbd9P7')


def read_temp_raw(dosya):
    f = open(dosya, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp(dosya):
    lines = read_temp_raw(dosya)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.200)
        lines = read_temp_raw(dosya)
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# ***************************************
def updateLast():
    global lastex
    lastex = time.time()
    wf = open("lastex.txt", "w")
    wf.write(str(time.time()))
    wf.close()


def boilerON():
    print("BOILER button pressed")
    bf = open("boilerfile.txt", "w")
    if GPIO.input(12):
        GPIO.output(12, GPIO.LOW)
        bf.write("1")
        boilerButton["text"] = "ISITMA ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Heating On", time.localtime(now)))
        bf.close()
    else:
        GPIO.output(12, GPIO.HIGH)
        bf.write("0")
        boilerButton["text"] = "ISITMA OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Heating Off", time.localtime(now)))
        bf.close()


def rainbirdON():
    print("RAINBIRD button pressed")
    wf = open("waterfile.txt", "w")
    if GPIO.input(11):
        GPIO.output(11, GPIO.LOW)
        wf.write("1")
        waterButton["text"] = "SULAMA ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Watering On", time.localtime(now)))
        wf.close()
    else:
        GPIO.output(11, GPIO.HIGH)
        wf.write("0")
        waterButton["text"] = "SULAMA OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Watering Off", time.localtime(now)))
        wf.close()


def lampON():
    print("LAMP button pressed")
    print(int(int(time.strftime("%M")) % 10) % 2)
    lf = open("lampfile.txt", "w")
    if GPIO.input(13):
        GPIO.output(13, GPIO.LOW)
        lf.write("1")
        lampButton["text"] = "LAMBA ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Lamp On", time.localtime(now)))
        lf.close()
    else:
        GPIO.output(13, GPIO.HIGH)
        lf.write("0")
        lampButton["text"] = "LAMBA OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Lamp Off", time.localtime(now)))
        lf.close()


def SICAKSUON():
    print("SICAKSU button pressed")
    yf = open("SICAKSUfile.txt", "w")
    # testLabel["text"]= time.strftime("%S")
    if GPIO.input(15):
        GPIO.output(15, GPIO.LOW)
        yf.write("1")
        SICAKSUButton["text"] = "SICAK SU ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Hot Water On", time.localtime(now)))
        yf.close()
    else:
        GPIO.output(15, GPIO.HIGH)
        yf.write("0")
        SICAKSUButton["text"] = "SICAK SU OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Hot Water Off", time.localtime(now)))
        yf.close()


def hidroforON():
    print("HIDROFOR button pressed")
    hf = open("hidrofile.txt", "w")
    if GPIO.input(33):
        GPIO.output(33, GPIO.LOW)
        hf.write("1")
        hidroButton["text"] = "HIDRO ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Hidrofor On", time.localtime(now)))
        hf.close()
    else:
        GPIO.output(33, GPIO.HIGH)
        hf.write("0")
        hidroButton["text"] = "HIDRO OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Hidrofor Off", time.localtime(now)))
        hf.close()

def pushNotif():
    global notifState
    print("NOTIFICATION button pressed")
    if notifState==0:
        notifState=1
        notifButton["text"] = "BILDIRIM ON"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Bildirim On", time.localtime(now)))

    else:
        notifState=0
        notifButton["text"] = "BILDIRIM OFF"
        print(time.strftime("%d:%m:%Y - %H:%M:%S Bildirim Off", time.localtime(now)))



def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    win.quit()


def lampturnON():
    if GPIO.input(13) == 1:  # TURN ON
        lampON()

def lampturnOFF():
    if GPIO.input(13) == 0:  # TURN OFF
        lampON()

def gate_opened(self):
    time.sleep(1)
    if notifState==1 and GPIO.input(36)==GPIO.HIGH:
        bullet_msg = "gate_opened"
        print("BAHÇE KAPISI ACILIDI")
        print(time.strftime("%d:%m:%Y - %H:%M:%S", time.localtime(now)))
        r = requests.post('https://maker.ifttt.com/trigger/'+bullet_msg+'/with/key/bgpeGDDB2101-7ibbd9P7')
        gatelog = open("gatefile.txt", "a+")
        gatelog.write("Gate : "+time.strftime("%d:%m:%Y - %H:%M:%S", time.localtime(now))+"\n")
        gatelog.close()

def door_opened(self):
    time.sleep(1)
    if notifState==1 and GPIO.input(35)==GPIO.HIGH:
        bullet_msg = "door_opened"
        print("EV KAPISI ACILIDI")
        print(time.strftime("%d:%m:%Y - %H:%M:%S", time.localtime(now)))
        r = requests.post('https://maker.ifttt.com/trigger/'+bullet_msg+'/with/key/bgpeGDDB2101-7ibbd9P7')
        gatelog = open("gatefile.txt", "a+")
        gatelog.write("Door : "+time.strftime("%d:%m:%Y - %H:%M:%S", time.localtime(now))+"\n")
        gatelog.close()

def tick():
    global ex1
    global ex2
    global exheat
    global now
    global lastex
    now = time.time()
    clock.config(text=time.strftime("%d:%m:%Y - %H:%M:%S", time.localtime(now)))
    if ((now - lastex) > 86400):
        ex1 = False
        ex2 = False
        updateLast()
        GPIO.output(29, GPIO.LOW)
        GPIO.output(31, GPIO.LOW)
        GPIO.output(32, GPIO.LOW)
        print(time.strftime("%d:%m:%Y - %H:%M:%S EXERCISE", time.localtime(now)))
        print(time.strftime("%d:%m:%Y - %H:%M:%S VANAYI AC", time.localtime(now)))
        if GPIO.input(12) == 0:
            # Eger boiler aciktiysa kapa ve acik oldugunu hatirla
            exheat = True
            print(time.strftime("%d:%m:%Y - %H:%M:%S KAZANI KAPAT", time.localtime(now)))
            boilerON()
    elif ((now - lastex) > 60 and not ex1):
        print(time.strftime("%d:%m:%Y - %H:%M:%S VANAYI KAPAT", time.localtime(now)))
        GPIO.output(32, GPIO.HIGH)
        ex1 = True
    elif ((now - lastex) > 120 and not ex2):
        print(time.strftime("%d:%m:%Y - %H:%M:%S VANAYI SERBEST BIRAK", time.localtime(now)))
        GPIO.output(29, GPIO.HIGH)
        GPIO.output(31, GPIO.HIGH)
        ex2 = True
    elif ((now - lastex) > 180 and exheat):
        boilerON()
        exheat = False
        print(time.strftime("%d:%m:%Y - %H:%M:%S KAZANI AC", time.localtime(now)))

    if (GPIO.input(36)==GPIO.HIGH):
        gateLabel["text"]= "GATE OPEN"
    else:
        gateLabel["text"]= "GATE CLOSED"

    if (GPIO.input(35)==GPIO.HIGH):
        doorLabel["text"]= "DOOR OPEN"
    else:
        doorLabel["text"]= "DOOR CLOSED"
    clock.after(200, tick)

win.title(ModifDate)
win.geometry("400x600")
clock = Label(win, font=myFont, height=1, width=20)
clock.grid(row=1, column=1)
testLabel1 = Label(win, text="SICAK SU " + u"\u2103", font=myFont, heigh=1, width=20)
testLabel1.grid(row=9, column=1)
testLabel = Label(win, text="ISITMA " + u"\u2103", font=myFont, heigh=1, width=20)
testLabel.grid(row=8, column=1)
boilerButton = Button(win, font=myFont, command=boilerON, height=1, width=12)
boilerButton.grid(row=4, column=1)
waterButton = Button(win, font=myFont, command=rainbirdON, height=1, width=12)
waterButton.grid(row=7, column=1)
lampButton = Button(win, font=myFont, command=lampON, height=1, width=12)
lampButton.grid(row=3, column=1)
SICAKSUButton = Button(win, font=myFont, command=SICAKSUON, height=1, width=12)
SICAKSUButton.grid(row=5, column=1)
hidroButton = Button(win, font=myFont, command=hidroforON, height=1, width=12)
hidroButton.grid(row=6, column=1)
exitButton = Button(win, text="SON", font=myFont, command=exitProgram, height=1, width=6)
exitButton.grid(row=13, column=1)
notifButton = Button(win, text="BILDIRIM", font=myFont, command=pushNotif, height=1, width=12)
notifButton.grid(row=10, column=1)
gateLabel = Label(win, text="GATE", font=myFont, heigh=1, width=20)
gateLabel.grid(row=11, column=1)
doorLabel = Label(win, text="DOOR", font=myFont, heigh=1, width=20)
doorLabel.grid(row=12, column=1)



def updateTestLabel():
    ft = read_temp(device_file)
    rt = round(ft, 1)
    testLabel["text"] = "ISITMA " + str(rt) + u"\u2103"  # BOILER TEMP
    ft1 = read_temp(device1_file)
    rt1 = round(ft1, 1)
    testLabel1["text"] = "SICAK SU " + str(rt1) + u"\u2103"  # WATER TEMP
    testLabel.after(60000, updateTestLabel)


updateTestLabel();

#bu kısım sade ilk çalışmada butonların yazılarını düzenliyor
if boilerState == "1":
    GPIO.output(12, GPIO.LOW)
    boilerButton["text"] = "ISITMA ON"
else:
    GPIO.output(12, GPIO.HIGH)
    boilerButton["text"] = "ISITMA OFF"
if waterState == "1":
    GPIO.output(11, GPIO.LOW)
    waterButton["text"] = "SULAMA ON"
else:
    GPIO.output(11, GPIO.HIGH)
    waterButton["text"] = "SULAMA OFF"
if lampState == "1":
    GPIO.output(13, GPIO.LOW)
    lampButton["text"] = "LAMBA ON"
else:
    GPIO.output(13, GPIO.HIGH)
    lampButton["text"] = "LAMBA OFF"
if SICAKSUState == "1":
    GPIO.output(15, GPIO.LOW)
    SICAKSUButton["text"] = "SICAK SU ON"
else:
    GPIO.output(15, GPIO.HIGH)
    SICAKSUButton["text"] = "SICAK SU OFF"
if hidroState == "1":
    GPIO.output(33, GPIO.LOW)
    hidroButton["text"] = "HIDRO ON"
else:
    GPIO.output(33, GPIO.HIGH)
    hidroButton["text"] = "HIDRO OFF"
if notifState == 1:
    notifButton["text"] = "BILDIRIM ON"
else:
    notifButton["text"] = "BILDIRIM OFF"


GPIO.add_event_detect(36, GPIO.RISING, callback=gate_opened, bouncetime=1000) # Setup event on pin 36 rising edge
GPIO.add_event_detect(35, GPIO.RISING, callback=door_opened, bouncetime=1000) # Setup event on pin 36 rising edge

tick()
mainloop()
