import RPi.GPIO as GPIO
import time

# GLOBALS
OUT1 = 12 #red
OUT2 = 11 #yellow
OUT3 = 13 #green
OUT4 = 15  #grey
SW_IN = 18

triggerHit = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SW_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Stepper Motor Output
GPIO.setup(OUT1, GPIO.OUT)
GPIO.setup(OUT2, GPIO.OUT)
GPIO.setup(OUT3, GPIO.OUT)
GPIO.setup(OUT4, GPIO.OUT)

GPIO.output(OUT1,GPIO.LOW)
GPIO.output(OUT2,GPIO.LOW)
GPIO.output(OUT3,GPIO.LOW)
GPIO.output(OUT4,GPIO.LOW)


def printTrig(x):
    print("trigger")
    global triggerHit
    triggerHit = True


def ForwardMotor(num_steps, step_delay):
    global triggerHit
    triggerHit = False
    current_step = 0
    for x in range(num_steps):
        if triggerHit:
            return
        elif current_step == 0:
            GPIO.output(OUT1,GPIO.HIGH)
            GPIO.output(OUT2,GPIO.LOW)
            GPIO.output(OUT3,GPIO.HIGH)
            GPIO.output(OUT4,GPIO.LOW)
            time.sleep(step_delay)
            #print("step 0")
        elif current_step == 1:
            GPIO.output(OUT1,GPIO.LOW)
            GPIO.output(OUT2,GPIO.HIGH)
            GPIO.output(OUT3,GPIO.HIGH)
            GPIO.output(OUT4,GPIO.LOW)
            time.sleep(step_delay)
            #print("step 1")
        elif current_step == 2:
            GPIO.output(OUT1,GPIO.LOW)
            GPIO.output(OUT2,GPIO.HIGH)
            GPIO.output(OUT3,GPIO.LOW)
            GPIO.output(OUT4,GPIO.HIGH)
            time.sleep(step_delay)
            #print("step 2")
        elif current_step == 3:
            GPIO.output(OUT1,GPIO.HIGH)
            GPIO.output(OUT2,GPIO.LOW)
            GPIO.output(OUT3,GPIO.LOW)
            GPIO.output(OUT4,GPIO.HIGH)
            time.sleep(step_delay)
            #print("step 3")
        if current_step == 3:
            current_step = 0
            continue 
        current_step = current_step + 1

def ReverseMotor(num_steps, step_delay):
    global triggerHit
    triggerHit = False
    current_step = 0
    for x in range(num_steps):
        if triggerHit:
            return
        elif current_step == 0:
            GPIO.output(OUT1,GPIO.HIGH)
            GPIO.output(OUT2,GPIO.LOW)
            GPIO.output(OUT3,GPIO.LOW)
            GPIO.output(OUT4,GPIO.HIGH)
            time.sleep(step_delay)
            #print("step 0")
        elif current_step == 1:
            GPIO.output(OUT1,GPIO.LOW)
            GPIO.output(OUT2,GPIO.HIGH)
            GPIO.output(OUT3,GPIO.LOW)
            GPIO.output(OUT4,GPIO.HIGH)
            time.sleep(step_delay)
            #print("step 1")
        elif current_step == 2:
            GPIO.output(OUT1,GPIO.LOW)
            GPIO.output(OUT2,GPIO.HIGH)
            GPIO.output(OUT3,GPIO.HIGH)
            GPIO.output(OUT4,GPIO.LOW)
            time.sleep(step_delay)
            #print("step 2")
        elif current_step == 3:
            GPIO.output(OUT1,GPIO.HIGH)
            GPIO.output(OUT2,GPIO.LOW)
            GPIO.output(OUT3,GPIO.HIGH)
            GPIO.output(OUT4,GPIO.LOW)
            time.sleep(step_delay)
            #print("step 3")
        if current_step == 3:
            current_step = 0
            continue 
        current_step = current_step + 1
try:
    #GPIO.add_event_detect(SW_IN, GPIO.RISING, callback=printTrig, bouncetime=200)
    time.sleep(3)
    ForwardMotor(25, 0.03)
    time.sleep(2)

    ReverseMotor(25, 0.03)
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
