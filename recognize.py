import cv2
import numpy as np
import datetime
import requests
import json
from PIL import Image

# Load the trained model (Trainer.yml)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("TrainingImageLabel/Trainer.yml")

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Server URL for sending attendance data
url = 'http://localhost:5000/mark/markpresent'

# Load ID-name mappings from data.json
try:
    with open("data.json", "r") as f:
        id_to_name = json.load(f)
except FileNotFoundError:
    print("Data file not found. Starting with an empty ID-to-name mapping.")
    id_to_name = {}

def mark_attendance(id_, name):
    time_now = datetime.datetime.now()
    tStr = time_now.strftime('%H:%M:%S')
    dStr = time_now.strftime('%Y-%m-%d')

    attendance_data = {
        "rollno": id_,
        "name": name,
        "branch": "Unknown",
        "time": tStr,
        "date": dStr
    }
    response = requests.post(url, json=attendance_data)
    print("Status: ", response.text)

def recognize_faces():
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 65:
                name = id_to_name.get(str(id_), "Unknown")

                cv2.putText(img, f"Name: {name}", (x, y - 10), font, 1, (0, 255, 0), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if name != "Unknown":
                    mark_attendance(id_, name)
            else:
                name = "Unknown"
                cv2.putText(img, f"ID: {name}", (x, y - 10), font, 1, (0, 0, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("Recognizing Faces", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
