import logging
import time

from  ls_r2x4.r2x4 import LightSourceR2X4

logger = logging.getLogger('demo')
logger.setLevel(logging.INFO)


def sweep_all_channels_no_triggering(ls: LightSourceR2X4 = None):
    """Do a software sweep of all channels over the full range

    :param ls: Optional instance, one is created if left None
    """
    if ls is None:
        ls = LightSourceR2X4()
    ls.triggering_force_a_channels()
    logger.info("Sweep all channels with no triggering")
    for channel in (ls.red_a, ls.green_a, ls.blue_a, ls.white_a):
        logger.info(f"channel: {channel.name[:-2]} wave")
        for intensity in range(0, 101, 10):
            channel.value = intensity
            time.sleep(0.02)
        for intensity in range(100, -1, -10):
            channel.value = intensity
            time.sleep(0.02)


def pulse_white_with_4_lengths_from_software_trigger(ls: LightSourceR2X4 = None):
    """Pulse white with 4 different pulse lengths from software trigger

    :param ls: Optional instance, one is created if left None
    """
    if ls is None:
        ls = LightSourceR2X4()
    ls.triggering_force_a_channels()
    logger.info("Pulse white with 4 different pulse lengths from software trigger")
    ls.white_b.value = 4
    ls.triggering_edge_pulsed(nr_pulses=4, disable_external=True)
    ls.triggering_configure_pulse(0, 0, 0.1)
    ls.triggering_configure_pulse(1, 0, 0.2)
    ls.triggering_configure_pulse(2, 0, 0.3)
    ls.triggering_configure_pulse(3, 0, 0.4)
    ls.triggering_reset_pulse_state()
    for _ in range(8):
        ls.triggering_send_software_edge_trigger()
        time.sleep(0.5)
    ls.white_b.value = 0


def toggle_green_and_blue_with_self_triggering(ls: LightSourceR2X4 = None):
    """Toggle green and blue with self trigger period of 0.2s

    :param ls: Optional instance, one is created if left None
    """
    if ls is None:
        ls = LightSourceR2X4()
    logger.info("Toggle green and blue with self trigger period of 0.2s")
    ls.green_b.value = 4
    ls.blue_a.value = 4
    ls.triggering_edge_pulsed(nr_pulses=1, disable_external=True)
    ls.triggering_configure_pulse(0, 0, 0.2)
    ls.triggering_reset_pulse_state()
    ls.triggering_configure_self_trigger(period_s=0.2, enable=True)
    time.sleep(4)
    ls.triggering_configure_self_trigger(period_s=0.2, enable=False)
    ls.green_b.value = 0
    ls.blue_a.value = 0


def toggle_red_and_white_self_triggering_in_combination_with_filtering(ls: LightSourceR2X4 = None):
    """Use self triggering in combination with filtering to toggle red and white

    :param ls: Optional instance, one is created if left None
    """
    if ls is None:
        ls = LightSourceR2X4()
    logger.info("Use self triggering in combination with filtering to toggle red and white")
    ls.red_a.value = 4
    ls.white_b.value = 4
    ls.triggering_edge_pulsed(nr_pulses=1, disable_external=True)
    ls.triggering_configure_pulse(0, 0, 0.1)
    ls.triggering_configure_filtering(pass_count=4, skip_count=1)
    ls.triggering_reset_pulse_state()
    ls.triggering_configure_self_trigger(period_s=0.2, enable=True)
    time.sleep(4)
    ls.triggering_configure_self_trigger(period_s=0.2, enable=False)
    ls.red_a.value = 0
    ls.white_b.value = 0


def external_triggering_with_filtering(ls: LightSourceR2X4 = None):
    """Use external triggering in combination with filtering

    Make sure the trigger inputs has a signale connected to it!

    :param ls: Optional instance, one is created if left None
    """
    if ls is None:
        ls = LightSourceR2X4()
    logger.info("Use external triggering in combination with filtering")
    ls.green_a.value = 4
    ls.white_b.value = 4
    ls.triggering_edge_pulsed(nr_pulses=1, disable_external=False)
    ls.triggering_configure_pulse(0, 0, 0.1)
    ls.triggering_configure_filtering(pass_count=4, skip_count=1)
    ls.triggering_reset_pulse_state()
    time.sleep(4)
    ls.green_a.value = 0
    ls.white_b.value = 0


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.info("Create LightSourceR2X4 instance")
    ls = LightSourceR2X4()
    logger.info("Starting demo")
    sweep_all_channels_no_triggering(ls=ls)
    pulse_white_with_4_lengths_from_software_trigger(ls=ls)
    toggle_green_and_blue_with_self_triggering(ls=ls)
    toggle_red_and_white_self_triggering_in_combination_with_filtering(ls=ls)
    # set back to default
    ls.triggering_follow_external()  # set back to follow external trigger
