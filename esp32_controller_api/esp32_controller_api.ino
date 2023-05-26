#include <Adafruit_NeoPixel.h>
#include <string.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Change these values in accordance with your controller setup
#define PIN        18
#define NUMPIXELS 24

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500

void setup() {
  // Make sure your baudrate here is the same as in main.py
  Serial.begin(115200);

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();

  pixels.setBrightness(150);
}

void loop() {
  if(Serial.available() > 0) {
    byte command = Serial.read();

    switch(command) {
      // [0]
      case 0: //All On
      {
        Serial.println("All LEDs On");
        pixels.setBrightness(170);
        pixels.show();
        break;
      }
      // [1]
      case 1: //All Off
      {
        Serial.println("All LEDs Off");
        pixels.setBrightness(1);
        pixels.show();
        break;
      }
      // [2][VAL]
      case 2: //All Brightness
      {
        Serial.println("Brightness of all LEDs changed!");
        int brightness = Serial.read();

        pixels.setBrightness(brightness);
        pixels.show();
        break;
      }
      // [3][R][G][B]
      case 3: //All Hue
      {
        
        Serial.println("Hue of all LEDs changed!");
        int hue_R = Serial.read();
        int hue_G = Serial.read();
        int hue_B = Serial.read();

        for(int i=0; i<pixels.numPixels(); i++)
        { 
          pixels.setPixelColor(i, pixels.Color(hue_R, hue_G, hue_B));
        }
        pixels.show();
        break;
      }
      // [4][ID][R][G][B]
      case 4: //One Pixel Hue
      {
        Serial.println("One Pixel Hue");
        int pixel_id = Serial.read();

        if (pixel_id > pixels.numPixels()) {
          Serial.println("Pixel ID out of range!");
          break;
        }

        int hue_R = Serial.read();
        int hue_G = Serial.read();
        int hue_B = Serial.read();

        pixels.setPixelColor(pixel_id, pixels.Color(hue_R, hue_G, hue_B));
        pixels.show();
        break;
      }
      // [5][ID][ID][R][G][B]
      case 5: //Pixel Range Hue
      {
        int range_start = Serial.read(); // Start of pixel range
        int range_end = Serial.read();

        int hue_R = Serial.read();
        int hue_G = Serial.read();
        int hue_B = Serial.read();

        for (int i=range_start; i <= range_end; i++) {
          pixels.setPixelColor(i, pixels.Color(hue_R, hue_G, hue_B));
        }

        pixels.show();
        break;
      }
      // [6]
      case 6: // Reset all pixels
      {
        pixels.setBrightness(170);
        blank();
      }
      case 7: //Get numPixels information
      {
        Serial.println(pixels.numPixels());
        break;
      }
      default:
      {
        Serial.println(command, DEC);
      }
    }
  }
}

void blank() {
  for(int i=0; i<pixels.numPixels(); i++) { 
    pixels.setPixelColor(i, pixels.Color(1, 1, 1));
  }
  pixels.show();
}