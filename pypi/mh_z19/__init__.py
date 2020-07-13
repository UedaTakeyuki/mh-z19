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
import os.path

from mh_z19.const import VERSION as __version__

# setting
version = '{}.{}.{}'.format(*__version__)
pimodel        = getrpimodel.model
pimodel_strict = getrpimodel.model_strict()

if os.path.exists('/dev/serial0'):
  partial_serial_dev = 'serial0'
elif pimodel == "3 Model B" or pimodel_strict == "Zero W":
  partial_serial_dev = 'ttyS0'
else:
  partial_serial_dev = 'ttyAMA0'
  
serial_dev = '/dev/%s' % partial_serial_dev
#stop_getty = 'sudo systemctl stop serial-getty@%s.service' % partial_serial_dev
#start_getty = 'sudo systemctl start serial-getty@%s.service' % partial_serial_dev
#start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
#stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]

# major version of running python
p_ver = platform.python_version_tuple()[0]

def start_getty():
#  p = subprocess.call(start_getty, stdout=subprocess.PIPE, shell=True)
  start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(start_getty)

def stop_getty():
#  p = subprocess.call(stop_getty, stdout=subprocess.PIPE, shell=True)
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

def mh_z19():
  try:
    ser = connect_serial()
    while 1:
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)

      if p_ver == '2':
        if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86":
          return {'co2': ord(s[2])*256 + ord(s[3])}
        break
      else:
        if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86:
          return {'co2': s[2]*256 + s[3]}
        break
  except:
     traceback.print_exc()

def read(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()

  result = mh_z19()

  if not serial_console_untouched:
    start_getty()
  if result is not None:
    return result

def read_all(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()
  try:
    ser = connect_serial()
    while 1:
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)

      if p_ver == '2':
        if len(s) >= 9 and s[0] == "\xff" and s[1] == "\x86":
          return {'co2': ord(s[2])*256 + ord(s[3]),
                  'temperature': ord(s[4]) - 40,
                  'TT': ord(s[4]),
                  'SS': ord(s[5]),
                  'UhUl': ord(s[6])*256 + ord(s[7])
                  }
        break
      else:
        if len(s) >= 9 and s[0] == 0xff and s[1] == 0x86:
          return {'co2': s[2]*256 + s[3],
                  'temperature': s[4] - 40,
                  'TT': s[4],
                  'SS': s[5],
                  'UhUl': s[6]*256 + s[7]
                  }
        break
  except:
     traceback.print_exc()

  if not serial_console_untouched:
    start_getty()
  if result is not None:
    return result

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

def checksum(array):
  return struct.pack('B', 0xff - (sum(array) % 0x100) + 1)
