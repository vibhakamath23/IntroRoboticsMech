import RPi.GPIO as GPIO
import time

# GLOBALS
OUT1 = 12 #red
OUT2 = 11 #yellow
OUT3 = 13 #green
OUT4 = 15  #grey

GPIO.setmode(GPIO.BOARD)

# Stepper Motor Output
GPIO.setup(OUT1, GPIO.OUT)
GPIO.setup(OUT2, GPIO.OUT)
GPIO.setup(OUT3, GPIO.OUT)
GPIO.setup(OUT4, GPIO.OUT)

GPIO.output(OUT1,GPIO.LOW)
GPIO.output(OUT2,GPIO.LOW)
GPIO.output(OUT3,GPIO.LOW)
GPIO.output(OUT4,GPIO.LOW)

def ForwardMotor(num_steps, step_delay):
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
    time.sleep(3)
    ForwardMotor(25, 0.03)
    time.sleep(2) #stop at the top of the flagpole before Mario's descent

    ReverseMotor(25, 0.03)
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
