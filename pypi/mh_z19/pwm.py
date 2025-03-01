# -*- coding: utf-8 -*-
#
# © Takeyuki UEDA 2024 -
import time

# import RPi.GPIO as GPIO
from gpiozero import Button

# exception
class GPIO_Edge_Timeout(Exception):
  pass

'''
def read_from_pwm_with_gpio(gpio=12, range=5000):
  CYCLE_START_HIGHT_TIME = 2
  TIMEOUT = 2000 # must be larger than PWM cycle time.

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(gpio,GPIO.IN)

  # wait falling ¯¯|_ to see end of last cycle
  channel = GPIO.wait_for_edge(gpio, GPIO.FALLING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))

  # wait rising __|¯ to catch the start of this cycle
  channel = GPIO.wait_for_edge(gpio,GPIO.RISING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))
  else:
    rising = time.time() * 1000

  # wait falling ¯¯|_ again to catch the end of TH duration
  channel = GPIO.wait_for_edge(gpio, GPIO.FALLING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))
  else:
    falling = time.time() * 1000

  return {'co2': int(falling -rising - CYCLE_START_HIGHT_TIME) / 2 *(range/500)}
'''

# refer https://gpiozero.readthedocs.io/en/latest/migrating_from_rpigpio.html#input-devices
def read_from_pwm_with_gpiozero(gpio=12, range=5000):
  CYCLE_START_HIGHT_TIME = 2
  TIMEOUT = 2000 # must be larger than PWM cycle time.

  '''
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(gpio,GPIO.IN)
  '''
  btn = Button(gpio)

  # wait falling ¯¯|_ to see end of last cycle
  '''  
  channel = GPIO.wait_for_edge(gpio, GPIO.FALLING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))
  '''
  starting = time.time() * 1000
  btn.wait_for_press(2) # 2 sec for timeout because 1sec cycle of pwm
  last_falling = time.time() * 1000
  if last_falling - starting > 1000:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))

  # wait rising __|¯ to catch the start of this cycle
  '''
  channel = GPIO.wait_for_edge(gpio,GPIO.RISING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))
  else:
    rising = time.time() * 1000
  '''
  starting = time.time() * 1000
  btn.wait_for_release(2) # 2 sec for timeout because 1sec cycle of pwm
  rising   = time.time() * 1000
  if rising - starting > 1000:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))

  # wait falling ¯¯|_ again to catch the end of TH duration
  '''
  channel = GPIO.wait_for_edge(gpio, GPIO.FALLING, timeout=TIMEOUT)
  if channel is None:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))
  else:
    falling = time.time() * 1000
  '''
  starting = time.time() * 1000
  btn.wait_for_press(2) # 2 sec for timeout because 1sec cycle of pwm
  falling  = time.time() * 1000
  if falling - starting > 1000:
    raise GPIO_Edge_Timeout("gpio {} edge timeout".format(gpio))

  return {'co2': int(falling -rising - CYCLE_START_HIGHT_TIME) / 2 *(range/500)}
