import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go

# NASA API configuration
NASA_API_KEY = "h54FtvyFY4TGpzp7tBFCD2pmmAiC1rN74joa3hgE"
BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos"

def fetch_mars_photos(date):
    """Fetch Mars photos from Perseverance rover for a specific date"""
    params = {
        'api_key': NASA_API_KEY,
        'earth_date': date.strftime('%Y-%m-%d'),
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def main():
    st.title("Mars Weather & Imagery Dashboard 🔴")
    st.write("Explore the latest images from NASA's Perseverance rover on Mars!")

    # NEW: Add a sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # Date selector
        st.subheader("Select Date")
        selected_date = st.date_input("Choose Date", datetime.now() - timedelta(days=7))  #NEW
        
        # Camera selector
        camera_types = ["All Cameras", "NAVCAM_LEFT", "NAVCAM_RIGHT", "FRONT_HAZCAM_LEFT_A", 
                       "FRONT_HAZCAM_RIGHT_A", "REAR_HAZCAM_LEFT", "REAR_HAZCAM_RIGHT"]
        selected_camera = st.selectbox("Select Camera", camera_types)  #NEW
        
        # Display options
        max_images = st.slider("Maximum Images to Display", 1, 10, 5)  #NEW

    st.write(f"Fetching Mars images for: {selected_date}")
    
    # Fetch photos
    photos_data = fetch_mars_photos(selected_date)
    
    if photos_data and 'photos' in photos_data:
        photos = photos_data['photos']
        
        if not photos:
            st.warning(f"No photos available for {selected_date}. Try another date!")
            return
            
        # Filter by camera if specific camera selected
        if selected_camera != "All Cameras":
            photos = [photo for photo in photos if photo['camera']['name'] == selected_camera]
        
        # Display photos
        st.subheader(f"Mars Photos from {selected_date}")
        
        # Create columns for photos
        cols = st.columns(2)
        
        for idx, photo in enumerate(photos[:max_images]):
            with cols[idx % 2]:
                st.image(photo['img_src'], 
                        caption=f"Camera: {photo['camera']['name']} - Sol: {photo['sol']}")
                st.write(f"Earth Date: {photo['earth_date']}")
                
        # Display some statistics
        st.subheader("Image Statistics")
        total_photos = len(photos_data['photos'])
        cameras_used = len(set(photo['camera']['name'] for photo in photos_data['photos']))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Photos Available", total_photos)
        with col2:
            st.metric("Different Cameras Used", cameras_used)
            
        # Show camera distribution
        camera_counts = pd.DataFrame([
            {'camera': photo['camera']['name']} 
            for photo in photos_data['photos']
        ]).value_counts().reset_index()
        camera_counts.columns = ['Camera', 'Count']
        
        fig = px.bar(camera_counts, 
                    x='Camera', 
                    y='Count',
                    title='Distribution of Photos by Camera')
        st.plotly_chart(fig)
        
    else:
        st.error("Failed to fetch Mars photos. Please try again later.")
