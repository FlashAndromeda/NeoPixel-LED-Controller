from time import sleep

def rgb(Red, Green, Blue):
    return bytearray([Red, Green, Blue])

def soften_hue(amount, hue: bytearray) -> bytearray:
    hue_r: int
    hue_g: int
    hue_b: int

    hue_r, hue_g, hue_b = hue

    hue_r = int(hue_r * amount)
    hue_g = int(hue_g * amount)
    hue_b = int(hue_b * amount)


    return bytearray([hue_r, hue_g, hue_b])

def before_after(index: int, max_range: int) -> tuple[int, int]:
    before = index-1
    after = index + 1

    if before < 0:
        before = 0
    if after > max_range:
        after = max_range

    return before, after
def bounce(controller: object, numPixels, speed: int, hue: bytearray, background_hue: bytearray = None):
    """
    Creates a bouncing pixel!

    :param controller: Controller object.
    :param numPixels: Number of pixels in the LED strip.
    :param speed: Determines the speed of the pixel
    :param hue: Tuple of RGB channel values for the marching pixel.
    :param background_hue: Tuple of RGB channel values for the background.
    """

    speed_param = 0.05
    for i in range(0, numPixels):
        before, after = before_after(i, numPixels)
        controller.one_pixel_hue(before, soften_hue(0.1, hue))
        controller.one_pixel_hue(i, hue)
        controller.one_pixel_hue(after, soften_hue(0.1, hue))
        sleep(speed_param/speed)

        if background_hue:
            controller.all_hue(background_hue)
        else:
            controller.reset()

    for i in range(0, numPixels):
        before, after = before_after(i, numPixels)
        controller.one_pixel_hue(numPixels - before, soften_hue(0.1, hue))
        controller.one_pixel_hue(numPixels - i, hue)
        controller.one_pixel_hue(numPixels - after, soften_hue(0.1, hue))
        sleep(speed_param/speed)

        if background_hue:
            controller.all_hue(background_hue)
        else:
            controller.reset()