import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe
from time import sleep
detector    =   HandDetector(detectionCon=0.8,maxHands=1)
cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
if cap.isOpened(): # try to get the first frame
    success, image = cap.read()
else:
    success = False

keys    =   [['Q','W','E','R','T','Y','U','I','O','P'],
             ['A','S', 'D','F','G','H','J','K','L',';'],
             ['Z','X','C','V','B','N','M',',','.','/']]

final_text=""
buttons_List = []


def Draw(image,buttons_List):
    for buttons in buttons_List:
        x, y = buttons.pos
        w, h = buttons.size

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, buttons.text, ((x + w // 2 - 8), (y + h // 2 + 8)), 5, cv2.FONT_HERSHEY_PLAIN, (255, 0, 0), 2)
    return image
def drawrectangle(image,pos,size):
    cv2.rectangle(image, (pos[0],pos[1]), (size[0], size[1]), (0, 255, 0), cv2.FILLED)
    return image

class Button():
    def __init__(self,pos,text,size):
        self.pos=pos
        self.text=text
        self.size=size

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttons_List.append(Button([j * 100 - j * 40 + 40, i * 100 - i * 40 + 50], key, [50, 50]))




while True:

    success, image = cap.read()
    hands ,image =   detector.findHands(image, flipType=False)
    image = Draw(image, buttons_List)

    if hands:


        lmList = hands[0]['lmList']
        if lmList:
            for buttons in buttons_List:
                x, y = buttons.pos
                w, h = buttons.size
                if x < lmList[8][0] < x + w and y<lmList[8][1]<y+h:
                    cv2.rectangle(image, buttons.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                    cv2.putText(image, buttons.text, ((x + w // 2 - 8), (y + h // 2 + 8)), 5, cv2.FONT_HERSHEY_PLAIN,
                                (255, 0, 255), 2)
                    distance, _, _ = detector. findDistance(lmList[8], lmList[12], image)
                    if distance < 20:
                        print(distance)
                        pos  = [0, 400]
                        size = [700, 700]
                        sleep(1)
                        final_text+=buttons.text

    else:
        print("none")
    cv2.rectangle(image, (0,300), (400,400), (0, 0, 0), cv2.FILLED)
    cv2.putText(image, final_text, (0, 350), 5, cv2.FONT_HERSHEY_PLAIN,
                (255, 255, 255), 2)
    cv2.imshow("preview", image)




    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break

cap.release()
cv2.destroyAllWindow()