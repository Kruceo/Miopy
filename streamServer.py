from flask import Flask, render_template, Response
import cv2, time
import threading
import queue
app = Flask('hello')
camera = cv2.VideoCapture("rtsp://externo:0QbRoF7Xyuka@186.208.217.215:64554/cam/realmonitor?channel=1&subtype=0", cv2.CAP_ANY)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
success,frame = camera.read()

def get_frames():
    print('generation of frames started')
    while True:
        global frame, success
        success, rawframe = camera.read()
        frame = cv2.resize(rawframe,(720,480),interpolation=cv2.INTER_LINEAR)
        #print(222)

def send_frames():  
    while True:
        
       
        if not success:
            print('disconnect')
            break
        else:
           
            ret, buffer = cv2.imencode('.jpeg', frame)
            frameByte = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frameByte + b'\r\n')
            print(f'send frame {frameByte}' )
            time.sleep(1/30)

cameraThread = threading.Thread(target=get_frames)
cameraThread.start()
time.sleep(3)
@app.route('/video_feed')
def video_feed():
    return Response(send_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/')
def index():
    return """
<body>
<div class="container">
    <div class="row">
        <div class="col-lg-8  offset-lg-2">
            <h3 class="mt-5">Live Streaming</h3>
            <img src="/video_feed" width="100%">
        </div>
    </div>
</div>
</body>        
    """
app.run(host="192.168.20.198",port=9992)