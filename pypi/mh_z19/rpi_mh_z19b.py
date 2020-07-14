import itertools
import serial
import sys

from mh_z19 import const as CONST
from mh_z19 import utils


class RPi_MH_Z19B:
    __serial_file_path = ''
    __serial_object = None

    def __init__(self, serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH, **kwargs):
        self.__serial_file_path = serial_file_path
        self.__serial_object = self.__get_serial_object(serial_file_path)

    def __close__(self):
        self.__serial_object.close()

    @staticmethod
    def __get_serial_object(serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH,
                            **kwargs) -> serial.Serial:
        return serial.Serial(port=serial_file_path,
                             baudrate=CONST.BAUD_RATE,
                             bytesize=serial.EIGHTBITS,
                             parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE,
                             **kwargs)

    @classmethod
    def __send_one_shot_command(cls, serial_file_path: str, command_byte_sequence: bytes):
        serial_object = cls.__get_serial_object(serial_file_path)
        serial_object.write(command_byte_sequence)
        serial_object.close()

    @classmethod
    def enable_self_calibration(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.ENABLE_SELF_CALIBRATION_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def disable_self_calibration(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.DISABLE_SELF_CALIBRATION_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def set_detection_range_2000(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.SET_DETECTION_RANGE_2000_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def set_detection_range_5000(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.SET_DETECTION_RANGE_5000_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def set_detection_range_10000(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.SET_DETECTION_RANGE_10000_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def calibrate_zero_point(
        cls,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        cls.__send_one_shot_command(serial_file_path,
                                    CONST.CALIBRATE_ZERO_POINT_COMMAND_BYTE_SEQUENCE)

    @classmethod
    def calibrate_span_point(
        cls,
        span_point_value: int,
        serial_file_path: str = CONST.DEFAULT_SERIAL_FILE_PATH
    ) -> None:
        calibrate_span_point_command_byte_sequence = \
            bytes(itertools.chain(
                CONST.START_BYTE,
                CONST.RESERVED_BYTE,
                CONST.CALIBRATE_SPAN_POINT_COMMAND_BYTE,
                (span_point_value >> 8).to_bytes(1, 'big'),
                (span_point_value & 0xFF).to_bytes(1, 'big'),
                CONST.NONE_BYTE,
                CONST.NONE_BYTE,
                CONST.NONE_BYTE
            ))
        # Append the checksum
        calibrate_span_point_command_byte_sequence = \
            bytes(itertools.chain(
                calibrate_span_point_command_byte_sequence,
                utils.compute_checksum(list(calibrate_span_point_command_byte_sequence))
            ))
        cls.__send_one_shot_command(serial_file_path,
                                    calibrate_span_point_command_byte_sequence)

    def read_sensor_value(self) -> int or None:
        self.__serial_object.write(CONST.READ_COMMAND_BYTE_SEQUENCE)

        result_bytes = self.__serial_object.read(9)

        if len(result_bytes) >= 4 and \
           result_bytes[0] == int.from_bytes(CONST.START_BYTE, sys.byteorder) and \
           result_bytes[1] == int.from_bytes(CONST.READ_COMMAND_BYTE, sys.byteorder):
            return result_bytes[2] * 256 + result_bytes[3]
        else:
            return

    @property
    def serial_file_path(self) -> str:
        return self.serial_file_path

    @serial_file_path.setter
    def serial_file_path(self, serial_file_path: str):
        self.__serial_file_path = serial_file_path
