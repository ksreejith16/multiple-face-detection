import cv2
import numpy as np
import os
from PIL import Image

def get_images_and_labels(path):
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        pil_image = Image.open(image_path).convert('L')
        image_np = np.array(pil_image, 'uint8')
        
        # Extract the user_id from the image filename (format: User.{user_id}_{username}.{count}.jpg)
        id_ = int(os.path.split(image_path)[-1].split(".")[1].split("_")[0])

        # Detect faces in the image
        faces = detector.detectMultiScale(image_np)
        
        for (x, y, w, h) in faces:
            face_samples.append(image_np[y:y + h, x:x + w])
            ids.append(id_)

    return face_samples, ids

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_and_labels("TrainingImage")
    
    recognizer.train(faces, np.array(ids))
    recognizer.save("TrainingImageLabel/Trainer.yml")
    print("Model trained and saved as Trainer.yml")

if __name__ == "__main__":
    train_model()
