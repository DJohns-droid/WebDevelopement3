import streamlit as st
from PIL import Image
import numpy as np

# Adjust page configuration to fit content better
st.set_page_config(layout="wide")

# Title of App
st.title("Web Development Lab03")

# Assignment Data
st.markdown("**CS 1301** | **Team 52, Web Development - Section C** | **Team Members: Charlie Rivers, Daniel Johns**")

# Image Display with Continuous Shake Effect
def apply_shake(image, intensity=5):
    offset_x = np.random.randint(-intensity, intensity)
    offset_y = np.random.randint(-intensity, intensity)
    return image.transform(
        image.size, Image.AFFINE, (1, 0, offset_x, 0, 1, offset_y)
    )

profile_picture = "Images/homepage.jpg"
image = Image.open(profile_picture).rotate(50, expand=True).resize((200, 200))

# Generate a shaken image on each refresh
shaken_image = apply_shake(image)
st.image(shaken_image, caption="Space Theme Image", use_column_width=False)

# Auto-refresh the page for continuous shake effect
st.experimental_rerun()

# Introduction
st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. Here's what you'll find:

1. **Charlie's Portfolio**: Get to know Charlie's background in Industrial Engineering, his leadership roles, and his love for tackling practical challenges.

2. **Daniel's Portfolio**: Check out Daniel's projects in software development, showcasing his creativity and team-oriented approach.

3. **Mars Dashboard**: See the latest photos from NASA's Perseverance rover on Mars! Pick a date and camera type to dive into the images and stats.

4. **NASA 2024 Pictures of the Day**: Choose a date in 2024 to view NASA's Astronomy Picture of the Day and ask questions about it.
""")
