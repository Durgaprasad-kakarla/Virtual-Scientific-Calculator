import cv2
import mediapipe as mp
import math
import HandTrackingModule as htm

def check(s):
    i=0
    while i<len(s):
        if s[i]=='0':
            i+=1
        else:
            break
    return s[i:]

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 100, 230), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 3)

    def checkClick(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width and \
                self.pos[1]<y<self.pos[1]+self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),
                        9)
            return True
        else:
            return False
# Creating Buttons
buttonListValues = [
    ['&','|','^','=','AC'],
    ['7', '8', '9', '*','DE'],
                    ['4', '5', '6', '-','sq'],
                    ['1', '2', '3', '+','('],
                    ['0', '/', '.', 'log',')']]

detector = htm.HandDetector(detectionCon=0.8)
cap = cv2.VideoCapture(0)

myEquation=""
delayCounter=0
# Creating Buttons
buttonList = []
for i in range(len(buttonListValues[0])):
    for j in range(len(buttonListValues)):
        xpos = i * 100 + 700
        ypos = j * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[j][i]))
print(buttonList)
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)

    # Detection of the hand
    hands, img = detector.findHands(img)

    # Draw all buttons
    cv2.putText(img,"Calculator",(700,65),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3,(255,0,255),5)
    cv2.rectangle(img, (700, 70), (700 + 500, 70 + 100), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (700, 70), (700 + 500, 70 + 100), (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    #Check for hand
    if hands:
        lmList=hands[0]['lmList']
        length,_,img=detector.findDistance(lmList[8][:2],lmList[12][:2],img)
        x,y=lmList[8][:2]
        if length<50:
            for i,button in enumerate(buttonList):
                if button.checkClick(x,y) and delayCounter==0:
                    myvalue=buttonListValues[i%5][i//5]
                    if myvalue=='DE':
                        myEquation=myEquation[:-1]
                    elif myvalue=='AC':
                        myEquation=''
                    elif myvalue=='sq':
                        myEquation=check(myEquation)
                        myEquation=str((math.sqrt((int(eval(myEquation))))))
                    elif myvalue=='log':
                        myEquation=check(myEquation)
                        myEquation=str((math.log10(int(eval(myEquation)))))
                    elif myvalue=='=':
                        myEquation=check(myEquation)
                        myEquation=str(eval(myEquation))
                    else:
                        myEquation+=myvalue
                    delayCounter=1
    #Avoid Duplicates
    if delayCounter!=0:
        delayCounter+=1
        if delayCounter>10:
            delayCounter=0

    #Display equation/result
    cv2.putText(img,myEquation,(710,130),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)

    cv2.imshow("My Virtual Calculator", img)
    cv2.waitKey(1)
