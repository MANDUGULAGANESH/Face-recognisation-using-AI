import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
from datetime import datetime
import streamlit as st
import webbrowser

# Path to training images
path = 'images'  
images = []
classNames = []
myList = os.listdir(path)
print("Images found:", myList)

# Load the images and names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:  # Check if the image was loaded successfully
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    else:
        print(f"Warning: Unable to load image {cl}")
print("Class Names:", classNames)

# Function to encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:  # Ensure there is at least one encoding
            encodeList.append(encodings[0])
        else:
            print("Warning: No face detected in an image.")
    return encodeList

# Function to mark attendance
def markAttendance(name):
    try:
        p = pd.read_csv('att.csv')  # Load CSV
    except FileNotFoundError:
        # Create a new CSV with required columns if it doesn't exist
        print("Attendance CSV not found. Creating new file.")
        p = pd.DataFrame(columns=["name", "attendance", "time", "date", "days"])
        p.to_csv("att.csv", index=False)

    if name in p['name'].tolist():
        name_idx = p['name'].tolist().index(name)
        p.loc[name_idx, 'attendance'] += 1
        now = datetime.now()
        date, time = now.strftime("%d-%m-%Y %H:%M:%S").split(' ')
        p.loc[name_idx, 'time'] = time

        if date != p.loc[name_idx, 'date']:
            p.loc[name_idx, 'date'] = date
            p.loc[name_idx, 'days'] += 1

        p.to_csv("att.csv", index=False)
    else:
        print(f"{name} not found in the attendance list.")

# Encode all known faces
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    name = "UNKNOWN"
    success, img = cap.read()
    if not success:
        print("Failed to capture image.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

        # Draw rectangle around the face and name label
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Face Recognition Based Attendance System', img)

    # Press space to mark attendance
    if cv2.waitKey(1) & 0xFF == ord(' '):
        if name != "UNKNOWN":
            print(name)
            webbrowser.open_new_tab("http://localhost:8502/voting")
            markAttendance(name)
        else:
            print("UNKNOWN")
            webbrowser.open_new_tab("http://localhost:8501/another_page")

        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()