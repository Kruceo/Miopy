import numpy as np
import sys
import cv2 as cv

input_rtsp = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"
input_rtspA = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
vcap = cv.VideoCapture(input_rtsp)
vcapa = cv.VideoCapture(input_rtspA)
#vcapb = cv.VideoCapture(input_rtspA)
#vcapc = cv.VideoCapture(input_rtsp)
while(1):
    ret, frame = vcap.read()
    reta, framea = vcapa.read()
    print(vcap)
    small = cv.resize(frame,(640,360),interpolation=cv.INTER_AREA)
    smalla = cv.resize(framea,(640,360),interpolation=cv.INTER_AREA)
    img = np.zeros((720,1280,3),np.uint8)
    print(img.shape)
    img[0:360  ,0:640] = small
    img[0:360,640:1280] = smalla
    img[360:720,0:640] = smalla
    img[360:720,640:1280] = small
  
    cv.imshow('VIDEO', img)
    cv.setWindowProperty('VIDEO',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    if cv.waitKey(1) == ord('q'):
        break
vcap.release()
vcapa.release()
cv.destroyAllWindows()