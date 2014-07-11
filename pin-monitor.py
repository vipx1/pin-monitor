__author__ = 'Stephen Smith, vipx1 Development'
import os
import pathlib
import configparser
import datetime
from datetime import timedelta
from time import sleep
import argparse
import RPi.GPIO as GPIO
import emailer

config_file = '/etc/pin-monitor/pin-monitor.conf'
path = pathlib.Path(config_file)
if not path.exists():
    raise FileNotFoundError('Configuration file not found at Path: {0}\r\nCurrent working directory is {1}'
                            .format(path, os.path.dirname(os.path.realpath(__file__))))
config = configparser.RawConfigParser()
config._interpolation = configparser.ExtendedInterpolation()
# read config file
config.read(config_file)
# set mode in RPi.GPIO
GPIO.setmode(GPIO.BCM)
# Turn off warnings about pins being used already
GPIO.setwarnings(False)
# get pins from config
LED_01 = config.getint('GPIO', 'LED_01')
LED_02 = config.getint('GPIO', 'LED_02')
ALARM_CONTACT_01 = config.getint('GPIO', 'ALARM_CONTACT_01')
# give the config to the EmailClient class
ec = emailer.EmailClient(config)

# Pull up resistor, switch against ground!
GPIO.setup(ALARM_CONTACT_01, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set up outputs and reset any LED's that might be on
GPIO.setup(LED_01, GPIO.OUT)
GPIO.setup(LED_02, GPIO.OUT)
GPIO.output(LED_01, GPIO.LOW)
GPIO.output(LED_02, GPIO.LOW)

# Set valid time back one minute so first Alarm can be activated immediately after service start
alarm_time_stamp = datetime.datetime.now() - timedelta(0, 60)

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--exit', help="exit pin-monitor service", action="store_true")
parser.add_argument("-i", "--init", help='initiate pin-monitor service', action="store_true")
args = parser.parse_args()


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
        # If alarm contact is low and the time difference between now and last alarm is greater than 60 seconds..
        if GPIO.input(ALARM_CONTACT_01) == 0 and \
                        (datetime.datetime.now() - alarm_time_stamp).seconds > timedelta(0, 60).seconds:
            # Switch off flashing LED
            if GPIO.input(LED_01) == 1:
                GPIO.output(LED_01, GPIO.LOW)
            # reset alarm activation time stamp
            alarm_time_stamp = datetime.datetime.now()
            # Switch on second LED to show Pi is busy sending email
            GPIO.output(LED_02, GPIO.HIGH)
            # send an email
            ec.send_email_image_conf(ec)
            # Switch off second LED to show Pi is finished sending email
            GPIO.output(LED_02, GPIO.LOW)
            # have a rest :)
            sleep(1)
        # Flash LED fast while no new Alarm is possible
        while (datetime.datetime.now() - alarm_time_stamp).seconds < timedelta(0, 60).seconds:
            current_value = GPIO.input(LED_01)
            GPIO.output(LED_01, not current_value)
            sleep(0.15)

        # Normal operation, waiting for new Alarm
        current_value = GPIO.input(LED_01)
        GPIO.output(LED_01, not current_value)
        sleep(0.5)
except KeyboardInterrupt:
    clean_exit()
