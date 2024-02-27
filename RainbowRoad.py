import numpy as np
import cv2
from picamera2 import Picamera2
from libcamera import controls
import time
import RPi.GPIO as GPIO

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

# Set up pins as outputs
GPIO.setup(motor1_enable_pin, GPIO.OUT)
GPIO.setup(motor1_input1_pin, GPIO.OUT)
GPIO.setup(motor1_input2_pin, GPIO.OUT)

GPIO.setup(motor2_enable_pin, GPIO.OUT)
GPIO.setup(motor2_input1_pin, GPIO.OUT)
GPIO.setup(motor2_input2_pin, GPIO.OUT)

right = GPIO.PWM(motor1_enable_pin, 50)
left = GPIO.PWM(motor2_enable_pin, 50)
right.start(0)
left.start(0)

# Core camera setup
picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()
time.sleep(1)

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
    set_speed_right(20)

def left_wheel_forward():
    set_speed_left(20)

def motors_stop():
    set_speed_left(0)
    set_speed_right(0)

# Set both motors to move in opposite directions
def move_forward():
    motors_stop()
    print("Moving forward...")
    right_wheel_forward()
    left_wheel_forward()


def move_right():
    GPIO.output(motor2_enable_pin, GPIO.LOW)
    motors_stop()
    left_wheel_forward()

def move_left():
    GPIO.output(motor1_enable_pin, GPIO.LOW)
    motors_stop()
    right_wheel_forward()

try:
    set_motor_direction(motor1_enable_pin, motor1_input1_pin, motor1_input2_pin, 'forward')
    set_motor_direction(motor2_enable_pin, motor2_input1_pin, motor2_input2_pin, 'backward')

    while True:
        
        # Display camera input
        image = picam2.capture_array("main")
        cv2.imshow('img',image)
    
        # Crop the image
        #crop_img = image[60:120, 0:160]
        crop_img = image[100:400, 200:500]
    
        # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)
    
        # Color thresholding
        input_threshold,comp_threshold = cv2.threshold(blur,50,245,cv2.THRESH_BINARY_INV)
    
        # Find the contours of the frame
        contours,hierarchy = cv2.findContours(comp_threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
        # Find the biggest contour (if detected)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c) # determine moment - weighted average of intensities

            if int(M['m00']) != 0:
                cx = int(M['m10']/M['m00']) # find x component of centroid location
                cy = int(M['m01']/M['m00']) # find y component of centroid location
            else:
                print("Centroid calculation error, looping to acquire new values")
                continue
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1) # display vertical line at x value of centroid
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1) # display horizontal line at y value of centroid
    
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 2) # display green lines for all contours
            
            # determine location of centroid in x direction and adjust steering recommendation
            if cx >= 120:
                print("Turn Right!")
                move_right()
            if cx < 120 and cx > 50:
                print("On Track!")
                move_forward()
            if cx <= 50:
                print("Turn Left!")
                move_left()
        else:
            print("I don't see the line")
            motors_stop()
            set_motor_direction(motor1_enable_pin, motor1_input1_pin, motor1_input2_pin, 'backward')
            set_motor_direction(motor2_enable_pin, motor2_input1_pin, motor2_input2_pin, 'forward')
            move_forward()
            time.sleep(0.5)
            motors_stop
            set_motor_direction(motor1_enable_pin, motor1_input1_pin, motor1_input2_pin, 'forward')
            set_motor_direction(motor2_enable_pin, motor2_input1_pin, motor2_input2_pin, 'backward')
    
        # Display the resulting frame
        cv2.imshow('frame',crop_img)
        
        # Show image for 1 ms then continue to next image
        cv2.waitKey(1)

except KeyboardInterrupt:
    print('All done')
