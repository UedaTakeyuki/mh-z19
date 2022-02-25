# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/mh_z19.py
#
# © Takeyuki UEDA 2015 -

import serial
import time
import subprocess
import traceback
import getrpimodel
import struct
import platform
import argparse
import sys
import json
import os.path

import RPi.GPIO as GPIO

# setting
version = "3.1.3"
pimodel        = getrpimodel.model()
pimodel_strict = getrpimodel.model_strict()
retry_count    = 3

# exception
class GPIO_Edge_Timeout(Exception):
  pass

if os.path.exists('/dev/serial0'):
  partial_serial_dev = 'serial0'
elif pimodel == "3 Model B" or pimodel == "4 Model B" or pimodel_strict == "Zero W":
  partial_serial_dev = 'ttyS0'
else:
  partial_serial_dev = 'ttyAMA0'

serial_dev = '/dev/%s' % partial_serial_dev
#stop_getty = 'sudo systemctl stop serial-getty@%s.service' % partial_serial_dev
#start_getty = 'sudo systemctl start serial-getty@%s.service' % partial_serial_dev

# major version of running python
p_ver = platform.python_version_tuple()[0]

def start_getty():
  start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(start_getty)

def stop_getty():
  stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(stop_getty)

def set_serialdevice(serialdevicename):
  global serial_dev
  serial_dev = serialdevicename

def connect_serial():
  return serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)

def read_concentration():
  try:
    ser = connect_serial()
    for retry in range(retry_count):
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)

      if p_ver == '2':
        if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86" and checksum(s[1:-1]) == s[-1]:
          return ord(s[2])*256 + ord(s[3])
      else:
        if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86 and ord(checksum(s[1:-1])) == s[-1]:
          return s[2]*256 + s[3]
  except:
     traceback.print_exc()
  return ""

def mh_z19():
  co2 = read_concentration()
  if not co2:
    return {}
  else:
    return {'co2': co2}

