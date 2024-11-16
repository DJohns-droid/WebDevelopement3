import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 52, Web Development - Section C")
st.subheader("Team Members: Charlie Rivers, Daniel Johns")

# Image Display
profile_picture = "Images/homepage.jpg"
st.image(profile_picture, caption="Space Theme Image", width=300)

# Introduction
st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. Here's what you'll find:

1. **Charlie's Portfolio**: Get to know Charlie's background in Industrial Engineering, his leadership roles, and his love for tackling practical challenges.

2. **Daniel's Portfolio**: Check out Daniel's projects in software development, showcasing his creativity and team-oriented approach.

3. **Mars Dashboard**: See the latest photos from NASA's Perseverance rover on Mars! Pick a date and camera type to dive into the images and stats.

4. **NASA 2024 Pictures of the Day**: Choose a date in 2024 to view NASA's Astronomy Picture of the Day and ask questions about it.
""")
