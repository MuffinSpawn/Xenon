import time

from   adafruit_display_text import label
from   adafruit_hx8357 import HX8357
import adafruit_imageload
import adafruit_sdcard
from   adafruit_stmpe610 import Adafruit_STMPE610_SPI
import analogio
import board
import busio
import digitalio
import displayio
import storage
import terminalio


def main():
    spi = board.SPI()

    display = setup_display(spi)

    touch_screen = setup_touch_screen(spi)

    # distance_sensor = setup_distance_sensor()
    # led = setup_led()

    # while True:
    #     distance = meters_from_counts(distance_sensor.value)
    #
    #     led.value = False
    #     time.sleep(distance)
    #     led.value = True
    #     time.sleep(distance)

    print("Go Ahead - Touch the Screen - Make My Day!")
    while True:
        if not touch_screen.buffer_empty:
            print(touch_screen.read_data())


def setup_display(spi):
    # Release any resources currently in use for the displays
    displayio.release_displays()

    tft_cs = board.D4
    tft_dc = board.D5

    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

    display = HX8357(display_bus, width=480, height=320)

    # Make the display context
    # splash = displayio.Group(max_size=10)
    splash = displayio.Group()
    display.show(splash)

    # color_bitmap = displayio.Bitmap(480, 320, 1)
    # color_palette = displayio.Palette(1)
    # color_palette[0] = 0x00FF00  # Bright Green
    #
    # bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    # splash.append(bg_sprite)
    #
    # # Draw a smaller inner rectangle
    # inner_bitmap = displayio.Bitmap(440, 280, 1)
    # inner_palette = displayio.Palette(1)
    # inner_palette[0] = 0xAA0088  # Purple
    # inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
    # splash.append(inner_sprite)

    # # Draw a label
    # text_group = displayio.Group(max_size=10, scale=3, x=137, y=160)
    # text = "Hello World!"
    # text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    # text_group.append(text_area)  # Subgroup for text scaling
    # splash.append(text_group)

    mount_sd_card(spi, "/sd")
    import gc
    # print(gc.mem_free())

    image, palette = adafruit_imageload.load(
        "/sd/keypad_small.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
    )
    tile_grid = displayio.TileGrid(image, pixel_shader=palette)

    splash.append(tile_grid)

    return display


def setup_touch_screen(spi):
    cs = digitalio.DigitalInOut(board.D3)
    touch_screen = Adafruit_STMPE610_SPI(spi, cs)

    return touch_screen


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


def mount_sd_card(spi, mount_point):
    cs = digitalio.DigitalInOut(board.D2)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    sd_card_fs = storage.VfsFat(sdcard)

    storage.mount(sd_card_fs, mount_point)

main()
