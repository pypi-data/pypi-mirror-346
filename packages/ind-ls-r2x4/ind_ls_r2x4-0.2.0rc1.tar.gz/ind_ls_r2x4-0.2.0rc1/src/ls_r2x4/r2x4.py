"""Holds the LightSourceR2X4 class"""
import json
import pathlib
import logging
import struct
import time

from ls_r2x4._connection import Connection
from ls_r2x4._utils import ConfigFloat, ConfigBool, R2X4OperationError

logger = logging.getLogger(__name__)


class LightSourceR2X4:

    SOURCE_TYPE = "R/G/B/W"
    CHANNELS = ("Red_a", "Red_b",
                "Green_a", "Green_b",
                "Blue_a", "Blue_b",
                "White_a", "White_b")

    CHANNEL_DETAILS = dict(red_a=dict(wavelength=625),
                           red_b=dict(wavelength=625),
                           green_a=dict(wavelength=525),
                           green_b=dict(wavelength=525),
                           blue_a=dict(wavelength=475),
                           blue_b=dict(wavelength=475),
                           white_a=dict(wavelength=0),
                           white_b=dict(wavelength=0))

    HW_CHANNEL = dict(red=3, green=1, blue=0, white=2)
    HW_IDX_TO_CHANNEL = {v: k for k, v in HW_CHANNEL.items()}

    _instance = None

    def __init__(self, serial_name: str = None, wait_for_stable_temperature: bool = True, assert_is_running: bool = True):
        self._conn = Connection(serial_name=serial_name)

        self.info = self._conn.get_info()
        logger.info("R2X4 Firmware version: {}".format(self.info['version']))
        logger.info("R2X4 HW uid: {}".format(self.info['hw_uid']))
        logger.info("R2X4 Controller board HW revision: {}".format(self.info['hw_rev']))
        logger.info("R2X4 LED board HW revision: {}".format(self.info['led_hw_rev']))
        logger.info("R2X4 CPLD version: {}".format(self.info['cpld_version']))

        self.red_a = ConfigFloat(name="red_a", minimum=0, maximum=100, unit="%", doc="Red channel a power",
                                 gui_show=False)
        self.red_b = ConfigFloat(name="red_b", minimum=0, maximum=100, unit="%", doc="Red channel b power",
                                 gui_show=False)
        self.green_a = ConfigFloat(name="green_a", minimum=0, maximum=100, unit="%", doc="Green channel a power",
                                   gui_show=False)
        self.green_b = ConfigFloat(name="green_b", minimum=0, maximum=100, unit="%", doc="Green channel b power",
                                   gui_show=False)
        self.blue_a = ConfigFloat(name="blue_a", minimum=0, maximum=100, unit="%", doc="Blue channel a power",
                                  gui_show=False)
        self.blue_b = ConfigFloat(name="blue_b", minimum=0, maximum=100, unit="%", doc="Blue channel b power",
                                  gui_show=False)
        self.white_a = ConfigFloat(name="white_a", minimum=0, maximum=100, unit="%", doc="White channel a power",
                                   gui_show=False)
        self.white_b = ConfigFloat(name="white_b", minimum=0, maximum=100, unit="%", doc="White channel b power",
                                   gui_show=False)

        self.mux_sel = ConfigBool(name="mux_sel", doc="Activate level 'a' when False and level 'b' when True", gui_show=False)

        self.red_a.value = 0
        self.red_b.value = 0
        self.green_a.value = 0
        self.green_b.value = 0
        self.blue_a.value = 0
        self.blue_b.value = 0
        self.white_a.value = 0
        self.white_b.value = 0

        self.mux_sel.value = False

        self.red_a.set_value_event += self._apply_configs
        self.red_b.set_value_event += self._apply_configs
        self.green_a.set_value_event += self._apply_configs
        self.green_b.set_value_event += self._apply_configs
        self.blue_a.set_value_event += self._apply_configs
        self.blue_b.set_value_event += self._apply_configs
        self.white_a.set_value_event += self._apply_configs
        self.white_b.set_value_event += self._apply_configs

        self.mux_sel.set_value_event += self._apply_mux

        self._channels = dict(red_a=self.red_a, red_b=self.red_b,
                              green_a=self.green_a, green_b=self.green_b,
                              blue_a=self.blue_a, blue_b=self.blue_b,
                              white_a=self.white_a, white_b=self.white_b)

        if not assert_is_running:
            self._protect_instance = True
            return
        else:
            state = self._conn.app.get_status()['ls_state_by_name']
            if state != 'running':
                # attempt to get out of standby of it was in standby mode
                self.standby_disable(wait_for_stable_temperature=False)

        for channel in self._channels.values():
            channel.value = 0  # all off
        self.triggering_force_a_channels()
        self._setup_comparator()
        LightSourceR2X4._instance = self

        if wait_for_stable_temperature:
            try:
                self._wait_for_stable_led_temperature()
            except TimeoutError:
                logger.warning("Timeout waiting for stable temperature!")

        self._protect_instance = True

    @classmethod
    def get_instance(cls, recreate=False, serial_name=None) -> 'LightSourceR2X4':
        """Get the LightSourceR2X4 singleton instance

        :param serial_name: The serial port name, leave None to try and auto connect
        :param recreate: If True, the old instance is closed and a new one is created
        :return: The LightSourceR2X4 instance
        """
        # A bit ugly, as this sets a class variable in its super class.
        if LightSourceR2X4._instance is None:
            LightSourceR2X4._instance = cls(serial_name=serial_name)
        elif recreate:
            cls._instance._conn.ser.close()
            LightSourceR2X4._instance = cls(serial_name=serial_name)
        return LightSourceR2X4._instance

    def _setup_comparator(self):
        """Set up the comparator for the light source trigger input"""

        def voltage_to_dn(voltage=1.66, gain=3, vref=1.21):
            lsb = int((voltage * (2 ** 10)) / (vref * gain))
            assert 0 <= lsb < (2 ** 10)
            return lsb

        dn = voltage_to_dn()
        write_data = dn  << 2 + 4

        # hardcode settings for 1.66V here for now
        self._conn.i2c.write(0x49, [0x0f, 0x10, 0x00])
        self._conn.i2c.write(0x49, [0x1b, 0x00, 0x00])
        self._conn.i2c.write(0x49, [0x16, 0x10, 0x00])
        self._conn.i2c.write(0x49, [0x1f, 0x1c, 0x76])
        self._conn.i2c.write(0x49, [0x1c, 0x7f, 0xff])
        self._conn.i2c.write(0x49, [0x1b, (write_data & 0xff00) >> 8, write_data & 0xff])

    def standby_enable(self):
        """Put the light source in a low power standby mode

        This will turn off the LEDs and the temperature control. The light source will not be able to be controlled
        until it is brought back out of standby mode with the standby_disable method, or by power cycling the light
        source.
        """
        for channel in self:
            channel.value = 0
        self._conn.app.set_control(pwr_en=False)

    def standby_disable(self, wait_for_stable_temperature: bool = True):
        """Bring the light source out of standby mode

        When the light source is powered on it will not be in standby mode. So you only need to call this method if you
        have put the light source in standby mode before. Or you can call it to try and get out of an error state.

        :param wait_for_stable_temperature: Wait for the LED temperature to stabilize before returning
        """
        self._conn.app.set_control(pwr_en=True)

        # check if we are in the expected state
        start = time.time()
        while time.time() - start < 2:
            status = self._conn.app.get_status()
            if status['ls_state_by_name'] == 'running':
                break
        if status['ls_state_by_name'] != 'running':
            raise TimeoutError("Light source did not reach running state. Check the power supply and connections. "
                               f"Current state: {status['ls_state_by_name']}")

        if wait_for_stable_temperature:
            self._wait_for_stable_led_temperature()

    def _wait_for_stable_led_temperature(self):
        logger.info("Waiting for temperature to stabilize")
        set_point = self._conn.app.get_tec_setpoint()
        margin = 1  # we want to be in the range of the set point +- margin
        timeout = 60
        start = time.time()
        while time.time() - start < timeout:  # one min timeout
            temp = self._conn.adc.bulk_read_temperatures()['lb_ntc_rt2']  # center temperature sensor on LED board
            if abs(temp - set_point) < margin:
                # we are in range, now check for stability
                time.sleep(1)  # wait for a bit
                temp2 = self._conn.adc.bulk_read_temperatures()['lb_ntc_rt2']  # measure again
                if abs(temp - temp2) < 0.02:  # 0.02C difference after 1s is considered stable
                    break
            time.sleep(0.2)
            logger.info(f"Temperature: {temp:.2f}C")
        if abs(temp - set_point) > margin:
            raise TimeoutError(f"Temperature did not stabilize within {timeout}s. Current temperature: {temp:.2f}C")

    def reboot(self, wait_for_stable_temperature: bool = True, assert_is_running: bool = True):
        """Reboot the light source"""
        self._conn.reboot_ls(assert_is_running=assert_is_running)

        for channel in self:
            channel.value = 0

        if not assert_is_running and self._conn.app.get_status()['ls_state_by_name'] != 'running':
            logger.warning("LS probably unpowered?")
            return

        if wait_for_stable_temperature:
            self._wait_for_stable_led_temperature()
        self.triggering_follow_external()
        self._setup_comparator()

    def _apply_mux(self, changed_config: ConfigBool):
        """Write the value to the light source"""
        if changed_config.value:
            self.triggering_force_b_channels()
        else:
            self.triggering_force_a_channels()

    @staticmethod
    def power_min_max():
        return 0, 100

    def _apply_configs(self, changed_config: ConfigFloat):
        """Write the value to the light source"""
        changed_name = changed_config.name
        color, channel = changed_name.split('_')
        hw_idx = self.HW_CHANNEL[color]
        if channel == 'a':
            muxsel = 0
        else:
            muxsel = 1
        self._conn.app.set_led_calibrated_power(led_channel=hw_idx, mux_sel=muxsel, percentage=changed_config.value)

    def get_ls_hw_revision(self):
        return self._conn.get_info()["hw_rev"]

    def get_ledboard_hw_revision(self):
        return self._conn.get_info()["led_hw_rev"]

    def get_hardware_uid(self):
        return self._conn.get_info()['hw_uid']

    def triggering_force_a_channels(self):
        """Force light source to enable the 'a' channels

        External and software triggers are ignored
        """
        self._conn.cpld.config_trigger_mode(mode=self._conn.cpld.TRIGGER_MODE_FORCE_LOW)
        self._conn.cpld.send_sw_trigger()

    def triggering_force_b_channels(self):
        """Force light source to enable the 'b' channels

        External and software triggers are ignored
        """
        self._conn.cpld.config_trigger_mode(mode=self._conn.cpld.TRIGGER_MODE_FORCE_HIGH)
        self._conn.cpld.send_sw_trigger()

    def triggering_follow_external(self, invert=True):
        """The light follows the digital trigger input

        :param invert: invert the input trigger
        """
        self._conn.cpld.config_ext_trigger(enable=True, invert=invert, edge=False)
        self._conn.cpld.config_trigger_mode(mode=self._conn.cpld.TRIGGER_MODE_FOLLOW)

    def triggering_edge_pulsed(self, nr_pulses: int, disable_external: bool = False, rising_edge=True):
        """Configure the triggering to use edge triggers to generate configured pulses. Up to 4 pulses are supported.

        Both external or internal software triggers can be used. Extra filtering can be used to pass or skip pulses as
        well usings the triggering_configure_filtering method.

        Each pulse must be configured using the triggering_configure_pulse method.

        :param nr_pulses: The number of pulses to use. Must be value >=1 and <=4. The triggering_configure_pulse method
        must be called to configure each pulse.
        :param disable_external: Disable the external trigger input, only the software trigger will work
        :param rising_edge: Trigger on the rising edge, if False, trigger on the falling edge
        """
        self._conn.cpld.config_trigger_filter(pass_count=1, skip_count=0)  # reset filtering
        self._conn.cpld.config_ext_trigger(enable=not disable_external, invert=not rising_edge, edge=True)
        self._conn.cpld.config_trigger_mode(mode=self._conn.cpld.TRIGGER_MODE_PULSE, pulsenr=nr_pulses)
        self._conn.cpld.reset_pulse_state()

    def triggering_configure_pulse(self, index: int = 0, low_s: float = 0.1, high_s: float = 0.1):
        """Configure a pulse for the triggering_edge_pulsed method

        :param index: The index of the pulse to configure. Must be 0-3
        :param low_s: The duration of the low pulse in seconds.
        :param high_s: The duration of the high pulse in seconds.
        """
        clk_freq = self.info['cpld_clock_hz']
        max_s = 2**32 / clk_freq
        for s in (low_s, high_s):
            if not 0 <= s < max_s:
                raise ValueError(f"The pulse duration must be between 0 and {max_s} seconds")
        low_clocks = int(low_s * clk_freq)
        high_clocks = int(high_s * clk_freq)
        self._conn.cpld.config_trigger_pulse(index=index, low_ticks=low_clocks, high_ticks=high_clocks)
        return low_clocks, high_clocks

    def triggering_configure_filtering(self, pass_count: int = 1, skip_count: int = 0):
        """Configure the filtering of pulses

        Can be used to mask out pulses. For example when x illumination pulses are needed and then y pulses no pulses.

        :param pass_count: The number of pulses to pass
        :param skip_count: The number of pulses to skip
        """
        self._conn.cpld.config_trigger_filter(pass_count=pass_count, skip_count=skip_count)
        self._conn.cpld.reset_pulse_state()

    def triggering_reset_pulse_state(self):
        """Reset the pulse and filtering counts

        This does not change the configuration, it only resets the counters of the steps and filter to the initial state
        """
        self._conn.cpld.reset_pulse_state()

    def triggering_send_software_edge_trigger(self):
        """Trigger the light source using the software trigger"""
        self._conn.cpld.send_sw_trigger()

    def triggering_configure_self_trigger(self, period_s: float, enable: bool = True) -> float:
        """Configure the light source to trigger itself at a given period

        :param period_s: The period in seconds
        :param enable: Enable or disable the self triggering
        :return: The actual period in seconds
        """
        freq = self.info['cpld_clock_hz']
        periodticks = round(period_s * freq) - 2

        if periodticks < 0:
            periodticks = 0

        periodactual = (periodticks + 2) / freq

        logger.info(f"Period requested {period_s:e}s: period ticks = {periodticks}, actual period = {periodactual:e}s")

        # read
        self._conn.i2c.write(0x4E, [0xC])
        bytes_read = self._conn.i2c.read(0x4E, 4)
        prev = struct.unpack("<I", bytes_read)[0]
        bit = 1 << 3

        if enable:
            new = prev | bit
            # when enabling make sure the period is set first before enabling
            self._conn.i2c.write(0x4E, [0x34] + list(struct.pack("<I", periodticks)))
            self._conn.i2c.write(0x4E, [0xC] + list(struct.pack("<I", new)))
        else:
            new = prev & ~bit
            # when disabling make sure the period is set after disabling
            self._conn.i2c.write(0x4E, [0xC] + list(struct.pack("<I", new)))
            self._conn.i2c.write(0x4E, [0x34] + list(struct.pack("<I", periodticks)))
        return periodactual

    def get_info(self, print_to_console: bool = True):
        if print_to_console:
            for k, v in self.info.items():
                print(f"{k}: {v}")
        return self.info

    def get_status(self, print_to_console: bool = True):
        status = dict(app=self._conn.app.get_status(),
                      sys_mon=self._conn.adc.bulk_read(),
                      temperatures=self._conn.adc.bulk_read_temperatures(),
                      fan=self._conn.app.get_fan_info())
        if print_to_console:
            for section, section_dict in status.items():
                print(f"{section.upper()}:")
                for k, v in section_dict.items():
                    print(f"{k}: {v}")
        return status

    def __getitem__(self, key):
        return self._channels[key]

    def __setitem__(self, key, v):
        self._channels[key].value = v

    def __iter__(self):
        return iter(self._channels.values())

    def __repr__(self):
        return (f"LightSourceR2X4(red_a/b={self.red_a.value}/{self.red_b.value}, "
                f"green_a/b={self.green_a.value}/{self.green_b.value}, "
                f"blue_a/b={self.blue_a.value}/{self.blue_b.value}, "
                f"white_a/b={self.white_a.value}/{self.white_b.value})")

    def __del__(self):
        try:
            self._conn.ser.close()
        except AttributeError:
            pass

    def __setattr__(self, name, value):
        """Protect the instance from being modified

        Mainly to prevent ls.red_a = 10 type of assignments (needs to be ls.red_a.value = 10)
        """
        if hasattr(self, '_protect_instance') and self._protect_instance:
            raise AttributeError("Cannot set attributes on LightSourceR2X4 instance")
        else:
            super().__setattr__(name, value)


def main():
    import ls_r2x4.demo.demo as demo
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    ls = LightSourceR2X4()
    logger.info("Starting demo")
    demo.sweep_all_channels_no_triggering(ls=ls)
    demo.pulse_white_with_4_lengths_from_software_trigger(ls=ls)
    demo.toggle_green_and_blue_with_self_triggering(ls=ls)
    demo.toggle_red_and_white_self_triggering_in_combination_with_filtering(ls=ls)
    # set back to default
    ls.triggering_follow_external()  # set back to follow external trigger


# demo run
if __name__ == '__main__':
    main()
