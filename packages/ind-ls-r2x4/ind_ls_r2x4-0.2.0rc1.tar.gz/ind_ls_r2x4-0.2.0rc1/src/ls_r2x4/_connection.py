import threading
import time
import logging
import platform
import struct
import serial.tools.list_ports

from serial import Serial
from typing import Union
from cobs import cobs

logger = logging.getLogger(__name__)


class Connection:
    """
    Industrialise LS communication class over Serial/UART binary protocol.
    """
    MESSAGE_GET_INFO = 0x0000
    MESSAGE_ECHO = 0x0001
    MESSAGE_CONTROL_RD = 0x0002
    MESSAGE_CONTROL_WR = 0x0003
    MESSAGE_STATUS_RD = 0x0004
    MESSAGE_REBOOT_LS = 0x000f
    MESSAGE_TEC_PID_SETPOINT_RD = 0x000c
    MESSAGE_ADC_READ = 0x0020
    MESSAGE_ADC_READ_RAW = 0x0021
    MESSAGE_TEMP_READ = 0x0022
    MESSAGE_FAN_TACH_READ = 0x0023
    MESSAGE_LED_GET_CH_POWER = 0x0102
    MESSAGE_LED_SET_CH_CALIB_POWER = 0x0106
    MESSAGE_CPLD_SEND_SW_TRIGGER = 0x0200
    MESSAGE_CPLD_RESET_PULSE_STATE = 0x0201
    MESSAGE_CPLD_CONFIG_TRIGGER_MODE = 0x0202
    MESSAGE_CPLD_CONFIG_EXT_TRIGGER = 0x0203
    MESSAGE_CPLD_CONFIG_TRIGGER_PULSE = 0x0204
    MESSAGE_CPLD_CONFIG_TRIGGER_FILTER = 0x0205
    MESSAGE_CPLD_CONFIG_TRIGGER_OUTPUT = 0x0206
    MESSAGE_CPLD_SET_LDAC = 0x0207
    MESSAGE_I2C_RD = 0x8000
    MESSAGE_I2C_WR = 0x8001
    MESSAGE_I2C_WR_R_RD = 0x8002
    MESSAGE_ERROR = 0xe000

    RETRIES = 3
    SERIAL_TIMEOUT_IN_S = 2

    def __init__(self, serial_name=None):
        """
        Create a connection to the device

        :param serial_name: The name of the serial port to connect to. Leave none to auto-detect.
        """
        self.lock = threading.Lock()
        if serial_name is None:
            serial_name, _ = self._auto_detect_serial()
            if serial_name is None:
                raise ValueError("No 'Lightsource VCP' serial port found")
        self.serial_name = serial_name
        self.ser = Serial(serial_name, 115200, timeout=Connection.SERIAL_TIMEOUT_IN_S)
        self.ser.read_all()
        self._ls_info = self.get_info()
        self.serial_number = self._ls_info['hw_uid']
        self.i2c = I2C(self, bus=0)
        self.i2c_pd = I2C(self, bus=1)
        self.adc = ADC(self)
        self.cpld = CPLD(self)
        self.app = APP(self)

    def _auto_detect_serial(self, serial_number_match=None) -> (str, int):
        """Auto-detect the serial port

        Try to find the serial port with the 'Lightsource VCP' description.
        If serial_number is given, it will try to find the port with that serial number.

        :param serial_number_match: The serial number of the device to try and connect to
        :return: The serial port name and serial number
        """
        ports = list(serial.tools.list_ports.comports())
        serial_name = None
        serial_number = None
        if not ports:
            raise ValueError("No serial ports found")
        for p in ports:
            if platform.system() == "Windows":
                # on windows there is no description to check so we need to open each port
                try:
                    self.ser = serial.Serial(p.device, 115200, timeout=Connection.SERIAL_TIMEOUT_IN_S)
                    sn = self.get_info()['hw_uid']
                    self.ser.close()
                    if serial_number_match is not None and serial_number_match != sn:
                        continue
                    serial_name = p.device
                    serial_number = p.serial_number
                    break
                except Exception as e:
                    print(f"Error opening port {p.device}: {e}")
                    if hasattr(self, "ser"):
                        self.ser.close()
            else:
                if "Lightsource VCP" in p.description:
                    logger.debug(f"Found serial port: {p.device} ({p.description})")
                    self.ser = serial.Serial(p.device, 115200, timeout=Connection.SERIAL_TIMEOUT_IN_S)
                    sn = self.get_info()['hw_uid']
                    logger.debug(f"Auto detected serial number: {sn}")
                    self.ser.close()
                    if serial_number_match is not None and serial_number_match != sn:
                        logger.debug(f"SN: '{sn}' does not match the one we are looking for: '{serial_number_match}'")
                        continue
                    serial_name = p.device
                    serial_number = p.serial_number
                    break
        return serial_name, serial_number

    def _send_msg(self, msg_code, msg_data=None) -> None:
        self.ser.read_all()
        self.ser.write(self._create_msg(msg_code, msg_data))
        self.ser.flush()

    def _read_reply(self) -> (int, bytes):
        """Read a reply from the device

        Get the reply from the device and check the CRC.
        Returns the message code and the data part of the reply.
        """
        f_start = self.ser.read_until(b'\xf7')
        if not f_start or f_start[-1] != 0xf7:
            raise TimeoutError(f"No start of frame found, got: {f_start}")
        coded_reply = self.ser.read_until(b'\x00')
        coded_reply = coded_reply[:-1]
        try:
            decoded_reply = cobs.decode(coded_reply)
        except cobs.DecodeError as e:
            raise ValueError(f"COBS decode error: {e}. Data: {coded_reply}")
        if len(decoded_reply) >= 4:
            c = self._crc16(decoded_reply[:-2])
            if c != struct.unpack(">H", decoded_reply[-2:])[0]:
                raise ValueError("CRC check failed")
            return struct.unpack(">H", decoded_reply[:2])[0], decoded_reply[2:-2]
        raise ValueError("Invalid frame reply")

    @staticmethod
    def _create_msg(msg_code, msg_data=None):
        data = bytearray(struct.pack('>H', msg_code))
        if msg_data:
            data.extend(msg_data)
        crc = Connection._crc16(data)
        data.extend(struct.pack('>H', crc))
        encoded = bytearray(b'\xf7')
        encoded.extend(cobs.encode(data))
        encoded.extend(b'\x00')
        return encoded

    def get_info(self):
        reply_data = self.execute_command(self.MESSAGE_GET_INFO)
        reply_data += bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])  # append some extra bytes to accommodate old and new protocol reply
        reply_data += bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])  # append some extra bytes to accommodate old and new protocol reply
        return dict(hash=(int(reply_data[0]) << 24 | int(reply_data[1]) << 16 |
                          int(reply_data[2]) << 8 | int(reply_data[3])),
                    version=f"v{reply_data[4]}.{reply_data[5]}.{reply_data[6]}",
                    version_maj=int(reply_data[4]),
                    version_min=int(reply_data[5]),
                    version_pat=int(reply_data[6]),
                    hw_rev=int(reply_data[7]),
                    led_hw_rev=int(reply_data[8]),
                    cpld_version=f"v{chr(reply_data[9])}.{chr(reply_data[10])}{chr(reply_data[11])}",
                    cpld_version_maj=int(reply_data[9]) - 48,
                    cpld_version_min=int(reply_data[10]) - 48,
                    cpld_version_pat=chr(reply_data[11]),
                    hw_uid=struct.unpack(">L", reply_data[12:16])[0],
                    cpld_clock_hz=struct.unpack(">L", reply_data[16:20])[0],
                    scratch_buffer_size=struct.unpack(">H", reply_data[20:22])[0])

    def reboot_ls(self, assert_is_running: bool = True):
        """Send a reboot request."""
        self.execute_command(self.MESSAGE_REBOOT_LS)
        self.ser.close()
        # check for it to disappear
        start = time.time()
        while True:
            ports = list(serial.tools.list_ports.comports())
            if self.serial_name not in [p.device for p in ports]:
                break
            if time.time() - start > 10:
                raise TimeoutError("The port did not disappear when rebooting")
            time.sleep(0.1)
        # now start looking for it again
        start = time.time()
        while True:
            try:
                serial_name, sn = self._auto_detect_serial(serial_number_match=self.serial_number)
            except ValueError:
                serial_name = None
            if serial_name is not None:
                self.ser = Serial(serial_name, 115200, timeout=Connection.SERIAL_TIMEOUT_IN_S)
                self.ser.read_all()
                break
            if time.time() - start > 10:
                raise TimeoutError("Failed to reconnect to the device")
            time.sleep(0.2)
        if not self.ser.is_open:
            raise TimeoutError(f"Failed to reconnect to the device with serial number: {self.serial_number}")
        # check until it is running
        start = time.time()
        while assert_is_running:
            if self.app.get_status()['ls_state_by_name'] == 'running':
                break
            if time.time() - start > 3:
                raise TimeoutError("Failed to get running state after reboot. Is the power connected?")
            time.sleep(0.2)

    def execute_command(self, msg_code, msg_data=None):
        with self.lock:
            tries = 0
            reply_code = -1
            while tries < self.RETRIES:
                tries += 1
                try:
                    self._send_msg(msg_code, msg_data)
                    reply_code, reply_data = self._read_reply()
                    break
                except (ValueError, TimeoutError) as e:
                    logging.warning(f"Error executing '0x{msg_code:04x}': {msg_data}, try {tries}, error: {e}")
                    time.sleep(0.1)
                    # it can be problematic if certain commands get executed twice
                    if msg_code != Connection.MESSAGE_GET_INFO:
                        break
            else:
                raise ValueError(f"Failed to get reply after {self.RETRIES}")
        if reply_code == self.MESSAGE_ERROR:
            raise ValueError(f"Error reply: {reply_data}")
        if reply_code != msg_code:
            raise ValueError(f"Unexpected reply code: 0x{reply_code:x} != 0x{msg_code:x}")
        return reply_data

    @staticmethod
    def _crc16(data):
        crc = 0x0000
        n = len(data)
        for i in range(0, n):
            crc ^= data[i]
            for _ in range(0, 8):
                if (crc & 0x0001) > 0:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        return crc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.close()
        return False



