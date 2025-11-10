#OLED
import adafruit_displayio_ssd1306
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import terminalio
import board

def instantiate_OLED():
    displayio.release_displays()

    i2c = busio.I2C (scl=board.GP17, sda=board.GP16) # This RPi Pico way to call I2C
    display_bus = displayio.I2CDisplay(i2c, device_address = 0x3C) # The address of my Board
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
    splash = displayio.Group()
    display.show(splash)

    # Draw white background
    color_bitmap = displayio.Bitmap(128, 36, 1) # Full screen white
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # White
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a label
    text = "Error!\ndo better"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=0, y=10)

    # size of text as int(1 is the smallest)
    text_area.scale = 1
    splash.append(text_area)

    while True:
        pass
