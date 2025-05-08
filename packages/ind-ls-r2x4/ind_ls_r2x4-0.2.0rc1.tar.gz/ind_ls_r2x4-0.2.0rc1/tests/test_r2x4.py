"""Tests on the LightSourceR2X4 class

Needs hardware to run!
"""

from ls_r2x4.r2x4 import LightSourceR2X4

# create ls instance once to run tests on
ls = LightSourceR2X4(wait_for_stable_temperature=False)


def test_instance_protected():
    """
    Test that a class instance is protected from changes in the class
    """
    # change that changing the channel attritube raises an error
    try:
        ls.red_a = 1
    except AttributeError:
        pass
    else:
        raise AssertionError("No error raised")


def test_can_set_channel():
    """
    Test that a channel can be set
    """
    ls.red_a.value = 0.1
    assert ls.red_a.value == 0.1


def test_numpy_float_supported():
    """
    Test that numpy float is supported to set a channel
    """
    import numpy as np
    ls.red_a.value = np.float64(0.1)
    assert ls.red_a.value == 0.1
    ls.red_a.value = np.float32(0.1)
    # check of close enough
    assert abs(ls.red_a.value - 0.1) < 1e-5
    ls.red_a.value = 0


def test_numpy_int_supported():
    """
    Test that numpy int is supported to set a channel
    """
    import numpy as np
    ls.red_a.value = np.int8(1)
    assert ls.red_a.value == 1
    ls.red_a.value = np.int16(1)
    assert ls.red_a.value == 1
    ls.red_a.value = np.int32(1)
    assert ls.red_a.value == 1
    ls.red_a.value = np.int64(1)
    assert ls.red_a.value == 1
    ls.red_a.value = 0


def test_get_info():
    """
    Test that the info can be retrieved
    """
    info = ls.get_info()
    assert 'hw_uid' in info

def test_set_mux():
    """
    Test that the mux can be set
    """
    ls.mux_sel.value = False
    assert ls.mux_sel.value == False
    ls.mux_sel.value = 1
    assert ls.mux_sel.value == True
    ls.mux_sel.value = 0
    assert ls.mux_sel.value == False


def test_reboot():
    """
    Test that the lightsource can be rebooted
    """
    ls.reboot(wait_for_stable_temperature=False)
    ls._wait_for_stable_led_temperature()


def test_standby():
    """
    Test that the lightsource can be set to standby
    """
    ls.standby_enable()
    ls.standby_disable(wait_for_stable_temperature=False)


def test_get_status():
    """
    Test that the status can be retrieved
    """
    status = ls.get_status()
    assert 'app' in status
    assert 'ls_state' in status['app']
    assert 'sys_mon' in status
    assert 'jack_v' in status['sys_mon']
    assert 'temperatures' in status
    assert 'fan_local' in status['temperatures']
    assert 'fan' in status
    assert 'rpm' in status['fan']


def test_we_can_use_fixed_serial_name():
    """
    Test that we can use a fixed serial name
    """
    global ls
    sn = ls._conn.serial_name
    ls.standby_enable()
    ls._conn.ser.close()
    ls = LightSourceR2X4(serial_name=sn, wait_for_stable_temperature=False)