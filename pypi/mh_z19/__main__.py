# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/mh_z19.py
#
# © Takeyuki UEDA 2015 -
import sys
import argparse
import json
import mh_z19.__init__ as mh_z19
#import __init__ as mh_z19

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
  mh_z19.set_serialdevice(args.serial_device)

#print(args.serial_console_untouched)

if args.abc_on:
  mh_z19.abc_on(args.serial_console_untouched)
  print ("Set ABC logic as on.")
elif args.abc_off:
  mh_z19.abc_off(args.serial_console_untouched)
  print ("Set ABC logic as off.")
elif args.span_point_calibration is not None:
  mh_z19.span_point_calibration(args.span_point_calibration, args.serial_console_untouched)
  print ("Call Calibration with SPAN point.")
elif args.zero_point_calibration:
  print ("Call Calibration with ZERO point.")
  mh_z19.zero_point_calibration(args.serial_console_untouched)
elif args.detection_range_10000:
  mh_z19.detection_range_10000(args.serial_console_untouched)
  print ("Set Detection range as 10000.")
elif args.detection_range_5000:
  mh_z19.detection_range_5000(args.serial_console_untouched)
  print ("Set Detection range as 5000.")
elif args.detection_range_2000:
  mh_z19.detection_range_2000(args.serial_console_untouched)
  print ("Set Detection range as 2000.")
elif args.pwm:
  print mh_z19.read_from_pwm(gpio=args.pwm_gpio, range=args.pwm_range, )
elif args.version:
  print (mh_z19.version)
elif args.all:
  value = mh_z19.read_all(args.serial_console_untouched)
  print (json.dumps(value))
else:
  value = mh_z19.read(args.serial_console_untouched)
  print (json.dumps(value))

sys.exit(0)