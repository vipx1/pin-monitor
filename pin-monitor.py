__author__ = 'Stephen Smith, SKS Communications Limited'

import datetime
from datetime import timedelta
from time import sleep
from modules import emailer
import argparse
import RPi.GPIO as GPIO

# <editor-fold desc="Hardware Config">

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_01 = 4
LED_02 = 23
SWITCH_01 = 24

# Pull up resistor, switch against ground!
GPIO.setup(SWITCH_01, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set up outputs
GPIO.setup(LED_01, GPIO.OUT)
GPIO.setup(LED_02, GPIO.OUT)
GPIO.output(LED_01, GPIO.LOW)
GPIO.output(LED_02, GPIO.LOW)

# </editor-fold>

# Set valid time back one minute so first alarm can be activated immediately after service start
valid_alarm_time_stamp = datetime.datetime.now() - timedelta(0, 60)

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--exit', help="exit pin-monitor service", action="store_true")
parser.add_argument("-i", "--init", help='initiate pin-monitor service', action="store_true")
args = parser.parse_args()

ec = emailer.EmailClient()


def clean_exit():
    GPIO.output(LED_01, GPIO.LOW)
    GPIO.output(LED_02, GPIO.LOW)
    GPIO.cleanup()
    print('GPIO.cleanup in pin-monitor service')
    quit()


try:
    while 1:
        if args.exit:
            clean_exit()
        if GPIO.input(SWITCH_01) == 0 and \
                        (datetime.datetime.now() - valid_alarm_time_stamp).seconds > timedelta(0, 60).seconds:
            # Switch off flashing LED
            if GPIO.input(LED_01) == 1:
                GPIO.output(LED_01, GPIO.LOW)

            valid_alarm_time_stamp = datetime.datetime.now()
            GPIO.output(LED_02, GPIO.HIGH)
            ec.send_email_image_conf(ec)
            GPIO.output(LED_02, GPIO.LOW)
            sleep(1)
        # Flash LED fast while no new Alarm is possible
        while (datetime.datetime.now() - valid_alarm_time_stamp).seconds < timedelta(0, 60).seconds:
            current_value = GPIO.input(LED_01)
            GPIO.output(LED_01, not current_value)
            sleep(0.15)

        current_value = GPIO.input(LED_01)
        GPIO.output(LED_01, not current_value)
        sleep(0.5)
except KeyboardInterrupt:
    clean_exit()
