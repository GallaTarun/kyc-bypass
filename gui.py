from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
import multiprocessing
import virtual_camera

def onFaceImageUpload():
    global GENERATE_ANIMATION_BUTTON

    file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a Face Image", filetypes=(("JPG File","*.jpg"), ("PNG File", "*.png"))) 
    # Add generate animation Button
    res = Text(frm2, height=3, width=50)
    res.grid(row=3, column=0, columnspan=3)
    res.insert(END, "Uploaded Image: "+file_name)
    if not GENERATE_ANIMATION_BUTTON:
        GENERATE_ANIMATION_BUTTON = True
        generate_animation_btn = Button(frm2, text="Generate Animation", command=partial(createNewProcess, file_name))
        generate_animation_btn.grid(row=2, column=2)

def onIdUpload():
    file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File","*.jpg"), ("PNG File", "*.png")))
    res = Text(frm1, height=3, width=50)
    res.grid(row=1, column=0, columnspan=3)
    res.insert(END, "Uploaded Image: "+file_name)
    upload_button = Button(frm1, text="Send to Virtual Camera", command=partial(virtual_camera.sendImageFrames, file_name))
    upload_button.grid(row=0, column=2)

def generateAnimation(file_name):
    if os.path.exists('./animation/result.mp4'):
        os.remove('./animation/result.mp4')
    animation_script_command = 'python ./animation/demo.py --config ./animation/config/vox-adv-256.yaml --driving_video ./animation/driving.mp4 --source_image ' + file_name + ' --checkpoint ./animation/vox-adv-cpk.pth.tar --relative --adapt_scale --cpu'
    os.system("start /wait cmd /c "+animation_script_command)
    # ONCE DONE, use ./animation/result.mp4 frames to send to virtual camera
    upload_button = Button(frm2, "Send to Virtual Camera", command=partial(virtual_camera.sendVideoFrames, "./animation/result.mp4")) 
    upload_button.grid(row=3, column=3)


def createNewProcess(file_name):
    process = multiprocessing.Process(target=generateAnimation, args=(file_name, ))
    process.start()


GENERATE_ANIMATION_BUTTON = False
FACE_IMAGE_PATH = ""

root = Tk()

frm1 = Frame(root)
frm1.pack(side=TOP, padx=15, pady=20)

id_label = Label(frm1, text="Upload your ID")
id_label.grid(row=0, column=0)

id_btn = Button(frm1, text="Browse Image", command=onIdUpload)
id_btn.grid(row=0, column=1)

# id_path_text = Text(frm1)
# id_path_text.grid(row=1, column=0, columnspan=2)

frm2 = Frame(root)
frm2.pack(padx=15, pady=20)

face_label = Label(frm2, text="Upload your Image")
face_label.grid(row=2, column=0)

face_image_btn = Button(frm2, text="Browse Image", command=onFaceImageUpload)
face_image_btn.grid(row=2, column=1)

btn2 = Button(root, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=10)


root.title("ByPass KYC")
root.geometry("600x400")
root.mainloop()