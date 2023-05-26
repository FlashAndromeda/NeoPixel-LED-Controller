import serial

def before_after(index: int, max_range: int) -> tuple[int, int]:
    before = index - 1
    after = index + 1

    if before < 0:
        before = 0

    if after > max_range:
        after = max_range

    return before, after

def rgb(Red: int, Green: int, Blue: int) -> bytearray:
    return bytearray([Red, Green, Blue])

class Controller:
    def __init__(self):
        self.connection = serial.Serial()

        # Update these values in accordance with your setup.
        self.connection.baudrate = 115200
        self.connection.port = 'COM4'
        self.connection.open()

        self.numPixels: int = self.get_pixel_count() - 1

    def get_pixel_count(self) -> int:
        self.connection.write(bytearray([7]))
        count = int(self.connection.readline())

        return count

    def on(self):
        values = bytearray([0])
        self.connection.write(values)

    def off(self):
        values = bytearray([1])
        self.connection.write(values)

    def all_brightness(self, brightness: int):
        """
        Changes brightness of all pixels.
        :param brightness: Brightness value in range 0-255
        """
        if 0 > brightness > 255:
            raise Exception("Brightness value out of range (0-255)!")

        values = bytearray([2, brightness])
        self.connection.write(values)

    def all_hue(self, hue: bytearray):
        """
        Changes hue of all pixels.
        :param hue: Bytearray of RGB channel values eg. [255, 255, 255].
        """
        # hue = [hue_R, hue_G, hue_B]
        for channel in hue:
            if 0 > channel > 255:
                raise Exception(f'Hue value {hue} out of range (0-255)!')

        values = bytearray([3]) + hue
        self.connection.write(values)

    def one_pixel_hue(self, pixel_id: int, hue: bytearray):
        """
        Changes hue of one specific pixel.
        :param pixel_id: Index of the pixel.
        :param hue: Bytearray of RGB channel values eg. [255, 255, 255].
        """
        for channel in hue:
            if 0 > channel > 255:
                raise Exception(f'Hue value {hue} out of range (0-255)!')

        values = bytearray([4, pixel_id]) + hue
        self.connection.write(values)

    def pixel_range_hue(self, range_start: int, range_end: int, hue: bytearray):
        """
        Changes hue of a range of pixels.
        :param range_start:
        :param range_end:
        :param hue: Bytearray of RGB channel values eg. [255, 255, 255].
        """
        for channel in hue:
            if 0 > channel > 255:
                raise Exception(f'Hue value {hue} out of range (0-255)!')

        if range_start > range_end:
            raise Exception(f"range_start({range_start}) cannot be higher than range_end({range_end})!")

        if range_start < 0:
            raise Exception(f"range_start({range_start}) cannot be negative!")

        values = bytearray([5, range_start, range_end]) + hue
        self.connection.write(values)

    def reset(self):
        """
        Resets all LEDs to default brightness and RGB(1, 1, 1).
        """
        self.connection.write(bytearray([6]))

def main(led):
    # Import and initialize your effect here
    from effects import screen_mirror
    screen_mirror.screen_mirror(led)

if __name__ == "__main__":
    main(Controller())
