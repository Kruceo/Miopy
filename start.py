import subprocess
import time

print('lido')
p = subprocess.Popen(["python3","streamServer.py","|","cvlc","--demux=rawvideo --rawvid-fps=10 --rawvid-width=1280 --rawvid-height=720 --rawvid-chroma=RV24 - --sout '#display'"],shell=False)
print('lido2')
time.sleep(2)
p2 =  subprocess.Popen(["cvlc","video.yuv",p.stdout.read(1)],stdin=subprocess.PIPE)
print('lido3')

while True:
    time.sleep(5)

