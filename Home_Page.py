import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 52, Web Development - Section C")
st.subheader("Team Members: Charlie Rivers, Daniel Johns")

# Image Upload
uploaded_image = st.file_uploader("Upload a space-themed image", type=["png", "jpg", "jpeg"])

# Introduction
st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Charlie's Portfolio**: A comprehensive overview of Charlie's educational background, professional experiences, projects, skills, and activities.

2. **Daniel's Portfolio**: A comprehensive overview of Daniel's educational background, professional experiences, projects, skills, and activities.

3. **Mars Dashboard**: Displays the latest weather data from Mars, powered by the NASA API.

4. **NASA 2024 Pictures of the Day**: A gallery of stunning images from NASA's Astronomy Picture of the Day collection for 2024.
""")
