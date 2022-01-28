import cv2
from cv2 import bitwise_or
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness=25
eraserThickness=50
folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]
drawColor=(0,0,255)
cap = cv2.VideoCapture(0)
cap.set(3 , 1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.85)
xp,yp=0,0 #x and y previous
imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    #import image
    success,img =cap.read()
    img =cv2.flip(img, 1)

    #find hand landmarks
    img= detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        
      #  print(lmList)

        #tip of index and middle finger
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        #check which fingers are up
        fingers= detector.fingersUp()
        #print(fingers)
        #selection mode - 2 fingers up
        if fingers[1] and fingers[2]:
          xp,yp=0,0
         
          print("selection mode")
          #checking for the click 604,710  889,990  1100,1226
          if y1< 152:  #in header
            if 337<x1<434:
              header = overlayList[0]
              drawColor=(0,0,255)
            elif 604<x1<710:
              header = overlayList[1]
              drawColor=(255,0,0)
            elif 889<x1<990:
              header = overlayList[2]
              drawColor=(0,255,0)
            elif 1100<x1<1226:
              header = overlayList[3]
              drawColor=(0,0,0)
          cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        #draw mode - index finger is up
        if fingers[1] and fingers[2]== False:
          cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
          print("drawing mode")
          if xp==0 and yp==0:  #very first frame
            xp,yp=x1,y1   #sets previous position to current finger position

          if drawColor==(0,0,0):
             cv2.line(img, (xp,yp),(x1,y1),drawColor,eraserThickness)
             cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor,eraserThickness)
          else:
            cv2.line(img, (xp,yp),(x1,y1),drawColor,brushThickness)
            cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor,brushThickness)
          xp,yp=x1,y1  

    #convert canvas image to black and white
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)

    #convert it back to BGR
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    #merge the images
    img = cv2.bitwise_and(img,imgInv)
    img = bitwise_or(img,imgCanvas)
    
    #setting the header image
    img[0:153,0:1280] = header
   # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
  # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)