class ADC:
    ADC_NAME_TO_NUM = {
        "12v_v": 0,
        "aux_i": 1,
        "jack_i": 2,
        "jack_v": 3,
        "led0_v": 4,
        "led1_v": 5,
        "led2_v": 6,
        "led3_v": 7,
        "tec0_v": 8,
        "tec1_v": 9,
        "usb1_i": 10,
        "usb1_v": 11,
        "usb2_i": 12,
        "usb2_v": 13,
        "mcu_t": 14,
    }

    TEMP_NAME_TO_NUM_R1_0 = {
        "cb_ntc_j14": 0,
        "cb_ntc_led_ch0": 1,
        "cb_ntc_led_ch3": 2,
        "cb_ntc_j13": 3,
        "lb_ntc_rt1": 4,
        "lb_ntc_rt2": 5,
        "lb_ntc_rt3": 6,
        "lb_ntc_rt4": 7,
        "fan_local": 8,
        "fan_remote": 9,
    }

    TEMP_NAME_TO_NUM_R1_1 = {
        "cb_ntc_j14": 0,
        "cb_ntc_led_ch1": 1,
        "cb_ntc_led_ch3": 2,
        "cb_ntc_j13": 3,
        "cb_ntc_tec_1": 4,
        "cb_ntc_tec_0": 5,
        "cb_ntc_led_ch0": 6,
        "cb_ntc_led_ch2": 7,
        "lb_ntc_rt1": 8,
        "lb_ntc_rt2": 9,
        "lb_ntc_rt3": 10,
        "lb_ntc_rt4": 11,
        "fan_local": 12,
        "fan_remote": 13,
    }

    def __init__(self, connection: Connection):
        self.conn = connection

    def bulk_read(self) -> dict:
        """Read all ADC values"""
        reply_data = self.conn.execute_command(Connection.MESSAGE_ADC_READ)
        num_adc_chans = len(reply_data) // 2
        all_values = [struct.unpack(">H", reply_data[i * 2:i * 2 + 2])[0] for i in range(num_adc_chans)]
        return {k: all_values[v] for k, v in self.ADC_NAME_TO_NUM.items()}

    def bulk_read_raw(self):
        """Read all ADC values.
        """
        reply_data = self.conn.execute_command(Connection.MESSAGE_ADC_READ_RAW)
        num_adc_chans = len(reply_data) // 2
        return [struct.unpack(">H", reply_data[i * 2:i * 2 + 2])[0] for i in range(num_adc_chans)]

    def bulk_read_temperatures(self):
        """Read temperature sensor measurements and the timestamp of measurement."""
        reply_data = self.conn.execute_command(Connection.MESSAGE_TEMP_READ)
        num_temps = (len(reply_data) - 4) // 2
        if num_temps == 14:
            temp_name_to_num = self.TEMP_NAME_TO_NUM_R1_1
        elif num_temps == 10:
            temp_name_to_num = self.TEMP_NAME_TO_NUM_R1_0
        else:
            raise ValueError("Unexpected number of temperatures returned")
        all_values = [struct.unpack(">H", reply_data[4 + i * 2:6 + i * 2])[0] for i in range(num_temps)]
        r = {k: all_values[v] / 256. for k, v in temp_name_to_num.items()}
        r["_timestamp"] = struct.unpack(">L", reply_data[0:4])[0]
        return r


