
from flask import Flask, Response
import cv2, time
import threading
import numpy as np
import subprocess

streamCaptures = []
cols = 3
rows = 3
config = open('config.cfg','r').read()
#print(config)
lines = config.split('\n')
#print(lines)

for line in lines:
    print(line)
    if line.startswith('stream:'):
        streamUrl = line.replace('stream:','',1)
        print(streamUrl)
        streamCaptures.insert(0,cv2.VideoCapture(streamUrl))
    if line.startswith('cols:'):
        cols = int(line.replace('cols:','',1))
        print(cols)
    if line.startswith('rows:'):
      
        rows = int(line.replace('rows:','',1))
        print(rows)
        
print(streamCaptures)
time.sleep(1)


app = Flask('hello')
t1 = time.time()



camera = cv2.VideoCapture('rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=0') 

    
camera.set(cv2.CAP_PROP_FPS,5)
print("stream connect = "+str(time.time()- t1))
success,frame = camera.read()
screenWidth = 1280
screenHeight = 720

def get_frames():
    coefCols = screenWidth//cols
    coefRows = screenHeight//rows
    t2 = time.time()
    global frame, success
    t1 = time.time()
    img = np.zeros((screenHeight,screenWidth,3),np.uint8)
    success, rawframe = camera.read()
    print("stream read = "+str(time.time()- t1))
    t1 = time.time()
    small = cv2.resize(rawframe,(screenWidth//cols,screenHeight//cols),interpolation=cv2.INTER_LINEAR)
    #smalla = cv2.resize(rawframe,(screenWidth//cols,screenHeight//cols),interpolation=cv2.INTER_LINEAR)
    print("resize smalls = "+str(time.time()- t1))
    t1 = time.time()
    x = 0
    y = 0
        
    for x in range(rows):
        for y in range(cols):
            #print(x,y)
            #print(y*coefCols,(y+1)*coefCols)
            img[x*coefRows:(x+1)*coefRows,y*coefCols:(y+1)*coefCols] = small
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
   
    while True:
        successes,frames = [],[]
        for cam in streamCaptures:
            s,f = cam.read()
            img = np.zeros((screenHeight,screenWidth,3),np.uint8)
            small = cv2.resize(f,(coefCols,coefRows),interpolation=cv2.INTER_LINEAR)
            successes.insert(0,s)
            frames.insert(0,small)
        x = 0
        y = 0
        z = 0
        for x in range(rows):
            if z >= len(frames):
                    break
            for y in range(cols):
                       
                img[x*coefRows:(x+1)*coefRows     ,     y*coefCols:(y+1)*coefCols] = frames[z]
                z += 1 
                if z >= len(frames):
                    break
            
        frame = img

def generate():
    global frame, lock
    while True:
        t1 = time.time()
        if frame is None:
            continue
        
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        cv2.imwrite('test.jpg',encodedImage)
        if not flag:
            continue
        #print(time.time() - t1)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')   
        time.sleep(1/30)
       
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

