#This code is meant for fun only and not to be used in the contest
#Need to have the twitter page up and auto refeshing
#Need to have a mac with a shortcut setup to send the code to the number
#Thank you!

import mss
import imageio
import pytesseract
import time
import os
import pyperclip
from subprocess import call

#Colors
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

#Opening Art
art = '''
        _________ .__    .__               __  .__         _________            .___                
        \_   ___ \|  |__ |__|_____   _____/  |_|  |   ____ \_   ___ \  ____   __| _/____            
        /    \  \/|  |  \|  \____ \ /  _ \   __\  | _/ __ \/    \  \/ /  _ \ / __ |/ __ \           
        \     \___|   Y  \  |  |_> >  <_> )  | |  |_\  ___/\     \___(  <_> ) /_/ \  ___/           
         \______  /___|  /__|   __/ \____/|__| |____/\___  >\______  /\____/\____ |\___  >          
                \/     \/   |__|                         \/        \/            \/    \/           
_________                       __   .__                _________               __                  
\_   ___ \____________    ____ |  | _|__| ____    ____ /   _____/__.__. _______/  |_  ____   _____  
/    \  \/\_  __ \__  \ _/ ___\|  |/ /  |/    \  / ___\\_____  <   |  |/  ___/\   __\/ __ \ /     \ 
\     \____|  | \// __ \\  \___|    <|  |   |  \/ /_/  >        \___  |\___ \  |  | \  ___/|  Y Y  \
 \______  /|__|  (____  /\___  >__|_ \__|___|  /\___  /_______  / ____/____  > |__|  \___  >__|_|  /
        \/            \/     \/     \/       \//_____/        \/\/         \/            \/      \/ 
'''

print(art)


#Define functions
def captureScreenshot(left, top, width, height, output_file):
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        imageio.imwrite(output_file, sct_img)

def extractTextFromScreenshot(image_path):
    image = pytesseract.image_to_string(image_path)
    return image

def processScreenshot(left, top, width, height):
    screenshot_file = "screenshot.png"
    captureScreenshot(left, top, width, height, screenshot_file)
    text = extractTextFromScreenshot(screenshot_file)
    return text

def makeSingleLine(text):
    return text.replace('\n', ' ').replace('\r', ' ')
    os.remove(screenshot_file)

#create gloabal variable to store the code
sentCode = ""

def sendCodeToChipotle(code):
    global sentCode

    if sentCode == code:
        print("Code already sent")
        return
    else:
        sentCode = code
        call(["shortcuts", "run", "ChipotleBurrito"])
        print("Code sent")


#set your capture area
captureAreaLeft = 100  
captureAreaTop = 700 
captureAreaWidth = 700 
captureAreaHeight = 400 

#Main loop
while True:
    
    text = processScreenshot(captureAreaLeft, captureAreaTop, captureAreaWidth, captureAreaHeight)
    text = makeSingleLine(text)
    text = text.lower()

    # Find the code in the text
    startWord = "text"
    endWord = "to"

    #Loop to look for the word we need
    index = text.find(startWord)
    if index != -1:
        stopIndex = text.find(endWord, index + len(startWord))
        if stopIndex != -1:
            code = text[index + 1 + len(startWord):stopIndex - 1]
            #make the clipboard copy the code
            code = code.upper()
            pyperclip.copy(code)
            print(f"{COLOR_GREEN}{code}{COLOR_RESET} Code has been copied to clipboard")
            sendCodeToChipotle(code)

    #Time asleep
    time.sleep(3)
