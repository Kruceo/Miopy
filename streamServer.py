
from flask import Flask, Response
import cv2, time
import threading
import numpy as np
import subprocess

cols = 3
rows = 3

app = Flask('hello')
t1 = time.time()



camera = cv2.VideoCapture('rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=0') 
print("stream connect = "+str(time.time()- t1))
success,frame = camera.read()
screenWidth = 1280  
screenHeight = 720

def get_frames():
   
    t2 = time.time()
    global frame, success
    t1 = time.time()
    img = np.zeros((screenHeight,screenWidth,3),np.uint8)
    success, rawframe = camera.read()
    print("stream read = "+str(time.time()- t1))
    t1 = time.time()
    small = cv2.resize(rawframe,(screenWidth//cols,screenHeight//cols),interpolation=cv2.INTER_LINEAR)
    smalla = cv2.resize(rawframe,(screenWidth//cols,screenHeight//cols),interpolation=cv2.INTER_LINEAR)
    print("resize smalls = "+str(time.time()- t1))
    t1 = time.time()
    img[0:screenHeight//cols  ,0:screenWidth//cols] = small
    #img[0:screenHeight//cols,screenWidth//cols:screenWidth] = smalla
    #img[screenHeight//cols:screenHeight,0:screenWidth//cols] = smalla
    #img[screenHeight//cols:screenHeight,screenWidth//cols:screenWidth] = small
    print("img mosaic = "+str(time.time()- t1))
    t1 = time.time()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    print("img cvt = "+str(time.time()- t1))
    #ret, buffer = cv2.imencode('.jpeg', small)
    #frameByte = img.tobytes()   
    frame = img
    
    print("total = "+str(time.time()- t2))
    # p2.communicate(frame.tobytes())
    print()
    coefCols = screenWidth//cols
    coefRows = screenHeight//rows
    while True:
        
        img = np.zeros((screenHeight,screenWidth,3),np.uint8)
        success, rawframe = camera.read()
        #rawframe = cv2.resize(rawframe,(720,480),interpolation=cv2.INTER_LINEAR)
        small = cv2.resize(rawframe,(coefCols,coefRows),interpolation=cv2.INTER_LINEAR)
        #smalla = cv2.resize(rawframe,(screenWidth//cols,screenHeight//rows),interpolation=cv2.INTER_LINEAR)
        x = 0
        y = 0
        
        for x in range(rows):
            for y in range(cols):
                #print(x,y)
                #print(y*coefCols,(y+1)*coefCols)
                img[x*coefRows:(x+1)*coefRows     ,     y*coefCols:(y+1)*coefCols] = small
                
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #ret, buffer = cv2.imencode('.jpeg', small)
            
        frame = img
        #frameByte = img.tobytes()
        
        #frame = frameByte
        t1 = time.time()
        #time.sleep(1/30)
        #p2.communicate(input=frame)
        
        #print((time.time() - t1))
        #f.truncate(0)
        #f = open('video.yuv','wb')
        #f.write(frame)
        #f.close()
        
       
        #sys.stdout.buffer.write(frame)
def generate():
    # grab global references to the output frame and lock variables
    global frame, lock
    # loop over frames from the output stream
    while True:
        t1 = time.time()
        if frame is None:
            continue
        
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        print(time.time() - t1)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')   
        time.sleep(1/30)
       # print(time.time())
@app.route("/")
def index():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")   

#time.sleep(2)
cameraThread = threading.Thread(target=get_frames)
cameraThread.daemon = True
cameraThread.start()
#subprocess.Popen(["vlc","--demux=rawvideo --rawvid-fps=10 --rawvid-width=1280 --rawvid-height=720 --rawvid-chroma=RV24 - --sout '#display'","video.yuv"],stdin=subprocess.PIPE)

app.run('0.0.0.0',9921)
p2 = subprocess.Popen(["cvlc","http://127.0.0.1:9921/ "],stdout=subprocess.PIPE,stdin=subprocess.PIPE)

time.sleep(1)
