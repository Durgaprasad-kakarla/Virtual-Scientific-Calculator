import time
import cvzone
import cv2
import mediapipe as mp
import math
import HandTrackingModule as htm
from sympy import symbols, diff

# Define the variable and the expression
curr = symbols('x')
def check_zeros(s):
    i=0
    while i<len(s):
        if s[i]=='0':
            i+=1
        else:
            break
    return s[i:]
def add_closed_paranthesis(s):
    #This function is for adding the closed paranthesis for the trignometric function as we are using radians
    s=list(s)
    n=len(s)
    lst=[]
    for i in range(n):
        if "".join(s[i:i+3]) in ["tan","cos","sin"]:
            j=i+3
            while j<n and s[j]!=')':
                print(j)
                j+=1
            lst.append(j)
    for i in lst:
        if i<n:
            s[i]="))"
    lst = []
    for i in range(n):
        if "".join(s[i:i + 3]) == "nrt":
            j = i + 3
            while j<n and s[j] != ',':
                j += 1
            lst.append(j)
    for i in lst:
        if i<n:
            s[i] = ",1/"
    return "".join(s)


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        if self.value in ["sin", "cos", "tan", "log", "sqrt","fact","exp","der","ncr","hyp","nrt"]:
            cvzone.cornerRect(img, (self.pos[0],self.pos[1],self.width,self.height),colorC=(0,126,255),colorR=(0,126,255),rt=3,t=12)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50),
                        3)
        elif self.value.isdigit():
            cvzone.cornerRect(img, (self.pos[0],self.pos[1],self.width,self.height),colorC=(0,126,255),colorR=(0,126,255),rt=3,t=12)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50),
                        3)
        else:
            cvzone.cornerRect(img, (self.pos[0],self.pos[1],self.width,self.height),colorC=(0,126,255),colorR=(0,126,255),rt=3,t=12)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 3)

    def checkClick(self,x,y):
        if self.value in ["sin","cos","tan","log","AC","DE","exp","der","ncr","hyp","nrt"]:
            if self.pos[0] < x < self.pos[0] + self.width and \
                    self.pos[1] < y < self.pos[1] + self.height:
                cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0,126,255),
                              cv2.FILLED)
                # cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
                cv2.putText(img, self.value, (self.pos[0] + 15, self.pos[1] + 65), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0),
                            5)
                return True
            return False
        elif self.value in ["sqrt","fact"]:
            if self.pos[0] < x < self.pos[0] + self.width and \
                    self.pos[1] < y < self.pos[1] + self.height:
                cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0,126,255),
                              cv2.FILLED)
                # cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
                cv2.putText(img, self.value, (self.pos[0] , self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0),
                            5)
                return True
            return False
        else:
            if self.pos[0]<x<self.pos[0]+self.width and \
                    self.pos[1]<y<self.pos[1]+self.height:
                cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0,126,255),
                              cv2.FILLED)
                # cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
                cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),
                            9)
                return True
            return False
# Creating Buttons
buttonListValues = [
    ['sin','cos','tan','hyp','der','=','AC'],
    ['ncr','fact','%','7', '8', '9','DE'],
                    ['(','x','sqrt','4', '5', '6','*'],
                    [')','exp',"nrt",'1', '2', '3','-'],
                    ['log','ln',",",'.', '0', '/','+']]

detector = htm.HandDetector(detectionCon=0.8)
cap = cv2.VideoCapture(0)
myEquation=""
delayCounter=0
# Creating Buttons
buttonList = []
for i in range(len(buttonListValues[0])):
    for j in range(len(buttonListValues)):
        xpos = i * 100 + 50
        ypos = j * 100 + 200
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[j][i]))

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 800))
    img = cv2.flip(img, 1)

    # Detection of the hand
    hands, img = detector.findHands(img,draw=False)

    # Draw all buttons
    cv2.putText(img,"ScientificCalculator",(50,80),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3,(255,0,255),5)
    cv2.rectangle(img, (50, 110), (50 + 700, 110 + 70), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (50, 110), (50 + 700, 110 + 70), (50,50,50), 4)

    for button in buttonList:
        button.draw(img)

    #Check for hand
    if hands:
        lmList=hands[0]['lmList']
        length,_,img=detector.findDistance(lmList[8][:2],lmList[12][:2],img,color=(255,0,255))
        x,y=lmList[8][:2]
        if length<70:
            for i,button in enumerate(buttonList):
                if button.checkClick(x,y) and delayCounter==0:
                    print(i)
                    print(i%5,i//5)
                    myvalue=button.value
                    if myvalue=='DE':
                        if myEquation[-2:]=='ln':
                            myEquation=myEquation[:-2]
                        if myEquation[-3:] in ["sin","cos","tan","log","fact","exp","der","nrt","hyp","ncr"]:
                            myEquation=myEquation[:-3]
                        elif myEquation[-4:] in ['sqrt','fact']:
                            myEquation=myEquation[:-4]
                        else:
                            myEquation=myEquation[:-1]
                    elif myvalue=='AC':
                        myEquation=''
                    elif myvalue == '=' and myEquation[:3] == 'der':
                        try:
                            derivative = diff(myEquation[3:], curr)
                            myEquation = str(derivative)
                        except:
                            myEquation = "Invalid Input"
                            start = time.time()
                            duration = 1
                    elif myvalue=='=':
                        myEquation=add_closed_paranthesis(myEquation)
                        myEquation=myEquation.replace('sin','math.sin(math.radians')
                        myEquation=myEquation.replace('cos','math.cos(math.radians')
                        myEquation=myEquation.replace('tan','math.tan(math.radians')
                        myEquation=myEquation.replace('log','math.log10')
                        myEquation=myEquation.replace("sqrt",'math.sqrt')
                        myEquation=myEquation.replace("ln","math.log")
                        myEquation=myEquation.replace("exp","math.exp")
                        myEquation=myEquation.replace("fact","math.factorial")
                        myEquation=myEquation.replace("%","*(1/100)*")
                        myEquation=myEquation.replace("hyp","math.hypot")
                        myEquation=myEquation.replace("nrt","math.pow")
                        myEquation=myEquation.replace("ncr","math.comb")
                        try:
                            # print(myEquation)
                            myEquation=str(eval(myEquation))
                        except:
                            myEquation="Invalid Input"
                            start = time.time()
                            duration = 1
                    else:
                        myEquation+=myvalue
                    delayCounter=1
    if "Invalid" in myEquation and time.time() - start >= duration:
        myEquation = ""
    #Avoid Duplicates
    if delayCounter!=0:
        delayCounter+=1
        if delayCounter>10:
            delayCounter=0

    #Display equation/result
    cv2.putText(img,myEquation,(60,160),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)

    cv2.imshow("My Virtual Calculator", img)
    cv2.waitKey(1)
