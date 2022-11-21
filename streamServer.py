import sys
from flask import Flask, render_template, Response
import cv2, time
import threading
import vlc
import numpy as np
import subprocess
from ffpyplayer.player import MediaPlayer
app = Flask('hello')
camera = cv2.VideoCapture("rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=0", cv2.CAP_ANY)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
success,frame = camera.read()
screenWidth = 1280
screenHeight = 720

mediaPlayer = MediaPlayer()
def get_frames():
    #print('generation of frames started')
    global frame, success
      
    img = np.zeros((screenHeight,screenWidth,3),np.uint8)
    success, rawframe = camera.read()
    #rawframe = cv2.resize(rawframe,(720,480),interpolation=cv2.INTER_LINEAR)
    small = cv2.resize(rawframe,(screenWidth//2,screenHeight//2),interpolation=cv2.INTER_LINEAR)
    smalla = cv2.resize(rawframe,(screenWidth//2,screenHeight//2),interpolation=cv2.INTER_LINEAR)
    img[0:screenHeight//2  ,0:screenWidth//2] = small
    img[0:screenHeight//2,screenWidth//2:screenWidth] = smalla
    img[screenHeight//2:screenHeight,0:screenWidth//2] = smalla
    img[screenHeight//2:screenHeight,screenWidth//2:screenWidth] = small
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #ret, buffer = cv2.imencode('.jpeg', small)
    frameByte = img.tobytes()   
    frame = frameByte
    
    #p2 = subprocess.Popen(["cvlc", "--demux=rawvideo --rawvid-fps=30 --rawvid-width=1280 --rawvid-height=720 --rawvid-chroma=RV24 - --sout '#display' "+ frame.decode(encoding='utf8')],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    #print(p2.stdin.write(frame))
    
    while True:
        
        img = np.zeros((screenHeight,screenWidth,3),np.uint8)
        success, rawframe = camera.read()
        #rawframe = cv2.resize(rawframe,(720,480),interpolation=cv2.INTER_LINEAR)
        small = cv2.resize(rawframe,(screenWidth//2,screenHeight//2),interpolation=cv2.INTER_LINEAR)
        smalla = cv2.resize(rawframe,(screenWidth//2,screenHeight//2),interpolation=cv2.INTER_LINEAR)
        img[0:screenHeight//2  ,0:screenWidth//2] = small
        img[0:screenHeight//2,screenWidth//2:screenWidth] = smalla
        img[screenHeight//2:screenHeight,0:screenWidth//2] = smalla
        img[screenHeight//2:screenHeight,screenWidth//2:screenWidth] = small
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #ret, buffer = cv2.imencode('.jpeg', small)
        
        
        frameByte = img.tobytes()
        
        frame = frameByte
        t1 = time.time()
        
        #p2.communicate(input=frame)
        
        #print((time.time() - t1)*1000)
        #f.truncate(0)
        f = open('video.yuv','wb')
        f.write(frame)
        f.close()
        time.sleep(1/5)
        sys.stdout.buffer.write(frame)
       
        #print(time.time())
   

time.sleep(2)
cameraThread = threading.Thread(target=get_frames)
cameraThread.start()
#subprocess.Popen(["vlc","--demux=rawvideo --rawvid-fps=10 --rawvid-width=1280 --rawvid-height=720 --rawvid-chroma=RV24 - --sout '#display'","video.yuv"],stdin=subprocess.PIPE)

