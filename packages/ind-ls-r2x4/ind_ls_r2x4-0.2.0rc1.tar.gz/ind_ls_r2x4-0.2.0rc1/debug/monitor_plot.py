import queue

import matplotlib.pyplot as plt
import time
import collections

import numpy as np

from ls_r2x4.r2x4 import LightSourceR2X4


def run(ls: LightSourceR2X4, thread_messg_queue: queue.Queue = None, auto_draw: bool = True):
    """Run a monitor on the light source performance and plot the results

    Run this in a separate thread if you want to also change the light levels in parallel

    :param thread_messg_queue: queue for inter thread communication
    :param auto_draw: automatically draw the plot after each iteration
    """
    plt.close('all')  # close all previous plots to prevent them from updating each loop

    queue_len = 256
    tec0_volts = collections.deque(maxlen=queue_len)
    tec1_volts = collections.deque(maxlen=queue_len)
    tec_diffs = collections.deque(maxlen=queue_len)
    tec_pows = collections.deque(maxlen=queue_len)
    total_pows = collections.deque(maxlen=queue_len)
    led_pows = collections.deque(maxlen=queue_len)
    fan_pows = collections.deque(maxlen=queue_len)

    temps_hs_hot = collections.deque(maxlen=queue_len)
    temps_hs_cold = collections.deque(maxlen=queue_len)
    temps_lb_south_white = collections.deque(maxlen=queue_len)
    temps_lb_middle = collections.deque(maxlen=queue_len)
    temps_lb_west_blue = collections.deque(maxlen=queue_len)
    temps_lb_north_white = collections.deque(maxlen=queue_len)
    temps_blue = collections.deque(maxlen=queue_len)
    temps_red = collections.deque(maxlen=queue_len)
    temps_fan_local = collections.deque(maxlen=queue_len)
    temps_fan_remote = collections.deque(maxlen=queue_len)

    led_r_i_set = collections.deque(maxlen=queue_len)
    led_g_i_set = collections.deque(maxlen=queue_len)
    led_b_i_set = collections.deque(maxlen=queue_len)
    led_w_i_set = collections.deque(maxlen=queue_len)
    led_r_v_drv = collections.deque(maxlen=queue_len)
    led_g_v_drv = collections.deque(maxlen=queue_len)
    led_b_v_drv = collections.deque(maxlen=queue_len)
    led_w_v_drv = collections.deque(maxlen=queue_len)

    times = collections.deque(maxlen=queue_len)
    fan_duties = collections.deque(maxlen=queue_len)
    fan_tachs = collections.deque(maxlen=queue_len)

    all_queues = (tec0_volts, tec1_volts, tec_diffs, tec_pows,
                  temps_hs_hot, temps_hs_cold, temps_lb_south_white, temps_lb_middle, temps_lb_west_blue,
                  temps_lb_north_white, temps_blue, temps_red, temps_fan_local, temps_fan_remote,
                  led_r_i_set, led_g_i_set, led_b_i_set, led_w_i_set, led_r_v_drv, led_g_v_drv, led_b_v_drv, led_w_v_drv,
                  times, fan_duties, fan_tachs, total_pows, led_pows, fan_pows)

    if queue_len is not None:
        for q in all_queues:
            q.extend(np.zeros((queue_len,)))

    plt.ion()
    # have 4 plots
    fig, (ax_tec_v, ax_temps, ax_leds_i, ax_fan_duty) = plt.subplots(4, 1, sharex=True, figsize=(8, 10),
                                                                     height_ratios=[2, 3, 2, 2])
    plt.subplots_adjust(left=.1, right=.775)  # more space for 3rd axis
    plt.ioff()

    ax_tec_p = ax_tec_v.twinx()
    ax_led_v = ax_leds_i.twinx()
    ax_fan_tach = ax_fan_duty.twinx()
    ax_fan_ctrl_temp = ax_fan_duty.twinx()

    ax_tec_v.set_title("TEC")
    ax_tec_v.set_ylabel("tec volt (V)")
    ax_tec_v.set_ylim(-3, 25)
    ax_tec_p.set_ylabel("power (W)", color='C3')
    ax_tec_p.set_ylim(-10, 100)
    ax_temps.set_title("Temperatures")
    ax_temps.set_ylabel("temp (degC)")
    ax_temps.set_ylim(20, 45)
    ax_leds_i.set_title("LEDs")
    ax_leds_i.set_ylabel("LED setting (A)")
    ax_leds_i.set_ylim(-0.01, 0.52)
    ax_led_v.set_ylabel("LED driver -- (V)")
    ax_led_v.set_ylim(23, 32)
    ax_fan_duty.set_title("Fan")
    ax_fan_duty.set_ylabel("fan duty (%)", color='C0')
    ax_fan_duty.set_xlabel("time (s)")
    ax_fan_duty.set_ylim(0, 100)
    ax_fan_tach.set_ylabel("fan tach (RPM)", color='C1')
    ax_fan_tach.set_ylim(0, 5000)
    ax_fan_ctrl_temp.set_ylabel("fan control temp (degC)", color='C2')
    ax_fan_ctrl_temp.spines['right'].set_position(('outward', 60))
    ax_fan_ctrl_temp.set_ylim(20, 50)

    # turn on grid for all axes
    for ax in ax_tec_v, ax_temps, ax_leds_i, ax_fan_duty, ax_tec_p, ax_led_v, ax_fan_tach, ax_fan_ctrl_temp:
        ax.grid(True)

    line_tec0_v, = ax_tec_v.plot(times, tec0_volts, color='C0', label='TEC0 V')
    line_tec1_v, = ax_tec_v.plot(times, tec1_volts, color='C1', label='TEC1 V')
    line_tec_diff, = ax_tec_v.plot(times, tec_diffs, color='C2', label='TEC V diff')
    line_tot_p, = ax_tec_p.plot(times, total_pows, label='tot P', color='C3')
    line_tec_p, = ax_tec_p.plot(times, tec_pows, label='tec P', color='C4')
    line_led_p, = ax_tec_p.plot(times, led_pows, label='led P', color='C5')
    line_fan_p, = ax_tec_p.plot(times, fan_pows, label='fan P', color='C6')
    line_led_r_i_set, = ax_leds_i.plot(times, led_r_i_set, color='red', label='Red')
    line_led_g_i_set, = ax_leds_i.plot(times, led_g_i_set, color='green', label='Green')
    line_led_b_i_set, = ax_leds_i.plot(times, led_b_i_set, color='blue', label='Blue')
    line_led_w_i_set, = ax_leds_i.plot(times, led_w_i_set, color='black', label='White')
    line_led_r_v_drv, = ax_led_v.plot(times, led_r_v_drv, color='red', linestyle='--')
    line_led_g_v_drv, = ax_led_v.plot(times, led_g_v_drv, color='green', linestyle='--')
    line_led_b_v_drv, = ax_led_v.plot(times, led_b_v_drv, color='blue', linestyle='--')
    line_led_w_v_drv, = ax_led_v.plot(times, led_w_v_drv, color='black', linestyle='--')
    line_temp_hs_hot, = ax_temps.plot(times, temps_hs_hot, color='C0', label='HS hot')
    line_temp_hs_cold, = ax_temps.plot(times, temps_hs_cold, color='C1', label='HS cold')
    line_temp_lb_south_white, = ax_temps.plot(times, temps_lb_south_white, color='C2', label='LB south white')
    line_temp_lb_middle, = ax_temps.plot(times, temps_lb_middle, color='C3', label='LB middle')
    line_temp_lb_west_blue, = ax_temps.plot(times, temps_lb_west_blue, color='C4', label='LB west blue')
    line_temp_lb_north_white, = ax_temps.plot(times, temps_lb_north_white, color='C5', label='LB north white')
    line_temp_blue, = ax_temps.plot(times, temps_blue, color='C6', label='Blue driver')
    line_temp_red, = ax_temps.plot(times, temps_red, color='C7', label='Red driver')
    line_temp_fan_local, = ax_temps.plot(times, temps_fan_local, color='C8', label='Fan local')
    line_temp_fan_remote, = ax_temps.plot(times, temps_fan_remote, color='C9', label='Fan remote')
    line_fan_duty, = ax_fan_duty.plot(times, fan_duties, color='C0')
    line_fan_tach, = ax_fan_tach.plot(times, fan_tachs, color='C1')

    ax_tec_v.legend(loc='upper left', bbox_to_anchor=(0, 1), borderaxespad=0.)
    ax_tec_p.legend(loc='upper left', bbox_to_anchor=(1.15, 0.8), borderaxespad=0.)
    ax_leds_i.legend(loc='upper left', bbox_to_anchor=(1.15, 0.8), borderaxespad=0.)
    # makes sure the legend stays in the upper left
    ax_temps.legend(loc='upper left', bbox_to_anchor=(1, 1.05), borderaxespad=0.)

    fig.suptitle(f"Temperature control loop")

    begin = time.time()

    if auto_draw:
        plt.show()

    while True:
        if not auto_draw:
            plt.pause(0.01)
        if thread_messg_queue is not None:
            try:
                messg = thread_messg_queue.get_nowait()
                if messg == 'stop':
                    break
                elif messg == 'save':
                    plt.savefig(f"temp_control_latest.png")
            except Exception as e:
                pass
        status = ls.get_status(print_to_console=False)
        temps = status['temperatures']
        t_lb_south_white, t_lb_middle, t_lb_west_blue, t_lb_north_white = temps['lb_ntc_rt1'], temps['lb_ntc_rt2'], \
                                                                            temps['lb_ntc_rt3'], temps['lb_ntc_rt4']

        print(f"t_lb_middle: {t_lb_middle: .3f}")

        adc_value = status['sys_mon']
        high_volt = adc_value['jack_v'] / 1000
        total_c = adc_value['jack_i'] / 1000
        led0_v = adc_value['led0_v'] / 1000
        led1_v = adc_value['led1_v'] / 1000
        led2_v = adc_value['led2_v'] / 1000
        led3_v = adc_value['led3_v'] / 1000
        tec_0_v = adc_value['tec0_v'] / 1000
        tec_1_v = adc_value['tec1_v'] / 1000

        led0_i = ls.blue_a.value / 100 * 0.5
        led1_i = ls.green_a.value / 100 * 0.5
        led2_i = ls.white_a.value / 100 * 0.5
        led3_i = ls.red_a.value / 100 * 0.5

        t_hs_hot, t_driver_blue, t_driver_red, t_hs_cold = (temps['cb_ntc_j14'], temps['cb_ntc_led_ch0'],
                                                            temps['cb_ntc_led_ch3'], temps['cb_ntc_j13'])
        t_fan_local, t_fan_remote = temps['fan_local'], temps['fan_remote']

        fan_duty, fan_tach = status['fan']['duty_cycle'], status['fan']['rpm']

        fan_duties.append(fan_duty)
        fan_tachs.append(fan_tach)

        times.append(time.time() - begin)

        tec0_volts.append(tec_0_v)
        tec1_volts.append(tec_1_v)
        tec_diffs.append(tec_1_v - tec_0_v)
        total_pows.append(total_c * high_volt)
        led_pows.append(led0_v * led0_i + led1_v * led1_i + led2_v * led2_i + led3_v * led3_i)
        fan_pows.append(fan_duty * 0.07)  # very raw calc, todo improve
        tec_pows.append(total_pows[-1] - led_pows[-1] - fan_pows[-1])

        temps_hs_hot.append(t_hs_hot)
        temps_hs_cold.append(t_hs_cold)
        temps_lb_south_white.append(t_lb_south_white)
        temps_lb_middle.append(t_lb_middle)
        temps_lb_west_blue.append(t_lb_west_blue)
        temps_lb_north_white.append(t_lb_north_white)
        temps_blue.append(t_driver_blue)
        temps_red.append(t_driver_red)
        temps_fan_local.append(t_fan_local)
        temps_fan_remote.append(t_fan_remote)

        led_r_i_set.append(led3_i)
        led_g_i_set.append(led1_i)
        led_b_i_set.append(led0_i)
        led_w_i_set.append(led2_i)
        led_r_v_drv.append(led3_v)
        led_g_v_drv.append(led1_v)
        led_b_v_drv.append(led0_v)
        led_w_v_drv.append(led2_v)

        for line in line_tec0_v, line_tec1_v, line_tec_diff, line_tec_p, line_tot_p, line_led_p, line_fan_p:
            line.set_xdata(times)
        ax_tec_v.set_xlim(times[0], times[-1])
        line_tec0_v.set_ydata(tec0_volts)
        line_tec1_v.set_ydata(tec1_volts)
        line_tec_diff.set_ydata(tec_diffs)
        line_tec_p.set_ydata(tec_pows)
        line_tot_p.set_ydata(total_pows)
        line_led_p.set_ydata(led_pows)
        line_fan_p.set_ydata(fan_pows)

        for line in (line_led_r_i_set, line_led_g_i_set, line_led_b_i_set, line_led_w_i_set, line_led_r_v_drv,
                     line_led_g_v_drv, line_led_b_v_drv, line_led_w_v_drv):
            line.set_xdata(times)
        ax_leds_i.set_xlim(times[0], times[-1])
        line_led_r_i_set.set_ydata(led_r_i_set)
        line_led_g_i_set.set_ydata(led_g_i_set)
        line_led_b_i_set.set_ydata(led_b_i_set)
        line_led_w_i_set.set_ydata(led_w_i_set)
        line_led_r_v_drv.set_ydata(led_r_v_drv)
        line_led_g_v_drv.set_ydata(led_g_v_drv)
        line_led_b_v_drv.set_ydata(led_b_v_drv)
        line_led_w_v_drv.set_ydata(led_w_v_drv)

        for line in (line_temp_hs_hot, line_temp_hs_cold, line_temp_lb_south_white, line_temp_lb_middle,
                     line_temp_lb_west_blue, line_temp_lb_north_white, line_temp_blue, line_temp_red,
                     line_temp_fan_local, line_temp_fan_remote):
            line.set_xdata(times)
        line_temp_hs_hot.set_ydata(temps_hs_hot)
        line_temp_hs_cold.set_ydata(temps_hs_cold)
        line_temp_lb_south_white.set_ydata(temps_lb_south_white)
        line_temp_lb_middle.set_ydata(temps_lb_middle)
        line_temp_lb_west_blue.set_ydata(temps_lb_west_blue)
        line_temp_lb_north_white.set_ydata(temps_lb_north_white)
        line_temp_blue.set_ydata(temps_blue)
        line_temp_red.set_ydata(temps_red)

        for line in line_fan_duty, line_fan_tach:
            line.set_xdata(times)
        line_fan_duty.set_ydata(fan_duties)
        line_fan_tach.set_ydata(fan_tachs)

        if auto_draw:
            plt.draw()

if __name__ == "__main__":
    ls = LightSourceR2X4(wait_for_stable_temperature=False)
    # use pyside backend for matplotlib
    import matplotlib
    matplotlib.use('Qt5Agg')
    run(ls, auto_draw=False)