class I2C:
    MAX_READ_LENGTH = 48

    LOG_BUF_I2C_READ = 0x100
    LOG_BUF_I2C_WRITE = 0x101
    LOG_BUF_I2C_WRITE_READ = 0x102

    def __init__(self, connection: Connection, bus=0, log_buf_enabled=False):
        self.conn = connection
        self.bus = bus
        # For logging I2C transactions, logs the actual data sent and received.
        # LOG_BUF_I2C_ tokens are used to signal transactions. Otherwise, stuff
        # is just dumped in this list.
        self._log_buffer = [] if log_buf_enabled else None

    def _log_data(self, token, i2c_address, data_written: Union[bytearray, bytes, list, tuple], data_read: Union[bytearray, bytes, list, tuple]):
        """Write data to the log buffer (if enabled)
        """
        if self._log_buffer is not None:
            self._log_buffer.append((token, i2c_address, bytes(data_written) if data_written is not None else None, bytes(data_read) if data_read is not None else None))

    def clear_log_buffer(self):
        if self._log_buffer is None:
            return
        self._log_buffer = []

    def show_log_buffer(self, show_only_i2c_address = None):
        """Pretty prints the log buffer contents
        """
        if self._log_buffer is None:
            print("I2C logging is disabled")
            return
        # Loop over logged entries.
        for idx, e in enumerate(self._log_buffer):
            if show_only_i2c_address is None or show_only_i2c_address == e[1]:
                if e[0] == self.LOG_BUF_I2C_READ:
                    print(f"{idx:4d}=[0x{e[1]:02x}] R({len(e[3])})", " ".join([f"{x:02x}" for x in e[3]]))
                elif e[0] == self.LOG_BUF_I2C_WRITE:
                    print(f"{idx:4d}=[0x{e[1]:02x}] W({len(e[2])})", " ".join([f"{x:02x}" for x in e[2]]))
                else:
                    print(f"{idx:4d}=[0x{e[1]:02x}] W({len(e[2])})", " ".join([f"{x:02x}" for x in e[2]]), f"R({len(e[3])})", " ".join([f"{x:02x}" for x in e[3]]))

    def write(self, i2c_address: int, data: Union[bytearray, bytes, list, tuple]) -> None:
        """Write data to the I2C bus

        :param i2c_address: The I2C address of the device
        :param data: The data to write max size is 48
        """
        if len(data) > self.MAX_READ_LENGTH or len(data) <= 0:
            raise ValueError(f"Can't write less than 1 or more than {self.MAX_READ_LENGTH} bytes")
        if isinstance(data, (list, tuple)):
            data = bytearray(data)
        msg = bytearray([self.bus, i2c_address]) + data
        self._log_data(self.LOG_BUF_I2C_WRITE, i2c_address, data, None)
        reply_data = self.conn.execute_command(Connection.MESSAGE_I2C_WR, msg)
        if reply_data[0] != len(data):
            raise ValueError(f"Unexpected reply: {reply_data[0]} != {len(data)}")

    def read(self, i2c_address: int, length: int) -> bytes:
        """Read data from the I2C bus

        :param i2c_address: The I2C address of the device
        :param length: The number of bytes to read max size is 48
        """
        if length > self.MAX_READ_LENGTH or length <= 0:
            raise ValueError(f"Can't read less than 1 or more than {self.MAX_READ_LENGTH} bytes")
        msg = bytearray([self.bus, i2c_address, length])
        reply_data = self.conn.execute_command(Connection.MESSAGE_I2C_RD, msg)
        self._log_data(self.LOG_BUF_I2C_READ, i2c_address, None, reply_data)
        if len(reply_data) != length:
            raise ValueError(f"Unexpected reply length: {len(reply_data)} != {length}")
        return reply_data

    def write_restart_read(self, i2c_address: int, write_data: Union[bytearray, bytes, list, tuple],
                           read_length: int) -> bytes:
        """Write data to the I2C bus and then read data from the I2C bus

        :param i2c_address: The I2C address of the device
        :param write_data: The data to write max size is 48
        :param read_length: The number of bytes to read max size is 48
        """
        if len(write_data) > self.MAX_READ_LENGTH or len(write_data) <= 0:
            raise ValueError(f"Can't write less than 1 or more than {self.MAX_READ_LENGTH} bytes")
        if read_length > self.MAX_READ_LENGTH or read_length <= 0:
            raise ValueError(f"Can't read less than 1 or more than {self.MAX_READ_LENGTH} bytes")
        if isinstance(write_data, (list, tuple)):
            write_data = bytearray(write_data)
        msg = bytearray([self.bus, i2c_address]) + write_data + bytearray([read_length])
        reply_data = self.conn.execute_command(Connection.MESSAGE_I2C_WR_R_RD, msg)
        self._log_data(self.LOG_BUF_I2C_WRITE_READ, i2c_address, write_data, reply_data)
        if len(reply_data) != read_length:
            raise ValueError(f"Unexpected reply length: {len(reply_data)} != {read_length}")
        return reply_data


