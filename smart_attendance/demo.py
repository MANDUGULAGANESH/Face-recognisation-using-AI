import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import subprocess

# Set the page configuration
st.set_page_config(page_title="Smart Attendance", page_icon="🤓", layout="wide")

# CSS styling for centered elements
st.markdown("""
    <style>
        .centered-image {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Centered Title
st.markdown('<h1 style="color: rgb(102, 12, 99);"><center>Handle Smartly</center></h1>', unsafe_allow_html=True)

# Horizontal Menu
selected = option_menu(
    None,
    options=["Home", "Time-Table", "Contact"],
    icons=["house", "calendar-check", "person-lines-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Home Section
if selected == "Home":
    st.subheader("Every day counts")
    st.markdown('<center><img src="https://miro.medium.com/v2/resize:fit:679/1*DKSQVZdEa2GEv2ksxWViTg.gif" alt="Your Image" style="width: 390px; height: 400px;">', unsafe_allow_html=True)
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    st.write("Current Date and Time:", formatted_datetime)
    
    if st.button("Verify my ID"):
        subprocess.run(["python", "attendance.py"])

# Time-Table Section
elif selected == "Time-Table":
    st.subheader("Plan your day ahead")
    timetable_path = "images/time_table1.jpg"  # Adjust the filename as needed
    try:
        st.image(timetable_path, caption="Your Time Table", width=600,use_column_width=True)
    except FileNotFoundError:
        st.error("The timetable image was not found. Please check the file path.")

# Contact Section
elif selected == "Contact":
    st.subheader("Any issues....!!!!")
    # Additional content for the Contact section can go here
