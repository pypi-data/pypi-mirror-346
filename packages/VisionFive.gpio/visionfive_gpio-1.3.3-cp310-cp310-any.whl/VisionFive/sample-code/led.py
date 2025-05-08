"""
Please make sure the LED is connected to the correct pins.
The following table describes how to connect the LED to the 40-pin header.
-----------------------------------------
_______LED_________Pin Number_____Pin Name
    Positive          22          GPIO50
    Negative          6            GND
-----------------------------------------
"""

import VisionFive.gpio as GPIO
import time

led_pin = 22
# Set the gpio mode as 'BOARD'.
GPIO.setmode(GPIO.BOARD)
# Configure the direction of led_pin as output.
GPIO.setup(led_pin, GPIO.OUT)


def light(delay):
    # Configure the voltage level of led_pin as high.
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(delay)
    # Configure the voltage level of led_pin as low.
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(delay)


if __name__ == "__main__":
    try:
        delay_s = input("Enter delay(seconds): ")
        delay = float(delay_s)

        while True:
            try:
                light(delay)
            except KeyboardInterrupt:
                break
    finally:
        GPIO.cleanup()