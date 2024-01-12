import tkinter
import cv2
import numpy as np
from email.message import EmailMessage
import ssl
import smtplib
import playsound
from twilio.rest import Client
import test
from tkinter import *
from PIL import Image, ImageTk


def play_audio():
    playsound.playsound("alarm-sound.mp3", True)


root = tkinter.Tk()
root.geometry("700x550")
root.configure(bg="black")
tkinter.Label(root, text="Be Safe System", font=("times new roman", 30, "bold"), bg="black", fg="blue").pack()
f1 = tkinter.LabelFrame(root, bg="blue")
f1.pack()
L1 = tkinter.Label(f1, bg="blue")
L1.pack()
net = cv2.dnn.readNet('yolov3_custom_last (try).weights', 'yolov3_testing.cfg')
fire = False
again = True
account_ids = 'ACa934c1963d9ca524ca0c5e155be08e6d'
auto_token = 'a61186291fcf4193d2e72c95d3c2bdfd'
twillo_number = '+16513763173'
my_phone_number = '+20 111 412 1228'

classes = []
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture('video.mp4')
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

while True:

    _, img = cap.read()
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)
            fire = True
            if again == True:
                if fire:
                    play_audio()
                    sender = 'safeyourself629@gmail.com'
                    rec = 'mostafaelofy629@gmail.com'
                    email_pass = 'jgczpfgulwjgtrfk'
                    subject = 'you have fire'
                    body = """
                               you have a fire in your office call 111
                               """
                    em = EmailMessage()
                    em['from'] = sender
                    em['to'] = rec
                    em['subject'] = subject
                    em.set_content(body)

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(sender, email_pass)
                        smtp.sendmail(sender, rec, em.as_string())
                    cleint = Client(account_ids, auto_token)
                    message = cleint.messages.create(
                        body="you have fire in your office ",

                        from_=twillo_number,

                        to=my_phone_number
                    )
                    print(message.body)
                again = False

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    L1['image'] = img
    key = cv2.waitKey(1)
    if key == 27:
        break
    root.update()
