import numpy as np
import time 
import cv2 as cv
import threading
import queue

input_rtsp = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"
input_rtspA = "rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=1"

framesRendered = 0
timeEllapsed = 0
bufferQ = queue.Queue(1)
vcap = cv.VideoCapture(input_rtsp,cv.CAP_ANY)
print(vcap)
vcapa = cv.VideoCapture(input_rtspA)
#vcapb = cv.VideoCapture(input_rtspA)
#vcapc = cv.VideoCapture(input_rtsp)
vcap.set(cv.CAP_PROP_BUFFERSIZE,0)
ret, frame = vcap.read()
reta, framea = vcapa.read()
frameToRender = frame
def myTask():
    while 1:
        global bufferQ
        global frameToRender
        
        
        ret,frame = vcap.read()[1]
        frame = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_LINEAR)
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frameToRender = frame
        #global reta,framea 
        #reta, framea = vcapa.read()
        if not bufferQ.empty():
            try:
                print('0')
                bufferQ.get_nowait()   # discard previous (unprocessed) frame
            except bufferQ.Empty:
                pass
        bufferQ.put(frame)
        #print(bufferQ)
        #cv.imshow('VIDEO', frame)
        #framesRendered += 1

print(vcap.get(cv.CAP_PROP_FPS))

screenWidth = 1280
screenHeight = 720
img = np.zeros((screenHeight,screenWidth,3),np.uint8)

cv.imshow('VIDEO',img)
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
while 1:
   
    #print(img.shape)
    #small = cv.resize(frame,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_CUBIC)
    #smalla = cv.resize(framea,(screenWidth//2,screenHeight//2),interpolation=cv.INTER_AREA)
    #img[0:screenHeight//2  ,0:screenWidth//2] = small
    #img[0:screenHeight//2,screenWidth//2:screenWidth] = smalla
    #img[screenHeight//2:screenHeight,0:screenWidth//2] = smalla
    #img[screenHeight//2:screenHeight,screenWidth//2:screenWidth] = small
    cv.imshow('VIDEO', frameToRender)
    framesRendered += 1
    if cv.waitKey(1) == ord('q'):
        break
    print(int(framesRendered/(time.time() - timeA)))   
 #   time.sleep(1)

vcap.release()
vcapa.release()
cv.destroyAllWindows()
exit()
  