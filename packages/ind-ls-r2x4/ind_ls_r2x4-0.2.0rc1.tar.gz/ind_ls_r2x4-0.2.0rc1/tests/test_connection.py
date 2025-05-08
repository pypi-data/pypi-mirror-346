"""Test the connection module.

A connection with actual hardware is required to run these tests!
"""
import time
import struct
import pytest

from ls_r2x4._connection import Connection


def test_able_to_connect():
    with Connection() as conn:
        assert conn.ser.is_open
        conn.ser.close()

def test_get_info():
    with Connection() as conn:
        version_info = conn.get_info()
        assert isinstance(version_info, dict)
        assert "version" in version_info
        assert "hw_rev" in version_info
        assert "led_hw_rev" in version_info
        assert "cpld_version" in version_info


def test_adc_read():
    with Connection() as conn:
        adc = conn.adc.bulk_read()
        assert isinstance(adc, dict)
        assert adc['usb2_v'] > 4800 or adc['usb1_v'] > 4800
        assert adc['usb2_v'] < 5300 and adc['usb1_v'] < 5300


def test_adc_read_tempertures():
    with Connection() as conn:
        temps = conn.adc.bulk_read_temperatures()
        print(temps)
        time.sleep(2)
        temps = conn.adc.bulk_read_temperatures()
        print(temps)


@pytest.mark.order(1)
def test_reboot():
    with Connection() as conn:
        conn.reboot_ls()  # raises error when reboot is not successful


@pytest.mark.order(2)
def test_app_get_status():
    with Connection() as conn:
        status = conn.app.get_status()
        assert isinstance(status, dict)
        assert status['ls_state_by_name'] in ('awaiting_power', 'do_nothing', 'running')

@pytest.mark.order(3)
def test_app_power_on():
    with Connection() as conn:
        conn.app.set_control(pwr_en=True, tec_ctrl_en=False, fan_ctrl_en=False)
        ctrl = conn.app.get_control()
        assert ctrl['pwr_en'] == True
        assert ctrl['tec_ctrl_en'] == False
        assert ctrl['fan_ctrl_en'] == False
        time.sleep(.5)
        status = conn.app.get_status()
        assert status['ls_state_by_name'] == 'running'


@pytest.mark.order(5)
def test_app_fan_control_on():
    with Connection() as conn:
        conn.app.set_control(pwr_en=True, tec_ctrl_en=True, fan_ctrl_en=True)
        ctrl = conn.app.get_control()
        assert ctrl['pwr_en'] == True
        assert ctrl['tec_ctrl_en'] == True
        assert ctrl['fan_ctrl_en'] == True
        time.sleep(2)
        info = conn.app.get_fan_info()
        assert info['rpm'] > 0
        assert info['duty_cycle'] > 0
        status = conn.app.get_status()
        assert status['ls_state_by_name'] == 'running'


@pytest.mark.order(7)
def test_app_set_led_calibrated_power():
    with Connection() as conn:
        off_current = conn.adc.bulk_read()['jack_i']
        for channel in range(4):
            for mux in range(2):
                conn.app.set_led_calibrated_power(led_channel=channel, mux_sel=mux, percentage=30)
                time.sleep(0.5)
                on_current = conn.adc.bulk_read()['jack_i']
                conn.app.set_led_calibrated_power(led_channel=channel, mux_sel=mux, percentage=0)
                if mux == 0:
                    assert on_current - off_current > 100  # expecting more than 100 mA current increase
                else:
                    assert on_current - off_current < 20  # mux 1 is not active, so no current increase expected


@pytest.mark.order(8)
def test_cpld_send_sw_trigger_with_force_high_and_low():
    with Connection() as conn:
        conn.app.set_led_calibrated_power(led_channel=1, mux_sel=1, percentage=50)
        off_current = conn.adc.bulk_read()['jack_i']
        conn.cpld.config_trigger_mode(mode=conn.cpld.TRIGGER_MODE_FORCE_HIGH)
        conn.cpld.send_sw_trigger()
        time.sleep(1)
        on_current = conn.adc.bulk_read()['jack_i']
        conn.cpld.config_trigger_mode(mode=conn.cpld.TRIGGER_MODE_FORCE_LOW)
        conn.cpld.send_sw_trigger()
        conn.app.set_led_calibrated_power(led_channel=1, mux_sel=1, percentage=0)
        assert on_current - off_current > 75


@pytest.mark.order(9)
def test_cpld_send_sw_trigger_with_pulse():
    with Connection() as conn:
        conn.app.set_led_calibrated_power(led_channel=1, mux_sel=1, percentage=30)
        conn.cpld.config_ext_trigger(enable=False, invert=False, edge=False)
        conn.cpld.config_trigger_mode(mode=conn.cpld.TRIGGER_MODE_PULSE, pulsenr=1)
        clk_freq = conn.get_info()['cpld_clock_hz']
        conn.cpld.config_trigger_pulse(index=0, low_ticks=int(1 * clk_freq),
                                       high_ticks=int(1 * clk_freq))
        conn.cpld.reset_pulse_state()
        conn.cpld.send_sw_trigger()
        time.sleep(.1)
        off_current = conn.adc.bulk_read()['jack_i']
        time.sleep(1)
        on_current = conn.adc.bulk_read()['jack_i']
        time.sleep(1)
        conn.app.set_led_calibrated_power(led_channel=1, mux_sel=1, percentage=0)
        assert on_current - off_current > 100


@pytest.mark.order(22)
def test_app_power_off():
    with Connection() as conn:
        conn.app.set_control(pwr_en=False)
        time.sleep(1)
        status = conn.app.get_status()
        assert status['ls_state_by_name'] == 'do_nothing'