# Face Recognition Attendance System

A real-time face recognition attendance tracker using OpenCV, Streamlit, and KNN (K-Nearest Neighbors).

This system allows you to register faces via webcam, recognize them in real-time, log attendance with timestamps, and view logs live through a Streamlit dashboard.

---

## Features

-  Register new faces using webcam  
-  Real-time face recognition using KNN  
-  Attendance logging with CSV output  
-  Live dashboard using Streamlit  
-  Auto-refreshing UI for real-time updates  
-  Voice feedback on attendance (Windows only)


##  Installation Instructions

1. Clone the repo  
   `git clone https://github.com/vanshika0423/face-attendance-system.git`

2. Move into the project folder  
   `cd face-attendance-system`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Register a face  
   `python main.py`

5. Start attendance system  
   `python test.py`

6. Open the dashboard  
   `streamlit run app.py`

---

##  Project Structure

├── main.py # Face registration
├── test.py # Attendance recognition
├── app.py # Streamlit dashboard
├── background.png # Background image for attendance UI
├── requirements.txt # List of dependencies
├── attendance_folder # Stores daily attendance CSVs
├── data # Stores face data and labels
└── README.md # Project documentation


