/*
 * Arduino Leonardo Text File Creator for Windows
 * ---------------------------------------
 * This sketch emulates a keyboard to:
 * 1. Open CMD
 * 2. Create a text file on desktop with message "Hello I was here"
 * 3. Save and close everything
 */

 #include "Keyboard.h"

 // ----- CONSTANTS AND DEFINITIONS -----
 const int INITIAL_DELAY = 2000;    // Initial boot delay in milliseconds
 const int SETUP_DELAY = 5000;      // Setup delay before keyboard action starts
 const int KEY_PRESS_TIME = 100;    // Time to hold a key down in milliseconds
 const int SHORT_DELAY = 50;        // Short delay between actions
 const int MEDIUM_DELAY = 300;      // Medium delay between actions
 const int LONG_DELAY = 500;        // Long delay for application loading
 const int ENTER_KEY = 0xB0;        // Enter key code
 
 void setup() {
   // ----- INITIALIZATION PHASE -----
   delay(INITIAL_DELAY);
   Keyboard.begin();
   delay(SETUP_DELAY);
   
   // ----- OPEN RUN DIALOG -----
   Keyboard.press(KEY_RIGHT_GUI);   // Press Windows key
   Keyboard.press('r');             // Press 'r' key for Run dialog
   delay(KEY_PRESS_TIME);           // Wait while keys are pressed
   Keyboard.releaseAll();           // Release all pressed keys
   delay(MEDIUM_DELAY);             // Wait for run dialog to open
   
   // ----- LAUNCH COMMAND PROMPT -----
   Keyboard.print("cmd");
   delay(SHORT_DELAY);
   Keyboard.press(ENTER_KEY);
   delay(KEY_PRESS_TIME);
   Keyboard.releaseAll();
   delay(LONG_DELAY);
   
   // ----- CREATE TEXT FILE ON DESKTOP -----
   // Echo command to create text file with message
   Keyboard.print("echo Hello I was here > %USERPROFILE%\\Desktop\\message.txt");
   delay(SHORT_DELAY);
   Keyboard.press(ENTER_KEY);
   delay(KEY_PRESS_TIME);
   Keyboard.releaseAll();
   delay(MEDIUM_DELAY);
   
   // ----- CLOSE CMD WINDOW -----
   Keyboard.print("exit");
   delay(SHORT_DELAY);
   Keyboard.press(ENTER_KEY);
   delay(KEY_PRESS_TIME);
   Keyboard.releaseAll();
 }
 
 void loop() {
   // ----- MAIN LOOP (EMPTY) -----
 }