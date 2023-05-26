import math
import time

# There's an issue with importing cupy sometimes when you install the cupy_cuda11x version, I have no idea why :)
# I cannot install the 'cupy' package because Avast freaks out (a.exe) every time I try, and it's not worth disabling it.
import cupy as cp
from PIL import ImageGrab
from joblib import Parallel, delayed


def calculate_color_difference(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    # Calculate the square of the differences in each channel
    delta_r = (r2 - r1) ** 2
    delta_g = (g2 - g1) ** 2
    delta_b = (b2 - b1) ** 2

    # Calculate the Euclidean distance
    distance = math.sqrt(delta_r + delta_g + delta_b)

    return distance

def capture_frame(downsample_size):
    # Capture the screen image
    screen = ImageGrab.grab()

    # Downsample the image
    screen_resized = screen.resize(downsample_size)

    # Convert the image to a CuPy array
    screen_cp = cp.asarray(screen_resized)

    # Reshape the image array to a flat 1D array
    flat_image = screen_cp.reshape(-1, 3)

    return flat_image

def calculate_average_rgb(num_frames=2, downsample_size=(320, 240), num_jobs=-1):
    # Capture and process multiple frames in parallel
    frames = Parallel(n_jobs=num_jobs)(
        delayed(capture_frame)(downsample_size) for _ in range(num_frames)
    )

    # Combine frames into a single CuPy array
    flat_images = cp.vstack(frames)

    # Calculate the sum of RGB values
    total_rgb = cp.sum(flat_images, axis=0)
    pixel_count = flat_images.shape[0]

    # Calculate the average RGB value
    average_rgb = total_rgb // pixel_count

    # Convert average RGB to integers
    average_rgb = cp.asnumpy(average_rgb).astype(int)

    return tuple(average_rgb)


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

def screen_mirror(controller: object):
    prev = bytearray([1, 1, 1])
    while True:
        current = bytearray(calculate_average_rgb())

        for i in range(0, 100):
            controller.all_hue(bytearray(lerp_rgb(prev, current, i/100)))
            time.sleep(0.0001)

        prev = current