def read(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()

  result = mh_z19()

  if not serial_console_untouched:
    start_getty()
  return result

def read_co2valueonly(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()

  result = read_concentration()

  if not serial_console_untouched:
    start_getty()
  return result

def read_all(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  try:
    ser = connect_serial()
    for retry in range(retry_count):
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)

      if p_ver == '2':
        if len(s) >= 9 and s[0] == "\xff" and s[1] == "\x86" and checksum(s[1:-1]) == s[-1]:
          return {'co2': ord(s[2])*256 + ord(s[3]),
                  'temperature': ord(s[4]) - 40,
                  'TT': ord(s[4]),
                  'SS': ord(s[5]),
                  'UhUl': ord(s[6])*256 + ord(s[7])
                  }
        break
      else:
        if len(s) >= 9 and s[0] == 0xff and s[1] == 0x86 and ord(checksum(s[1:-1])) == s[-1]:
          return {'co2': s[2]*256 + s[3],
                  'temperature': s[4] - 40,
                  'TT': s[4],
                  'SS': s[5],
                  'UhUl': s[6]*256 + s[7]
                  }
  except:
     traceback.print_exc()

  if not serial_console_untouched:
    start_getty()
  return {}

def abc_on(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  result=ser.write(b"\xff\x01\x79\xa0\x00\x00\x00\x00\xe6")
  ser.close()
  if not serial_console_untouched:
    start_getty()

def abc_off(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  result=ser.write(b"\xff\x01\x79\x00\x00\x00\x00\x00\x86")
  ser.close()
  if not serial_console_untouched:
    start_getty()

def span_point_calibration(span, serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  if p_ver == '2':
    b3 = span / 256;
  else:
    b3 = span // 256;   
  byte3 = struct.pack('B', b3)
  b4 = span % 256; byte4 = struct.pack('B', b4)
  c = checksum([0x01, 0x88, b3, b4])
  request = b"\xff\x01\x88" + byte3 + byte4 + b"\x00\x00\x00" + c
  result = ser.write(request)
  ser.close()
  if not serial_console_untouched:
    start_getty()

def zero_point_calibration(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  request = b"\xff\x01\x87\x00\x00\x00\x00\x00\x78"
  result = ser.write(request)
  ser.close()
  if not serial_console_untouched:
    start_getty()

def detection_range_10000(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  request = b"\xff\x01\x99\x00\x00\x00\x27\x10\x2F"
  result = ser.write(request)
  ser.close()
  if not serial_console_untouched:
    start_getty()

def detection_range_5000(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  request = b"\xff\x01\x99\x00\x00\x00\x13\x88\xcb"
  result = ser.write(request)
  ser.close()
  if not serial_console_untouched:
    start_getty()

def detection_range_2000(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  ser = connect_serial()
  request = b"\xff\x01\x99\x00\x00\x00\x07\xd0\x8F"
  result = ser.write(request)
  ser.close()
  if not serial_console_untouched:
    start_getty()

def read_from_pwm(gpio=12, range=5000):
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

def checksum(array):
  if p_ver == '2' and isinstance(array, str):
    array = [ord(c) for c in array]
  csum = sum(array) % 0x100
  if csum == 0:
    return struct.pack('B', 0)
  else:
    return struct.pack('B', 0xff - csum + 1)

if __name__ == '__main__':
#  value = read()
#  print (value)
  parser = argparse.ArgumentParser(
    description='''return CO2 concentration as object as {'co2': 416}''',
  )
  parser.add_argument("--serial_device",
                      type=str,
                      help='''Use this serial device file''')

  parser.add_argument("--serial_console_untouched",
                      action='store_true',
                      help='''Don't close/reopen serial console before/after sensor reading''')


  group = parser.add_mutually_exclusive_group()

  group.add_argument("--version",
                      action='store_true',
                      help='''show version''')
  group.add_argument("--all",
                      action='store_true',
                      help='''return all (co2, temperature, TT, SS and UhUl) as json''')
  group.add_argument("--co2valueonly",
                      action='store_true',
                      help='''return co2 value alone, as unlabeled string''')
  group.add_argument("--abc_on",
                      action='store_true',
                      help='''Set ABC functionality on model B as ON.''')
  group.add_argument("--abc_off",
                      action='store_true',
                      help='''Set ABC functionality on model B as OFF.''')
  
  parser.add_argument("--span_point_calibration",
                      type=int,
                      metavar="span",
                      help='''Call calibration function with SPAN point''')
  parser.add_argument("--zero_point_calibration",
                      action='store_true',
                      help='''Call calibration function with ZERO point''')
  parser.add_argument("--detection_range_10000",
                      action='store_true',
                      help='''Set detection range as 10000''')
  parser.add_argument("--detection_range_5000",
                      action='store_true',
                      help='''Set detection range as 5000''')
  parser.add_argument("--detection_range_2000",
                      action='store_true',
                      help='''Set detection range as 2000''')

  parser.add_argument("--pwm",
                      action='store_true',
                      help='''Read CO2 concentration from PWM, see also `--pwm_range` and/or `--pwm_gpio`''')

  parser.add_argument("--pwm_range",
                      type=int,
                      choices=[2000,5000,10000],
                      default=5000,
                      metavar="range",
                      help='''with --pwm, use this to compute co2 concentration, default is 5000''')

  parser.add_argument("--pwm_gpio",
                      type=int,
                      default=12,
                      metavar="gpio(BCM)",
                      help='''with --pwm, read from this gpio pin on RPi, default is 12''')

  args = parser.parse_args()

  if args.serial_device is not None:
    set_serialdevice(args.serial_device)

  if args.abc_on:
    abc_on(args.serial_console_untouched)
    print ("Set ABC logic as on.")
  elif args.abc_off:
    abc_off(args.serial_console_untouched)
    print ("Set ABC logic as off.")
  elif args.span_point_calibration is not None:
    span_point_calibration(args.span_point_calibration, args.serial_console_untouched)
    print ("Call Calibration with SPAN point.")
  elif args.zero_point_calibration:
    print ("Call Calibration with ZERO point.")
    zero_point_calibration(args.serial_console_untouched)
  elif args.detection_range_10000:
    detection_range_10000(args.serial_console_untouched)
    print ("Set Detection range as 10000.")
  elif args.detection_range_5000:
    detection_range_5000(args.serial_console_untouched)
    print ("Set Detection range as 5000.")
  elif args.detection_range_2000:
    detection_range_2000(args.serial_console_untouched)
    print ("Set Detection range as 2000.")
  elif args.pwm:
    print (read_from_pwm(gpio=args.pwm_gpio, range=args.pwm_range))
  elif args.version:
    print (version)
  elif args.all:
    value = read_all(args.serial_console_untouched)
    print (json.dumps(value))
  elif args.co2valueonly:
    value = read_co2valueonly(args.serial_console_untouched)
    print (value)
  else:
    value = read(args.serial_console_untouched)
    print (json.dumps(value))

  sys.exit(0)
