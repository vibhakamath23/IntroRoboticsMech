import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)

# Motor right
motor1_enable_pin = 36
motor1_input1_pin = 38
motor1_input2_pin = 40

# Motor left
motor2_enable_pin = 11
motor2_input1_pin = 35
motor2_input2_pin = 37

# color sensor
s2 = 16
s3 = 18
sig = 22 #labeled "out" on your board
cycles = 10

# Set up pins as outputs
GPIO.setup(motor1_enable_pin, GPIO.OUT)
GPIO.setup(motor1_input1_pin, GPIO.OUT)
GPIO.setup(motor1_input2_pin, GPIO.OUT)

GPIO.setup(motor2_enable_pin, GPIO.OUT)
GPIO.setup(motor2_input1_pin, GPIO.OUT)
GPIO.setup(motor2_input2_pin, GPIO.OUT)

GPIO.setup(s2, GPIO.OUT)
GPIO.setup(s3, GPIO.OUT)
GPIO.setup(sig, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

right = GPIO.PWM(motor1_enable_pin, 50)
left = GPIO.PWM(motor2_enable_pin, 50)
right.start(0)
left.start(0)


def set_speed_left(speed):
    left.ChangeDutyCycle(speed)

def set_speed_right(speed):
    right.ChangeDutyCycle(speed)

# Function to set motor directions
def set_motor_direction(motor_enable_pin, input1_pin, input2_pin, direction):
    GPIO.output(motor_enable_pin, GPIO.HIGH)
    if direction == 'forward':
        GPIO.output(input1_pin, GPIO.HIGH)
        GPIO.output(input2_pin, GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(input1_pin, GPIO.LOW)
        GPIO.output(input2_pin, GPIO.HIGH)

def right_wheel_forward():
    set_speed_right(15)

def left_wheel_forward():
    set_speed_left(15)

def motors_stop():
    set_speed_left(0)
    set_speed_right(0)

# Set both motors to move in opposite directions
def move_forward(duration):
    print("Moving forward...")
    right_wheel_forward()
    left_wheel_forward()
    time.sleep(duration)
    motors_stop()

def move_right(duration):
    left_wheel_forward()
    time.sleep(duration)
    GPIO.output(motor2_enable_pin, GPIO.LOW)

def move_left(duration):
    right_wheel_forward()
    time.sleep(duration)
    GPIO.output(motor1_enable_pin, GPIO.LOW)

# Detect color
def DetectColor():
    global x1
    GPIO.output(s2, GPIO.LOW)  # Set s2 to LOW for red detection
    GPIO.output(s3, GPIO.LOW)  # Set s3 to LOW for red detection
    time.sleep(0.1)  # Wait for sensor stabilization
    start_time = time.time()  # Get current time
    for count in range(cycles):  # Loop for the specified number of cycles
        GPIO.wait_for_edge(sig, GPIO.FALLING)  # Wait for falling edge on sig pin
    duration = time.time() - start_time  # Calculate time taken for cycles
    red = cycles / duration  # Calculate red intensity
    print("red value - ", red)  # Print red intensity
     
    # Detect blue values
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.1)
    start_time = time.time()
    for count in range(cycles):
        GPIO.wait_for_edge(sig, GPIO.FALLING)
    duration = time.time() - start_time
    blue = cycles / duration
    print("blue value - ", blue)

    # Detect green values
    GPIO.output(s2, GPIO.HIGH)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.1)
    start_time = time.time()
    for count in range(cycles):
        GPIO.wait_for_edge(sig, GPIO.FALLING)
    duration = time.time() - start_time
    green = cycles / duration
    print("green value - ", green)

    return blue

def main():
    pl = 0
    try:
        set_motor_direction(motor1_enable_pin, motor1_input1_pin, motor1_input2_pin, 'forward')
        set_motor_direction(motor2_enable_pin, motor2_input1_pin, motor2_input2_pin, 'backward')

        while True:
            blue = DetectColor()
            print("blue intensity:", blue)
            if blue > 42000 and blue < 47000:  # If seeing the blue line
                move_forward(0.3)  # Move forward 
                pl = 1
                move = 0.3
            else:
                motors_stop()  # Stop if seeing white or another color
                # handle a crossroad first, then check right, then check left
                if pl == 1:
                    print("CROSSROAD")
                    #move_forward(0.1) # to get past a crossroad if there is one
                    motors_stop
                    pl = 2 
                    continue
                if pl == 2 and blue < 35000 and blue > 30000: # to the right of line
                    print("moving left", move)
                    move_left(move)
                    motors_stop
                    move = move + 0.1
                    pl = 3
                    continue
                if pl == 3 and blue > 35000 and blue < 40000: # to the left of line
                    print("moving right", move)
                    move_right(move)
                    motors_stop
                    pl = 2   
            time.sleep(0.1)  
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
