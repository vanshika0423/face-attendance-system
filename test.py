from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# Function to make the system speak a given text
def speak(text):
    try:
        speak_engine = Dispatch("SAPI.SpVoice")
        speak_engine.Speak(text)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Initialize video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load data
try:
    with open('data/names.pkl', 'rb') as f:
        LABELS = pickle.load(f)

    with open('data/faces_data.pkl', 'rb') as f:
        FACES = pickle.load(f)

    # Check consistency of FACES and LABELS
    if len(FACES) != len(LABELS):
        raise ValueError("FACES and LABELS must have the same number of samples.")

    # Initialize KNN classifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)
except FileNotFoundError as e:
    print(f"Data file not found: {e}")
    exit()
except ValueError as e:
    print(f"Data validation error: {e}")
    exit()

# Load background image
background_path = os.path.join(os.getcwd(), "background.png")
if os.path.exists(background_path):
    imgBackground = cv2.imread(background_path)
else:
    print(f"Error: Background image not found at {background_path}")
    exit()

# Column names for attendance CSV
COL_NAMES = ['NAME', 'TIME']

# Attendance loop
while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to access the camera.")
        break

    # Convert to grayscale for face detection
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(grey, 1.3, 5)

    for (x, y, w, h) in faces:
        # Crop, resize, and flatten the face for prediction
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        try:
            output = knn.predict(resized_img)

            # Generate timestamps
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

            # Ensure attendance folder exists
            attendance_folder = "attendance_folder"
            if not os.path.exists(attendance_folder):
                os.makedirs(attendance_folder)
            attendance_file = os.path.join(attendance_folder, f"attendance_{date}.csv")

            # Add attendance details
            attendance = [str(output[0]), str(timestamp)]
            with open(attendance_file, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not os.path.isfile(attendance_file) or os.path.getsize(attendance_file) == 0:
                    writer.writerow(COL_NAMES)
                writer.writerow(attendance)

            # Overlay predictions on the frame
            cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        except Exception as e:
            print(f"Error during prediction: {e}")

        # Voice feedback for attendance
        if cv2.waitKey(1) == ord('o'):
            speak("Attendance taken.")
            time.sleep(5)

    # Update the background with the frame
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
video.release()
cv2.destroyAllWindows()
