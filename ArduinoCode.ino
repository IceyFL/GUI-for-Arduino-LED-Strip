#include <FastLED.h>

#define LED_PIN           5
#define NUM_LEDS          60
#define BRIGHTNESS        64
#define LED_TYPE          WS2811
#define COLOR_ORDER       GRB
#define UPDATES_PER_SECOND 100

CRGB leds[NUM_LEDS];
CRGBPalette16 currentPalette;
TBlendType currentBlending;

CRGB myColors[2];

void setup() {
    Serial.begin(9600);
    delay(3000); // Power-up safety delay

    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS);

    // Set initial colors (modify as needed)
    setColors(CRGB::Red, CRGB::White);

    currentPalette = CRGBPalette16(
        myColors[0], myColors[0], myColors[0], myColors[0],
        myColors[1], myColors[1], myColors[1], myColors[1],
        myColors[1], myColors[1], myColors[1], myColors[1],
        myColors[1], myColors[1], myColors[1], myColors[1]
    );
}

void loop() {
    static uint8_t startIndex = 0;
    startIndex += 3; /* motion speed */

    // Update current palette based on incoming data
    updatePalette();

    // Update LED colors
    FillLEDsFromPaletteColors(startIndex);

    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void updatePalette() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        // Split the input into two color names
        int spaceIndex = input.indexOf(' ');
        if (spaceIndex != -1) {
            String color1 = input.substring(0, spaceIndex);
            String color2 = input.substring(spaceIndex + 1);

            // Set colors based on input
            setColors(parseColor(color1), parseColor(color2));
        }
    }
}

void FillLEDsFromPaletteColors(uint8_t colorIndex) {
    uint8_t brightness = 255;

    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette(currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}

void setColors(const CRGB &color1, const CRGB &color2) {
    // Update the myColors array
    myColors[0] = color1;
    myColors[1] = color2;

    // Update the palette colors directly
    currentPalette = CRGBPalette16(
        color1, color1, color1, color1,
        color2, color2, color2, color2,
        color2, color2, color2, color2,
        color2, color2, color2, color2
    );
}

CRGB parseColor(const String &colorName) {
    // Set default color to black
    CRGB defaultColor = CRGB::Black;

    // Set color based on input
    if (colorName.equalsIgnoreCase("Red")) return CRGB::Red;
    if (colorName.equalsIgnoreCase("Green")) return CRGB::Green;
    if (colorName.equalsIgnoreCase("Blue")) return CRGB::Blue;
    if (colorName.equalsIgnoreCase("Yellow")) return CRGB::Yellow;
    if (colorName.equalsIgnoreCase("Brown")) return CRGB::Brown;
    if (colorName.equalsIgnoreCase("Orange")) return CRGB::Orange;
    if (colorName.equalsIgnoreCase("Pink")) return CRGB::DeepPink;
    if (colorName.equalsIgnoreCase("Purple")) return CRGB::Purple;
    if (colorName.equalsIgnoreCase("Cyan")) return CRGB::Cyan;
    if (colorName.equalsIgnoreCase("Beige")) return CRGB::Beige;
    if (colorName.equalsIgnoreCase("Turquoise")) return CRGB::Turquoise;
    if (colorName.equalsIgnoreCase("Navy")) return CRGB::Navy;
    if (colorName.equalsIgnoreCase("Olive")) return CRGB::Olive;
    if (colorName.equalsIgnoreCase("Maroon")) return CRGB::Maroon;
    if (colorName.equalsIgnoreCase("Teal")) return CRGB::Teal;
    if (colorName.equalsIgnoreCase("Salmon")) return CRGB::Salmon;
    if (colorName.equalsIgnoreCase("Coral")) return CRGB::Coral;
    if (colorName.equalsIgnoreCase("Lavender")) return CRGB::Lavender;
    if (colorName.equalsIgnoreCase("Gray")) return CRGB::Gray;
    if (colorName.equalsIgnoreCase("White")) return CRGB::White;

    return defaultColor;
}
