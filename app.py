import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

# Timestamp and date information
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

# Autorefresh logic
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Define the file path
attendance_file = f"attendance_folder/attendance_{date}.csv"

# Check if the attendance file exists
if os.path.exists(attendance_file):
    try:
        # Read the attendance CSV file
        df = pd.read_csv(attendance_file)

        # Display the dataframe with style
        st.subheader(f"Attendance for {date}")
        st.dataframe(df.style.highlight_max(axis=0))

    except Exception as e:
        st.error(f"Error reading attendance file: {e}")
else:
    st.warning(f"No attendance file found for {date}. Please ensure attendance is taken.")

# Add footer or any additional information
st.write("*Note:* The app refreshes every 2 seconds to update attendance data.")