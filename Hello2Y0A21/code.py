import time

import analogio
import board
import digitalio


def main():
    distance_sensor = setup_distance_sensor()
    led = setup_led()

    while True:
        distance = meters_from_counts(distance_sensor.value)

        led.value = False
        time.sleep(distance)
        led.value = True
        time.sleep(distance)


def setup_distance_sensor():
    return analogio.AnalogIn(board.A0)


def setup_led():
    led = digitalio.DigitalInOut(board.BLUE_LED)
    led.direction = digitalio.Direction.OUTPUT

    return led


def meters_from_counts(counts):
    # 3.1V at 10cm to 0.4V at 80cm
    # ~15000@10cm - ~45000@10cm
    slope = (0.8 - 0.1) / (15000 - 45000)
    y_intercept = 0.8 - (slope * 15000)

    return y_intercept + slope * counts


main()
