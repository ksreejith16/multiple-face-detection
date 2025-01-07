import cv2
import os
import sys
import json

# Check for user_id and user_name arguments
if len(sys.argv) < 3:
    print("User ID and/or name not provided. Exiting.")
    sys.exit(1)

user_id = sys.argv[1]
user_name = sys.argv[2]

# Create the TrainingImage folder if it doesn't exist
if not os.path.exists("TrainingImage"):
    os.makedirs("TrainingImage")

# Load existing data from data.json or create an empty dictionary
data_file = "data.json"
try:
    with open(data_file, "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

# Update the data dictionary with the new ID-name entry
data[user_id] = user_name

# Save the updated data to data.json
with open(data_file, "w") as f:
    json.dump(data, f)

def capture_images():
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    num_images = 116  # Fixed number of images to capture
    print("\n[INFO] Initializing face capture. Look at the camera...")

    count = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            count += 1
            img_path = f"TrainingImage/User.{user_id}.{count}.jpg"
            cv2.imwrite(img_path, gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Image {count}/{num_images}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.imshow("Taking Images", frame)

            if count >= num_images:
                break

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_images:
            break

    print("\n[INFO] Image capture completed and saved to TrainingImage folder.")
    cam.release()
    cv2.destroyAllWindows()

# Run the function
capture_images()
