import numpy as np
import time 
import cv2 as cv
import threading
input_rtsp = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"
input_rtspA = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"

vcap = cv.VideoCapture(input_rtsp,cv.CAP_FFMPEG)
vcapa = cv.VideoCapture(input_rtspA,cv.CAP_ANY)
#vcapb = cv.VideoCapture(input_rtspA)
#vcapc = cv.VideoCapture(input_rtsp)
vcap.set(cv.CAP_PROP_BUFFERSIZE,3)


print(vcap.get(cv.CAP_PROP_FPS))



screenWidth = 720
screenHeight = 480
img = np.zeros((screenHeight,screenWidth,2),np.uint8)

cv.imshow('VIDEO',img)
cv.setWindowProperty('VIDEO',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

ret, frame = vcap.read()
reta, framea = vcapa.read()
    #print(vcap)
small = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
smalla = cv.resize(framea,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
    
while(1):
  
    ret, frame = vcap.read()
    reta, framea = vcapa.read()
    #print(img.shape)
    small = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
    smalla = cv.resize(framea,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
    img[0:screenHeight//2  ,0:screenWidth//2] = small
    img[0:screenHeight//2,screenWidth//2:screenWidth] = smalla
    img[screenHeight//2:screenHeight,0:screenWidth//2] = smalla
    img[screenHeight//2:screenHeight,screenWidth//2:screenWidth] = small
    cv.imshow('VIDEO', img)
    time.sleep(1/60)
    if cv.waitKey(1) == ord('q'):
        break
vcap.release()
vcapa.release()
cv.destroyAllWindows()