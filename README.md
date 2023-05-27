# NeoPixel-LED-Controller
This project was created to solve one simple issue. 

What if you had a NeoPixel LED strip running on an ESP32 controller hooked up to your PC through a USB port by a cable running from inside your case, through the backplate and into the back USB port?

**The LEDs, the controller, the DYI soldering job on the controller, the boilerplate code for the API and a lot of advice I owe to my good friend [@boreq](https://github.com/boreq)**

## Files
* `.\effects\` contains scripts you run for different effects for your LEDs
* `.\esp32_controller_api\` contains the code for the API that should run on your ESP32 controller.
* `.\main.py` runs your LED effects

## Installing
### Configuring the ESP32 API
1. Download the Arduino IDE from [their website.](https://www.arduino.cc/en/software)
2. Download and install the [Espressif library](https://espressif-docs.readthedocs-hosted.com/projects/arduino-esp32/en/latest/installing.html) for Arduino-ESP32 support. Follow the install instructions for the Arduino IDE on the website.
3. Open the IDE and open the sketch in the `esp32_controller_api` folder,
4. In your IDE, go into the Library Manager and install the **Adafruit NeoPixel** library by Adafruit (v1.11.0 for me),
5. In the IDE, in `Tools > Board > esp32` select `ESP32 Dev Module`
*note: You might have to try out different boards, that one is what worked for me.*
6. In `Tools > Port` select the port that your device is connected to. *In my case, I needed to download the CP2102 USB to UART Bridge Driver from [here.](https://www.usb-drivers.org/cp2102-usb-to-uart-bridge-driver.html#CP2102_to_UART_Bridge_Driver_%E2%80%93_Linux)*
7. In the API code, change the values for:
* `NUMPIXELS` - number of LEDs you have in your strip.
* `PIN` - which pin on the controller is the strip hooked up to.
* `NEO_GRB+NEO_KHZ800` string - the string depends on which type of LEDs you have, read the [Adafruit NeoPixel library documentation](https://adafruit.github.io/Adafruit_NeoPixel/html/_adafruit___neo_pixel_8h.html#ab88a50d51bb5488df4379ff49c81fd72) for more information.
8. Click "Upload" and after it finishes, you should be done with this part.

*Do not use the built-in Serial Monitor as it sends data as byte-encoded ASCII characters instead of raw bytes that are necessary for the API. This alone was responsible for at least 3h of troubleshooting.*

### Configuring the python script.
1. Install all packages from requirements.txt

      *There are issues with importing the cupy package, I have no idea why :)*
2. Change the values in the `Controller` class for:
* `self.connection.baudrate` - baudrate of your serial connection, make sure it's the same as in the API
* `self.connection.port` - name of the port that your controller is hooked up to
3. In the `main(led)` function import whichever effect you want to run and then run it. You're done!

## Plans for the Future
I hope to expand the script by adding a GUI for controlling the effects in real-time.
An important thing as well is adding parity checking in the API to make sure all data is transmitted correctly since with the screen_mirror effect I encountered issues that I suspect might've been caused by some bytes being lost on the way and commands being 'misunderstood'.

I will need to optimize the screen_mirror effect to lower the latency and possibly switch to calculating the dominant color on the screen, instead of averaging across all pixel colors.
Another change I wish to make to that effect is have the `current` color update in real-time but the color sent to the LEDs be 'chasing' that color in the RGB space with some latency and smoothing. That would ensure any changes on the screen would be reflected in the LEDs immediately while maintaining the smoothness of the effect.

Obviously more effects would be nice :) (for example, changing the hue depending on the current audio loudness or GPU/CPU temperatures)

## Known Issues
`cupy` import often breaks.

`serial` sometimes breaks but I've found reinstalling both `serial` and `pyserial` fixes that.

The screen_mirror effect sometimes crashes when Pillow has trouble grabbing the screen image. This can be fixed by running the script in administrator mode.

The effect can sometimes straight-up die but it shouldn't happen anymore since I rewrote the code a bit. If it happens, just restart the script.

It also sometimes causes flickering and weirdly, when the screen is too red, it can cause brief pure-blue flashes. I suspect this is to do with bytes going missing or arriving out of order (if that's even possible?) but I'll have to include parity checking to be sure.
