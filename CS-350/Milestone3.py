#
# Milestone3.py - This is the Python code template used to 
# setup the structure for Milestone 3. In this milestone, you need
# to demonstrate the capability to display a message in Morse code
# using red (dots) and blue (dashes) LEDs. The message changes between
# SOS and OK when the button is pressed using a state machine.
#
# ------------------------------------------------------------------
# Change History
# ------------------------------------------------------------------
# Version   |   Description
# ------------------------------------------------------------------
#    1      |   Initial Development
#    2      |   Revised code to address LCD cleanup errors and nested loop issues.
#    3      |   Revised transmission loop to update the LCD without repeatedly
#           |   clearing or deinitializing the display.
# ------------------------------------------------------------------

from gpiozero import Button, LED
from statemachine import StateMachine, State
from time import sleep
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from threading import Thread

DEBUG = True

# When testing LCD issues (wiring/contrast) you may set:
USE_LCD = True


class ManagedDisplay():
    def __init__(self):
        if not USE_LCD:
            return

        # Setup GPIO lines for the LCD.
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        # Set the dimensions for the LCD before initializing it.
        self.lcd_columns = 16
        self.lcd_rows = 2

        try:
            self.lcd = characterlcd.Character_LCD_Mono(
                self.lcd_rs, self.lcd_en,
                self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
                self.lcd_columns, self.lcd_rows
            )
            # Clear the display on init.
            self.lcd.clear()
        except Exception as e:
            if DEBUG:
                print("Warning: Initializing LCD failed:", e)
            self.lcd = None

    def cleanupDisplay(self):
        if not USE_LCD or self.lcd is None:
            return
        try:
            self.lcd.clear()
        except Exception as e:
            if DEBUG:
                print("Warning: lcd.clear() in cleanupDisplay failed:", e)
        # Deinitialize all LCD GPIO lines (only once at termination)
        for gpio in [self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7]:
            try:
                gpio.deinit()
            except Exception as e:
                if DEBUG:
                    print(f"Warning: deinitializing {gpio} failed:", e)

    def updateScreen(self, message):
        if not USE_LCD or self.lcd is None:
            return
        try:
            self.lcd.clear()  # Clear entire display first.
            self.lcd.message = message
        except Exception as e:
            if DEBUG:
                print("Warning: lcd.message update failed:", e)


class CWMachine(StateMachine):
    "A state machine to display Morse code messages using LEDs."
    redLight = LED(18)
    blueLight = LED(23)

    message1 = 'SOS'
    message2 = 'OK'
    activeMessage = message1
    endTransmission = False

    off = State(initial=True)
    dot = State()
    dash = State()
    dotDashPause = State()
    letterPause = State()
    wordPause = State()

    # Create the managed display.
    screen = ManagedDisplay()

    # Morse code dictionary.
    morseDict = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..",
        "E": ".", "F": "..-.", "G": "--.", "H": "....",
        "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.",
        "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
        "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----",
        "2": "..---", "3": "...--", "4": "....-", "5": ".....",
        "6": "-....", "7": "--...", "8": "---..", "9": "----.",
        "+": ".-.-.", "-": "-....-", "/": "-..-.", "=": "-...-",
        ":": "---...", ".": ".-.-.-", "$": "...-..-", "?": "..--..",
        "@": ".--.-.", "&": ".-...", "\"": ".-..-.", "_": "..--.-",
        "|": "--...-", "(": "-.--.-", ")": "-.--.-"
    }

    # Define event transitions.
    doDot = off.to(dot) | dot.to(off)
    doDash = off.to(dash) | dash.to(off)
    doDDP = off.to(dotDashPause) | dotDashPause.to(off)
    doLP = off.to(letterPause) | letterPause.to(off)
    doWP = off.to(wordPause) | wordPause.to(off)

    def on_enter_dot(self):
        if DEBUG:
            print("* Changing state to red - dot")
        self.redLight.on()
        sleep(0.5)
        self.redLight.off()

    def on_exit_dot(self):
        self.redLight.off()

    def on_enter_dash(self):
        if DEBUG:
            print("* Changing state to blue - dash")
        self.blueLight.on()
        sleep(1.5)
        self.blueLight.off()

    def on_exit_dash(self):
        self.blueLight.off()

    def on_enter_dotDashPause(self):
        if DEBUG:
            print("* Pausing Between Dots/Dashes - 250ms")
        sleep(0.25)

    def on_exit_dotDashPause(self):
        pass

    def on_enter_letterPause(self):
        if DEBUG:
            print("* Pausing Between Letters - 750ms")
        sleep(0.75)

    def on_exit_letterPause(self):
        pass

    def on_enter_wordPause(self):
        if DEBUG:
            print("* Pausing Between Words - 3000ms")
        sleep(3.0)

    def on_exit_wordPause(self):
        pass

    def toggleMessage(self):
        if self.activeMessage == self.message1:
            self.activeMessage = self.message2
        else:
            self.activeMessage = self.message1
        if DEBUG:
            print(f"* Toggling active message to: {self.activeMessage}")

    def processButton(self):
        print('*** processButton')
        self.toggleMessage()

    def run(self):
        myThread = Thread(target=self.transmit)
        myThread.start()

    def transmit(self):
        while not self.endTransmission:
            # Update the LCD with the current active message.
            self.screen.updateScreen(f"Sending:\n{self.activeMessage}")

            # Break the active message into words.
            wordList = self.activeMessage.split()
            lenWords = len(wordList)
            wordsCounter = 1

            for word in wordList:
                lenWord = len(word)
                wordCounter = 1

                for char in word:
                    morse = self.morseDict.get(char)
                    lenMorse = len(morse)
                    morseCounter = 1

                    for symbol in morse:
                        if symbol == '.':
                            self.doDot()
                            self.doDot()
                        elif symbol == '-':
                            self.doDash()
                            self.doDash()
                        if morseCounter < lenMorse:
                            self.doDDP()
                            self.doDDP()
                        morseCounter += 1

                    if wordCounter < lenWord:
                        self.doLP()
                        self.doLP()
                        wordCounter += 1

                if wordsCounter < lenWords:
                    self.doWP()
                    self.doWP()
                    wordsCounter += 1

            # Pause briefly between full transmission cycles.
            sleep(2)


# End CWMachine definition

# Begin execution.
cwMachine = CWMachine()
cwMachine.run()

greenButton = Button(24)
greenButton.when_pressed = cwMachine.processButton

# Main loop: we keep the program alive until keyboard interrupt.
repeat = True
try:
    while repeat:
        if DEBUG:
            print("Killing time in a loop...")
        sleep(20)
except KeyboardInterrupt:
    print("Cleaning up. Exiting...")
    repeat = False
    cwMachine.endTransmission = True
    # Only perform LCD cleanup once at exit.
    cwMachine.screen.cleanupDisplay()
    sleep(1)
