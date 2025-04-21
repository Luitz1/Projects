/*
 * Arduino Leonardo Text File Creator for Windows - C Version
 * ---------------------------------------------
 * This code emulates keyboard actions to:
 * 1. Open CMD 
 * 2. Create a text file on desktop with message "Hello I was here"
 * 3. Save and close everything
 */

#include <Arduino.h>
#include "Keyboard.h"

// ----- CONSTANTS AND DEFINITIONS -----
#define INITIAL_DELAY 2000    // Initial boot delay in milliseconds
#define SETUP_DELAY 5000      // Setup delay before keyboard action starts
#define KEY_PRESS_TIME 100    // Time to hold a key down in milliseconds
#define SHORT_DELAY 50        // Short delay between actions
#define MEDIUM_DELAY 300      // Medium delay between actions
#define LONG_DELAY 500        // Long delay for application loading
#define ENTER_KEY 0xB0        // Enter key code

// ----- FUNCTION PROTOTYPES -----
void pressAndRelease(uint8_t key);
void pressKeyCombination(uint8_t modifier, char key);
void typeAndEnter(const char* text);

void setup(void) {
  // ----- INITIALIZATION PHASE -----
  delay(INITIAL_DELAY);       // Wait for the board to fully initialize
  Keyboard.begin();           // Initialize keyboard emulation
  delay(SETUP_DELAY);         // Additional delay before executing keyboard commands
  
  // ----- OPEN RUN DIALOG -----
  pressKeyCombination(KEY_RIGHT_GUI, 'r');
  delay(MEDIUM_DELAY);
  
  // ----- LAUNCH COMMAND PROMPT -----
  typeAndEnter("cmd");
  delay(LONG_DELAY);
  
  // ----- CREATE TEXT FILE ON DESKTOP -----
  typeAndEnter("echo Hello I was here > %USERPROFILE%\\Desktop\\message.txt");
  delay(MEDIUM_DELAY);
  
  // ----- CLOSE CMD WINDOW -----
  typeAndEnter("exit");
}

void loop(void) {
  // ----- MAIN LOOP (EMPTY) -----
}

// ----- UTILITY FUNCTIONS -----

/*
 * Function to press and release a single key
 * key - The key to press and release
 */
void pressAndRelease(uint8_t key) {
  Keyboard.press(key);
  delay(KEY_PRESS_TIME);
  Keyboard.releaseAll();
}

/*
 * Function to press a combination of modifier + key
 * modifier - The modifier key (CTRL, ALT, GUI, etc.)
 * key - The key to press with the modifier
 */
void pressKeyCombination(uint8_t modifier, char key) {
  Keyboard.press(modifier);
  Keyboard.press(key);
  delay(KEY_PRESS_TIME);
  Keyboard.releaseAll();
}

/*
 * Function to type text and press Enter
 * text - The text to type before pressing Enter
 */
void typeAndEnter(const char* text) {
  Keyboard.print(text);
  delay(SHORT_DELAY);
  pressAndRelease(ENTER_KEY);
}