class CPLD:
    """
    CPLD related functionality.
    """
    TRIGGER_MODE_FOLLOW = 0
    TRIGGER_MODE_TOGGLE = 1
    TRIGGER_MODE_FORCE_HIGH = 2
    TRIGGER_MODE_FORCE_LOW = 3
    TRIGGER_MODE_PULSE = 4

    def __init__(self, connection: Connection):
        self.conn = connection

    def reset_pulse_state(self):
        self.conn.execute_command(Connection.MESSAGE_CPLD_RESET_PULSE_STATE)

    def send_sw_trigger(self):
        self.conn.execute_command(Connection.MESSAGE_CPLD_SEND_SW_TRIGGER)

    def config_trigger_mode(self, mode, pulsenr=1):
        if mode not in [0, 1, 2, 3, 4]:
            raise ValueError("Invalid trigger mode value")
        msg = struct.pack(">BB", mode, pulsenr)
        reply_data = self.conn.execute_command(Connection.MESSAGE_CPLD_CONFIG_TRIGGER_MODE, msg)
        # Returns 0 or 1 to indicate NOK/OK.
        return reply_data[0]

    def config_ext_trigger(self, enable : bool, invert : bool, edge : bool):
        c = 0
        if enable:
            c |= 1
        if invert:
            c |= 2
        if edge:
            c |= 4
        msg = struct.pack(">B", c)
        self.conn.execute_command(Connection.MESSAGE_CPLD_CONFIG_EXT_TRIGGER, msg)

    def _config_trigger_output(self):
        """Should not be used, we can invert the input and this only makes it more complicated"""
        invert = False
        out_select = False  # not used / supported feature leave False
        c = 0
        if invert:
            c |= 1
        if out_select:
            c |= 2
        msg = struct.pack(">B", c)
        self.conn.execute_command(Connection.MESSAGE_CPLD_CONFIG_TRIGGER_OUTPUT, msg)

    def config_trigger_filter(self, pass_count = 0xffff, skip_count = 0x0000):
        msg = struct.pack(">HH", pass_count, skip_count)
        self.conn.execute_command(Connection.MESSAGE_CPLD_CONFIG_TRIGGER_FILTER, msg)

    def config_trigger_pulse(self, index, low_ticks, high_ticks):
        msg = struct.pack(">BLL", index, low_ticks, high_ticks)
        reply_data = self.conn.execute_command(Connection.MESSAGE_CPLD_CONFIG_TRIGGER_PULSE, msg)
        # Returns 0 or 1 to indicate NOK/OK.
        return reply_data[0]

    def set_ldac(self, v):
        msg = struct.pack(">L", v)
        self.conn.execute_command(Connection.MESSAGE_CPLD_SET_LDAC, msg)


