import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from mh_z19 import version
from mh_z19.rpi_mh_z19b import RPi_MH_Z19B


def main():
    parser, args = parse_args()

    if hasattr(args, 'func'):
        # Execute the designated function
        getattr(args, 'func')(args)
    else:
        # Otherwise, print the help messages
        parser.print_help()


def parse_args():
    parser = ArgumentParser(
        description='Manipulate the MH-Z19B sensor installed on a Raspberry Pi'
    )
    subparsers = parser.add_subparsers(title='Available sub-commands')

    parser.add_argument(
        '-S', '--serial-file-path',
        action='store',
        help='The path of the serial file (e.g. /dev/ttyAMA1)\n'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='{}'.format(version))

    # Sub-command: read
    msg = 'Get CO2 sensor value from the specified serial file'
    read_subparser = subparsers.add_parser('read', description=msg, help=msg)
    read_subparser.set_defaults(func=read_sensor_value)

    # Sub-command: disable-sf
    msg = 'Disable self-calibration'
    disable_sf_subparser = subparsers.add_parser('disable-sf', description=msg, help=msg)
    disable_sf_subparser.set_defaults(func=disable_self_calibration)

    # Sub-command: enable-sf
    msg = 'Enable self-calibration'
    enable_sf_subparser = subparsers.add_parser('enable-sf', description=msg, help=msg)
    enable_sf_subparser.set_defaults(func=enable_self_calibration)

    # Sub-command: calibrate-span-point
    msg = 'Calibrate the sensor with the span point'
    calibrate_span_point_subparser = subparsers.add_parser(
        'calibrate-span-point',
        description=msg,
        help=msg)
    calibrate_span_point_subparser.add_argument(
        'span_point_value',
        action='store',
        metavar='SPAN_POINT_VALUE',
        type=int,
        help='Span point value')
    calibrate_span_point_subparser.set_defaults(func=calibrate_span_point)

    # Sub-command: calibrate-zero-point
    msg = 'Calibrate the sensor with the zero point'
    calibrate_zero_point_subparser = subparsers.add_parser(
        'calibrate-zero-point',
        description=msg,
        help=msg)
    calibrate_zero_point_subparser.set_defaults(func=calibrate_zero_point)

    # Sub-command: set-detection-range
    msg = 'Set detection range'
    set_detection_range_subparser = subparsers.add_parser(
        'set-detection-range',
        description=msg,
        formatter_class=RawTextHelpFormatter,
        help=msg)
    set_detection_range_subparser.add_argument(
        'max_range',
        action='store',
        metavar='M',
        type=int,
        help='Maximum range.\n'
             'It can be one of the following values: \n'
             '2000, 5000, 10000 (unit: ppm)')
    set_detection_range_subparser.set_defaults(func=set_detection_range)

    return parser, parser.parse_args()


def read_sensor_value(args):
    rpi_mh_z19_instance = RPi_MH_Z19B(args.serial_file_path, timeout=5)
    print('CO2 sensor value: {}'.format(rpi_mh_z19_instance.read_sensor_value()))


def disable_self_calibration(args):
    RPi_MH_Z19B.disable_self_calibration(args.serial_file_path)
    print('Disable self calibration')


def enable_self_calibration(args):
    RPi_MH_Z19B.enable_self_calibration(args.serial_file_path)
    print('Enable self calibration')


def calibrate_span_point(args):
    span_point_value = args.span_point_value

    if span_point_value >= (2 ** 16) or span_point_value < 0:
        print('Span point value is out of range, it should be in 0 ~ 65535')
        sys.exit(1)

    print('Call Calibration with SPAN point.')
    RPi_MH_Z19B.calibrate_span_point(span_point_value, args.serial_file_path)


def calibrate_zero_point(args):
    print('Call Calibration with ZERO point.')
    RPi_MH_Z19B.calibrate_zero_point(args.serial_file_path)


def set_detection_range(args):
    desired_range_max = args.max_range

    if desired_range_max == 2000:
        RPi_MH_Z19B.set_detection_range_2000(args.serial_file_path)
        print('Set Detection range as 2000')
    elif desired_range_max == 5000:
        RPi_MH_Z19B.set_detection_range_5000(args.serial_file_path)
        print('Set Detection range as 5000')
    elif desired_range_max == 10000:
        RPi_MH_Z19B.set_detection_range_10000(args.serial_file_path)
        print('Set Detection range as 10000')
    else:
        print('Range can only be one of the following values: 2000, 5000, 10000')
        sys.exit(1)
