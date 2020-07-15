import getrpimodel
import struct

from pathlib import Path


def compute_checksum(array: list):
    return struct.pack('B', 0xff - (sum(array) % 0x100) + 1)


def get_default_serial_file_path() -> str:
    pi_model = getrpimodel.model()
    pi_model_strict = getrpimodel.model_strict()

    if Path('/dev/serial0').resolve().exists():
        return '/dev/serial0'
    elif pi_model == '3 Model B' or pi_model_strict == 'Zero W':
        return '/dev/ttyS0'
    else:
        return '/dev/ttyAMA0'
