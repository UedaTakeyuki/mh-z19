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
group = parser.add_mutually_exclusive_group()
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
                    help='''Call calibration function with SPAN point''')
parser.add_argument("--zero_point_calibration",
                    action='store_true',
                    help='''Call calibration function with ZERO point''')
parser.add_argument("--detection_range_5000",
                    action='store_true',
                    help='''Set detection range as 5000''')
parser.add_argument("--detection_range_2000",
                    action='store_true',
                    help='''Set detection range as 2000''')

args = parser.parse_args()

if args.abc_on:
  mh_z19.abc_on()
  print ("Set ABC logic as on.")
elif args.abc_off:
  mh_z19.abc_off()
  print ("Set ABC logic as off.")
elif args.span_point_calibration is not None:
  mh_z19.span_point_calibration(args.span_point_calibration)
  print ("Call Calibration with SPAN point.")
elif args.zero_point_calibration:
  mh_z19.zero_point_calibration()
  print ("Call Calibration with ZERO point.")
elif args.detection_range_5000:
  mh_z19.detection_range_5000()
  print ("Set Detection range as 5000.")
elif args.detection_range_2000:
  mh_z19.detection_range_2000()
  print ("Set Detection range as 2000.")
elif args.all:
  value = mh_z19.read_all()
  print (json.dumps(value))
else:
  value = mh_z19.read()
  print (json.dumps(value))

sys.exit(0)