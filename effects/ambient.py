from time import sleep

class Color:
    def __init__(self, color: bytearray):
        red, green, blue = color
        self.r = red
        self.g = green
        self.b = blue

    def to_bytearray(self):
        return bytearray([self.r, self.g, self.b])

def lerp_rgb(color1: bytearray, color2: bytearray, t: float) -> list[int, int, int]:
    """
    Lerps between two colors.
    :param color1: Bytearray of RGB values for the first color.
    :param color2: Bytearray of RGB values for the second color.
    :param t: Step value (t=0 returns color1, t=1 returns color2).
    :return: Returns a list of RGB values [R, G, B].
    """
    a = Color(color1)
    b = Color(color2)

    red = int(a.r + (b.r - a.r)*t)
    green = int(a.g + (b.g - a.g)*t)
    blue = int(a.b + (b.b - a.b)*t)

    return [red, green, blue]


def ambient(Controller: object, speed: int):
    """
    Smoothly changes the hue of all LEDs across the entire RGB spectrum.

    :param Controller: Controller class object used to communicate with the LEDs
    :param speed: Speed of the effect.
    """
    c1 = bytearray([255,0,0])
    c2 = bytearray([255,0,255])
    c3 = bytearray([0,0,255])
    c4 = bytearray([0,255,255])
    c5 = bytearray([0,255,0])
    c6 = bytearray([255,255,0])
    c7 = bytearray([255,0,0])

    speed_param: float = 0.000001

    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c1, c2, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c2, c3, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c3, c4, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c4, c5, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c5, c6, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c6, c7, i / 100)))
        sleep(speed_param/speed)
    for i in range(0, 100):
        Controller.all_hue(hue=bytearray(lerp_rgb(c7, c1, i / 100)))
        sleep(speed_param/speed)