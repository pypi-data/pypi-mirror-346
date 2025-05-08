"""
Please make sure the button is connected to the correct pins.
The following table describes how to connect the button to the 40-pin header.
-----------------------------------------
_______button____Pin Number_____Pin Name
    one end          37          GPIO60
  The other end      39            GND
-----------------------------------------
"""

import VisionFive.gpio as GPIO
import sys
import time

key_pin = 37


# The callback function for edge detection
def detect(pin, edge_type):
    if 1 == edge_type:
        print("*-----------------------------------*")
        print("Rising edge is detected on pin {} !".format(pin))
    elif 2 == edge_type:
        print("*-----------------------------------*")
        print("Falling edge is detected on pin {} !".format(pin))
    print()


def main():
    # Set the gpio mode as 'BOARD'.
    GPIO.setmode(GPIO.BOARD)
    
    # Configure the direction of key_pin as input.
    GPIO.setup(key_pin, GPIO.IN)

    # A falling edge detection event is added to key_pin, also set bouncetime(unit: millisecond) to avoid jitter
    GPIO.add_event_detect(key_pin, GPIO.FALLING, callback=detect, bouncetime=2)

    print("Wait 5 seconds")
    time.sleep(5)
    
    # Query if edge event happens
    edge_detected = GPIO.event_detected(key_pin)
    
    if edge_detected:
        print("The falling edge is detected on pin{}!".format(key_pin))
    else:
        print("The rising edge failed to be detected on the pin{}!".format(key_pin))
    
    # Remove detection for edge event
    GPIO.remove_event_detect(key_pin)
    
    # Both edge rising and falling can be detected, also set bouncetime(unit: millisecond) to avoid jitter
    print("Both rising and falling edge detection event are added to pin {}.".format(key_pin))
    GPIO.add_event_detect(key_pin, GPIO.BOTH, callback=detect, bouncetime=2)
    
    print("Please press the key on pin {} once at any time!".format(key_pin))

    while True:
        time.sleep(1)
        if GPIO.event_detected(key_pin):
            print("Exit demo program")
            GPIO.cleanup()
            break

if __name__ == "__main__":
    sys.exit(main())