class APP:
    """
    LS high-level API functions.
    """

    def __init__(self, connection: Connection):
        self.conn = connection

    def set_control(self, pwr_en : bool, tec_ctrl_en : bool = True, fan_ctrl_en : bool = True):
        """
        Set control register value. Currently defined bits:
          bit 0: Enable power sequencing (essentially enables the LS to power up and configure itself).
          bit 1: Enable TEC control (only possible in combination with bit 0 enabled).
          bit 2: Enable FAN control (only possible in combination with bit 0 enabled).
        """
        v = 0
        if pwr_en:
            v |= 1
            if tec_ctrl_en:
                v |= 2
            if fan_ctrl_en:
                v |= 4
        msg = struct.pack(">L", v)
        reply_data = self.conn.execute_command(Connection.MESSAGE_CONTROL_WR, msg)
        return struct.unpack(">L", reply_data)[0]

    def get_status(self):
        """
        Read status register.
        """
        reply_data = self.conn.execute_command(Connection.MESSAGE_STATUS_RD)
        v = struct.unpack(">L", reply_data)[0]
        PS_BY_NAME = ["none", "jack", "usb1pd", "usb2pd"]
        STATE_BY_NAME = ["do_nothing", "awaiting_power", "running", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR"]
        return {
            "ps_none_avail": v & 1 == 1,
            "ps_jack_avail": v & 2 == 2,
            "ps_usb1pd_avail": v & 4 == 4,
            "ps_usb2pd_avail": v & 8 == 8,
            "ps_selected": (v >> 4) & 3,
            "ps_selected_by_name": PS_BY_NAME[(v >> 4) & 3],
            "ls_state": (v >> 8) & 15,
            "ls_state_by_name": STATE_BY_NAME[(v >> 8) & 15],
        }

    def get_fan_info(self):
        """
        Read the fan RPM (tach) and duty cycle.
        """
        reply_data = self.conn.execute_command(Connection.MESSAGE_FAN_TACH_READ)
        v = struct.unpack(">HB", reply_data)
        return {
            "rpm": v[0],
            "duty_cycle": v[1]
        }

    def get_control(self):
        """
        Read control register.
        """
        reply_data = self.conn.execute_command(Connection.MESSAGE_CONTROL_RD)
        v = struct.unpack(">L", reply_data)[0]
        return {
            "pwr_en": v & 1 == 1,
            "tec_ctrl_en": v & 2 == 2,
            "fan_ctrl_en": v & 4 == 4,
        }

    def get_tec_setpoint(self):
        """Get the TEC target temperature in C (can be comma)."""
        reply_data = self.conn.execute_command(Connection.MESSAGE_TEC_PID_SETPOINT_RD)
        return struct.unpack(">H", reply_data[0:2])[0] / 256

    def get_led_power(self, led_channel, mux_sel):
        """Get the raw DAC 16-bit value for a LED and mux channel. Returns -1 on error."""
        if led_channel < 0 or led_channel > 3:
            raise ValueError("Invalid LED channel")
        if mux_sel != 0 and mux_sel != 1:
            raise ValueError("Invalid LED MUX selection")
        msg = struct.pack(">B", led_channel | (mux_sel << 7))
        reply_data = self.conn.execute_command(Connection.MESSAGE_LED_GET_CH_POWER, msg)
        if reply_data[0] == 0:
            return -1
        return struct.unpack(">H", reply_data[1:])[0]
    
    def set_led_calibrated_power(self, led_channel, mux_sel, percentage):
        """Set a calibrated power level (in percent of max calibrated range)."""
        if led_channel < 0 or led_channel > 3:
            raise ValueError("Invalid LED channel")
        if mux_sel != 0 and mux_sel != 1:
            raise ValueError("Invalid LED MUX selection")
        if percentage < 0 or percentage > 100:
            raise ValueError("Invalid LED power value")
        percent24 = int(percentage * (256 * 256 * 256 - 1) / 100 + 0.5)
        msg = struct.pack(">BL", led_channel | (mux_sel << 7), percent24)
        reply_data = self.conn.execute_command(Connection.MESSAGE_LED_SET_CH_CALIB_POWER, msg)
        return reply_data[0] == 1

