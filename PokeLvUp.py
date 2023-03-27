import numpy as np
from PIL import Image, ImageGrab
import cv2
import time
import pyautogui as botbom
import pytesseract

'''
This only works in ROUTE 7 in the 3th bottom grass from left to right, right above the guard from Saffron city.
this is a very simple script I made by videos and forums from Internet, so it may have bugs. You can adjust the number 
of your pokemon's PP and pretty much everything actually. The control is based in 'POKEMMO' which is the game I tested. 
'''

#reset after a battle
def reset(numberOfSearches):
    if(numberOfSearches >= 1):
        botbom.keyDown('s')
        time.sleep(.15)
        botbom.keyUp('s')
        time.sleep(.1)


def runAway():
    botbom.keyDown('s')
    time.sleep(.03)
    botbom.keyUp('s')
    time.sleep(.1)
    botbom.keyDown('d')
    time.sleep(.03)
    botbom.keyUp('d')
    time.sleep(.1)
    botbom.keyDown('e')
    time.sleep(.03)
    botbom.keyUp('e')
    time.sleep(.1)
    botbom.keyDown('e')
    time.sleep(.03)
    botbom.keyUp('e')
    time.sleep(.1)

def spamButton(Button, durationInSeconds):
    timeEnd = time.time() + durationInSeconds
    while (time.time() <  timeEnd):
        botbom.keyDown(Button)
        time.sleep(.03)
        botbom.keyUp(Button)
        time.sleep(.1)

def findWildPokemon():
    botbom.keyDown('w');
    time.sleep(.2);
    botbom.keyUp('w');
    time.sleep(1);
    botbom.keyDown('s');
    time.sleep(.2);
    botbom.keyUp('s');
    time.sleep(1);

def heal():
    botbom.keyDown('s');
    time.sleep(.6);
    botbom.keyUp('s');
    time.sleep(1);
    botbom.keyDown('a');
    time.sleep(1.7);
    botbom.keyUp('a');
    time.sleep(1);
    botbom.keyDown('w');
    time.sleep(2);
    botbom.keyUp('w');
    time.sleep(1);
    botbom.keyDown('a');
    time.sleep(4.7);
    botbom.keyUp('a');
    time.sleep(1);
    botbom.keyDown('w');
    time.sleep(3);
    botbom.keyUp('w');
    time.sleep(1);
    spamButton('e', 4)
    time.sleep(1)
    #goingback
    botbom.keyDown('s');
    time.sleep(2);
    botbom.keyUp('s');
    time.sleep(1);
    botbom.keyDown('d');
    time.sleep(4.7);
    botbom.keyUp('d');
    time.sleep(1);
    botbom.keyDown('s');
    time.sleep(2);
    botbom.keyUp('s');
    time.sleep(1);
    botbom.keyDown('d');
    time.sleep(1.7);
    botbom.keyUp('d');
    time.sleep(1);
    botbom.keyDown('w');
    time.sleep(.46);
    botbom.keyUp('w');
    time.sleep(1);

#dumbing down (narrowing) image down
def roi(img, vertices):
    mask = np.zeros_like(img) #returning array of zeros
    cv2.fillPoly(mask, vertices, 255) #fill with polygons
    masked = cv2.bitwise_and(img, mask) #take only the region from logo image
    return masked

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY);
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300);
    vertices = np.array([[10,500], [10,300],[800,300], [800,500]]);
    processed_img = roi(processed_img, [vertices])
    return processed_img;

#getting text to check the instance (combat or searching)
def get_text(img):
    text = pytesseract.image_to_string(img)
    return text


#wait time
for i in list(range(4)) [::-1]:
     print(i+1);
     time.sleep(1);



numberOfSearches = 0
PP = 4
last_time = time.time();
while(True):
    #grabing image (north left, 1920x1080 monitor) and analising it
    screen = np.array(ImageGrab.grab(bbox=(0,50,890,715)));
    new_screen = process_img(screen);
    text = get_text(new_screen);

    cv2.imshow('window', new_screen);
    #auto level, run in case of horde and kill in case of single pokemon
    if (PP > 0):
        if('horde' in text and ('apeeared' in text or 'appeared' in text)):
            print(text)
            time.sleep(4)
            runAway();
        elif('wild' in text and ('apeeared' in text or 'appeared' in text)):
            print(text)
            print('KILLING EVERYONE HAHAHA')
            spamButton('e', 20)

            PP = PP - 1
            print('PP =', PP)

            if(PP == 0):
                numberOfSearches = 0
                time.sleep(6)
                heal();
                PP = 10;
            else:
                time.sleep(2)
                print('reset')
                reset(numberOfSearches)
                numberOfSearches = 0
        else:
            findWildPokemon();
            numberOfSearches += 1
            print('Searched = ', numberOfSearches)

    #quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows();
        break;
