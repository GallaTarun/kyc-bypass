import av
import pyvirtualcam
import sys
import cv2

def get_img_radio(img):
    width = img.shape[1]
    height = img.shape[0]
    if width>height:
        return width/height
    else:
        return height/width

def add_padding(img):
    width = img.shape[1]
    height = img.shape[0]
    ratio = 16/9
    
    desired_height = height
    desired_width = width
    top = 0
    bottom = 0
    left = 0
    right = 0
    if get_img_radio(img) > ratio: #17/9 > 16/9 add padding to short side
        if width>height:
            desired_width = width
            desired_height = width / ratio
            top = int((desired_height - height)/2)
            bottom = top
        else:
            desired_width = height / ratio
            desired_height = height
            left = int((desired_width - width)/2)
            right = left
    else: # 4/3 < 16/9 add padding to long side
        if width>=height:
            desired_width = height * ratio
            desired_height = height
            left = int((desired_width - width)/2)
            right = left
        else:
            desired_width = width
            desired_height = width * ratio
            top = int((desired_height - height)/2)
            bottom = top

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=[255,255,255])
    return img

def sendVideoFrames(path):
    container = av.open(path)
    height = container.streams[0].codec_context.coded_height
    width = container.streams[0].codec_context.coded_width

    cam = pyvirtualcam.Camera(width=width, height=height, fps=20)

    while True:
        container = av.open(path)
        stream = container.streams.video[0]
        for frame in container.decode(stream):
            frame = frame.to_ndarray(format='bgr24')
            cam.send(frame)
            cam.sleep_until_next_frame()
        if cv2.waitKey(1) & 0xFF == 27:
            break
        

def sendImageFrames(path):
    frame = cv2.imread(path)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = add_padding(frame)
    width = frame.shape[1]
    height = frame.shape[0]

    cam = pyvirtualcam.Camera(width=width, height=height, fps=20)
    while True:
        cam.send(frame)
        cam.sleep_until_next_frame()

