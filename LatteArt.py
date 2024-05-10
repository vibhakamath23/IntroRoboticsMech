import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BOARD)

# Set the GPIO pin for the transistor
transistor_pin = 11
GPIO.setup(transistor_pin, GPIO.OUT)

# Define/setup GPIO pins for motor control
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pins for the L298N motor driver
OUT1 = 37
OUT2 = 35
OUT3 = 33
OUT4 = 31

# Set the GPIO pins as output
GPIO.setup(OUT1, GPIO.OUT)
GPIO.setup(OUT2, GPIO.OUT)
GPIO.setup(OUT3, GPIO.OUT)
GPIO.setup(OUT4, GPIO.OUT)

GPIO.output(OUT1,GPIO.LOW)
GPIO.output(OUT2,GPIO.LOW)
GPIO.output(OUT3,GPIO.LOW)
GPIO.output(OUT4,GPIO.LOW)

# AIRTABLE DATA
URL = 'https://api.airtable.com/v0/appZXeS3vQKy6x41E/Drive'
# Format: {'Authorization':'Bearer Access_Token'}
Headers = {'Authorization':'Bearer patnz4q3YD2b6QE5b.c888c6f15cb3bbb30c73cb0bcd9b186c09f7459d2e0569c8f80a34dd45a8651b'}

'''
FUNCTION: thumper()
turns solenoid on and off using transistor pin
'''

def thumper():
    # Turn on the transistor (solenoid on)
    GPIO.output(transistor_pin, GPIO.HIGH)
    print("Transistor turned ON")
    time.sleep(0.1)  # Wait for 2 seconds
    
    # Turn off the transistor (solenoid off)
    GPIO.output(transistor_pin, GPIO.LOW)
    print("Transistor turned OFF")
    time.sleep(0.1)  # Wait for 2 seconds

'''
FUNCTION: turnStencil()
turns solenoid on and off using transistor pin
'''

def turnStencil(direction, steps, step_delay):
    if direction == "clockwise":
        print("turning clockwise...")
        current_step = 0
        for _ in range(steps):
            if current_step == 0:
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
            elif current_step == 3:
                GPIO.output(OUT1,GPIO.HIGH)
                GPIO.output(OUT2,GPIO.LOW)
                GPIO.output(OUT3,GPIO.LOW)
                GPIO.output(OUT4,GPIO.HIGH)
                time.sleep(step_delay)
            if current_step == 3:
                current_step = 0
                continue 
            current_step = current_step + 1

    if direction == "counterclockwise": 
        print("turning counterclockwise...")
        current_step = 0
        for _ in range(steps):
            if current_step == 0:
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
            elif current_step == 3:
                GPIO.output(OUT1,GPIO.HIGH)
                GPIO.output(OUT2,GPIO.LOW)
                GPIO.output(OUT3,GPIO.HIGH)
                GPIO.output(OUT4,GPIO.LOW)
                time.sleep(step_delay)
            if current_step == 3:
                current_step = 0
                continue 
            current_step = current_step + 1
    
    return steps

'''
FUNCTION: processAndRunStencil()
- takes in a stencil selection as a parameter and turns a predefined amount
- returns steps as a parameter to be used for restoration
'''

def processAndRunStencil(stencil):
    print(stencil)
    if stencil == 'ShyGuy':
        steps = turnStencil('clockwise', 80, 0.03) # CHANGE STEPS AS NEEDED FOR ALL
    if stencil == 'Kirby':
        steps = turnStencil('clockwise', 40, 0.03)
    if stencil == 'Mario':
        steps = turnStencil('clockwise', 120, 0.03)
    return steps
    
'''
FUNCTION: restoreStencil()
- takes in turnAmount of steps returned by processAndRunStencil() in main()
- subtracts how much stencil turned to make the design to turn back to start 
'''

def restoreStencil(turnAmount):
    fullRound = 200 # REPLACE THIS WITH WHAT A FULL ROTATION NEEDS IN STEPS
    restoreTurn = fullRound - turnAmount
    turnStencil('clockwise', restoreTurn, 0.03)

'''
FUNCTION: retrieveDesignInfo()
- accesses airtable fields for design
- takes parameter to return either arrival or design info
'''

def retrieveDesignInfo(field):
    r = requests.get(url = URL, headers = Headers, params = {})
    data = r.json()

    design_info = {
            'design':   data['records'][0]['fields']['Design'],
            'arrived':  data['records'][0]['fields']['Arrived at station'], 
            'done':     data['records'][0]['fields']['Done']
        }

    if field == 'arrived':
        return (design_info['arrived'])
    elif field == 'design':
        return (design_info['design'])

'''
FUNCTION: publishCompletionInfo()
- updates airtable saying we're done
- transport team will reset our values to 0!
'''

def publishCompletionInfo():
    design_info = {
        "fields": {
            "Arrived at station": 1,
            "Done": 1,
            #"Design": "Done",
        }
    }

    update_url = 'https://api.airtable.com/v0/appZXeS3vQKy6x41E/Drive/recJQILiP3Ls6Cy5G'
    # Make the PATCH request
    response = requests.patch(update_url, json=design_info, headers=Headers)

'''
FUNCTION: main()
- once latte has arrived, turn to correct stencil, dispense cinnamon, restore
the stencil, and update the airtable correctly
'''

def main():
    try:

        while True:
            latteArrived = retrieveDesignInfo("arrived")
            if latteArrived == 1:
  
                print("Latte has arrived at the design station!")
                time.sleep(1)

                # TURN TO DESIRED STENCIL
                stencil = retrieveDesignInfo('design')
                #stencil = stencil.split()[0]
                stencil = stencil.replace(" ", "").replace("\n", "")
                print("selecting", stencil, "stencil...")
                stencil = ''.join(char for char in stencil if not char.isdigit()) # Remove all digits
                turnAmount = processAndRunStencil(stencil)
                time.sleep(1)
            
                # THUMP CINNAMON
                print("dispensing cinnamon...")
                thumper()
                time.sleep(1)

                # TURN STENCIL BACK
                print("turning stencil back...")
                restoreStencil(turnAmount)
                time.sleep(1)

                # PUBLISH THAT WE'RE DONE TO AIRTABLE & RESET ARRIVAL FIELD
                print("updating airtable...")
                publishCompletionInfo()
                time.sleep(7)

            else:
                print("Latte has not arrived.")

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
    GPIO.cleanup()
