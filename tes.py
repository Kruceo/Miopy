import numpy as np
import time
import argparse
import cv2 as cv
import threading
import queue
import vlc
import sys

vlcPlayer = vlc.Instance()
#vlcPlayer.setData

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",required=True)
args = vars(ap.parse_args())

input_rtsp = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"
input_rtspA = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"

framesRendered = 0
timeEllapsed = 0
bufferQ = queue.Queue(128)
vcap = cv.VideoCapture(input_rtsp,cv.CAP_ANY)
print(vcap)
vcapa = cv.VideoCapture(input_rtspA)
#vcapb = cv.VideoCapture(input_rtspA)
#vcapc = cv.VideoCapture(input_rtsp)
#vcap.set(cv.CAP_PROP_FPS, 24)
ret, frame = vcap.read()
reta, framea = vcapa.read()
frameToRender = frame
def myTask():
    while 1:
        global bufferQ
        global frameToRender
        
        img = np.zeros((screenHeight,screenWidth,3),np.uint8)
        ret,frame = vcap.read()
        #frame = cv.resize(frame,(screenWidth//1,screenHeight//1),interpolation=cv.INTER_LINEAR)
        #frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        small = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_CUBIC)
        smalla = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
        img[0:screenHeight//2  ,0:screenWidth//2] = small
        img[0:screenHeight//2,screenWidth//2:screenWidth] = smalla
        img[screenHeight//2:screenHeight,0:screenWidth//2] = smalla
        img[screenHeight//2:screenHeight,screenWidth//2:screenWidth] = small
        frameToRender = img
        #global reta,framea 
        #reta, framea = vcapa.read()
        if not bufferQ.empty():
            try:
                print('0')
                bufferQ.get_nowait()   # discard previous (unprocessed) frame
            except bufferQ.Empty:
                pass
        bufferQ.put(frame)
        sys.stdout.buffer.write(frame.tobytes())
        #print(bufferQ)
        #cv.imshow('VIDEO', frame)
        #framesRendered += 1

print(vcap.get(cv.CAP_PROP_FPS))

screenWidth = 1280
screenHeight = 720


cv.imshow('VIDEO',frameToRender)
cv.setWindowProperty('VIDEO',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

 #ret, frame = vcap.read()
#reta, framea = vcapa.read()
    #print(vcap)
#small = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
#smalla = cv.resize(framea,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)

t1 = threading.Thread(target=myTask)
t1.daemon = True
t1.start()
timeA = time.time()
wout = cv.VideoWriter('test2.mp4',cv.VideoWriter_fourcc(*'MP4V'), 30, (screenWidth,screenHeight))

while 1:
   
    #print(img.shape)
    
   
    #cv.imwrite('jpeg.jpg',frameToRender)
    wout.write(frameToRender)
   
    print(wout)
    
    cv.imshow('VIDEO', frameToRender)
    framesRendered += 1
    if cv.waitKey(1) == ord('q'):
        break
    print(int(framesRendered/(time.time() - timeA)))   
 #   time.sleep(1)

vcap.release()
wout.release()
vcapa.release()
cv.destroyAllWindows()
exit()
  