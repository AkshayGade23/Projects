import cv2
import numpy as np 
import time
from keys import *
from handTracker import *
from pynput.keyboard import Controller
import pyautogui
# from app7 import main_loop

def getMousPos(event , x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        #print(x,y)
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
    #     print(x,y)
        mouseX, mouseY = x, y

def calculateIntDidtance(pt1, pt2):
    return int(((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)**0.5)




# Creating keys
w,h = 80, 60
startX, startY = 40, 200
keys=[]
letters =list("QWERTYUIOPASDFGHJKLZXCVBNM")
canvas_script = ""

with open('app7.py', 'r') as file: canvas_script = file.read()


for i,l in enumerate(letters):
    if i<10:
        keys.append(Key(startX + i*w + i*5, startY, w, h, l))
    elif i<19:
        keys.append(Key(startX + (i-10)*w + i*5, startY + h + 5,w,h,l))  
    else:
        keys.append(Key(startX + (i-19)*w + i*5, startY + 2*h + 10, w, h, l)) 

keys.append(Key(startX+25, startY+3*h+15, 5*w, h, "Space"))
keys.append(Key(startX+8*w + 50, startY+2*h+10, w, h, "clr"))
keys.append(Key(startX+5*w+30, startY+3*h+15, 5*w, h, "<--"))


cap = cv2.VideoCapture(0)
ptime = 0

# initiating the hand tracker
tracker = HandTracker(detectionCon=0.8)

# getting frame's height and width
frameHeight, frameWidth, _ = cap.read()[1].shape
buttonX = frameWidth //2  + 160
buttonY = frameHeight + 170

# showKey = Key(buttonX - 200,buttonY,100,45, 'Keyboard')
mouse = Key(buttonX - 40,buttonY,100,45, 'Mouse')
exitKey = Key(buttonX + 120,buttonY,100,45, 'Exit')
textBox = Key(startX, startY-h-5, 10*w+9*5, h,'')

# showKey = Key(20, frameHeight - 70, 80, 50, 'Show Canvas')
# keyboardKey = Key(120, frameHeight - 70, 80, 50, 'Show Keyboard')
# exitKey = Key(220, frameHeight - 70, 80, 50, 'Exit')
# textBox = Key(startX, startY-h-5, 10*w+9*5, h, '')


# showKey.x = int(frameWidth*1.5) - 85
# exitKey.x = int(frameWidth*1.5) - 85
#print(showKey.x)

clickedX, clickedY = 0, 0
mousX, mousY = 0, 0

show = True
isMouse = False
cv2.namedWindow('video')

counter = 0
previousClick = 0
previousClickShow = 0

keyboard = Controller()
    
def show_control_keyboard(mousX,mousY,signTipX,signTipY,thumbTipX,thumbTipY,clickedX, clickedY,previousClick,alpha):
    textBox.drawKey(frame, (255,255,255), (0,0,0), 0.3)
    for k in keys:
        if k.isOver(mousX, mousY) or k.isOver(signTipX, signTipY):
            alpha = 0.1
            # writing using mouse right click
            if k.isOver(clickedX, clickedY):                              
                if k.text == '<--':
                    textBox.text = textBox.text[:-1]
                elif k.text == 'clr':
                    textBox.text = ''
                elif len(textBox.text) < 30:
                    if k.text == 'Space':
                        textBox.text += " "
                    else:
                        textBox.text += k.text
                        
            # writing using fingers
            if (k.isOver(thumbTipX, thumbTipY)):
                clickTime = time.time()
                if clickTime - previousClick > 0.6:                               
                    if k.text == '<--':
                        textBox.text = textBox.text[:-1]
                    elif k.text == 'clr':
                        textBox.text = ''
                    elif len(textBox.text) < 30:
                        if k.text == 'Space':
                            textBox.text += " "
                        else:
                            textBox.text += k.text
                            #simulating the press of actuall keyboard
                            keyboard.press(k.text)
                    previousClick = clickTime
        k.drawKey(frame,(255,255,255), (0,0,0), alpha=alpha)
        alpha = 0.5
    clickedX, clickedY = 0, 0 

# def display_canvas():
#     cap.release()
#     cv2.destroyWindow('video')
#     time.sleep(1)
#     main_loop()
    

while True:
    if counter >0:
        counter -=1
        
    signTipX = 0
    signTipY = 0

    thumbTipX = 0
    thumbTipY = 0

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(int(frameWidth*1.5), int(frameHeight*1.5)))
    frame = cv2.flip(frame, 1)
    #find hands
    frame = tracker.findHands(frame)
    lmList = tracker.getPostion(frame, draw=False)
    if lmList:
        signTipX, signTipY = lmList[8][1], lmList[8][2]
        thumbTipX, thumbTipY = lmList[4][1], lmList[4][2]
        if calculateIntDidtance((signTipX, signTipY), (thumbTipX, thumbTipY)) < 30:
            centerX = int((signTipX+thumbTipX)/2)
            centerY = int((signTipY + thumbTipY)/2)
            cv2.line(frame, (signTipX, signTipY), (thumbTipX, thumbTipY), (0,255,0),2)
            cv2.circle(frame, (centerX, centerY), 5, (0,255,0), cv2.FILLED)

    ctime = time.time()
    fps = int(1/(ctime-ptime))

    cv2.putText(frame,str(fps) + " FPS", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),2)
    # showKey.drawKey(frame,(255,255,255), (0,0,0),0.1, fontScale=0.5)
    mouse.drawKey(frame,(255,255,255), (0,0,0),0.1, fontScale=0.5)
    exitKey.drawKey(frame,(255,255,255), (0,0,0),0.1, fontScale=0.5)
    cv2.setMouseCallback('video', getMousPos)

    # if showKey.isOver(clickedX, clickedY):
    #     show = not show
    #     isMouse = False
    #     showKey.text = "Canvas" if show else "Keyboard"
    #     clickedX, clickedY = 0, 0

    # if (showKey.isOver(thumbTipX, thumbTipY)):
    #     clickTimeShow = time.time()
    #     if clickTimeShow - previousClickShow > 1:    
    #         show = not show
    #         isMouse = False
    #         showKey.text = "Canvas" if show else "Keyboard"
    #         previousClickShow = clickTimeShow
            
    if mouse.isOver(clickedX, clickedY):
        isMouse = not isMouse
        show = not show
        mouse.text = "Off Mouse" if isMouse else "Mouse"
        clickedX, clickedY = 0, 0

    if (mouse.isOver(thumbTipX, thumbTipY)):
        clickTimeShow = time.time()
        if clickTimeShow - previousClickShow > 1:    
            isMouse = not isMouse
            show = not show
            mouse.text = "Off Mouse" if isMouse else "Mouse"
            previousClickShow = clickTimeShow

    # if (showKey.isOver(thumbTipX, thumbTipY)):
    #     show = not show
    #     showKey.text = "Hide" if show else "Show"
           
    

    if exitKey.isOver(clickedX, clickedY):
        #break
        exit()

    #checking if sign finger is over a key and if click happens
    alpha = 0.5
    
    if show:
        show_control_keyboard(mousX,mousY,signTipX,signTipY,thumbTipX,thumbTipY,clickedX, clickedY,previousClick,alpha)
    # elif not isMouse:
    #     display_canvas()
    
    if isMouse : 
        if signTipX > 0 and  signTipY > 0:
            pyautogui.moveTo(signTipX,signTipY , duration = 0)
              
    ptime = ctime
    cv2.imshow('video', frame)

    ## stop the video when 'q' is pressed
    pressedKey = cv2.waitKey(1)
    if pressedKey == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
