import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configure page
st.set_page_config(page_title="Mars Weather Dashboard", layout="wide")

# Get API key from secrets
NASA_API_KEY = st.secrets["NASA"]

# NASA API configuration
BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos"

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def fetch_mars_photos(date_str, camera=None):
    """Fetch Mars photos from Perseverance rover for a specific date"""
    params = {
        'api_key': NASA_API_KEY,
        'earth_date': date_str,
    }
    if camera and camera != "All Cameras":
        params['camera'] = camera
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Title and description
st.title("Mars Weather & Imagery Dashboard 🔴")
st.markdown("""
Explore the latest images from NASA's Perseverance rover on Mars! 
Select a date and camera type to view photos and statistics.
""")

# Sidebar controls
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Date selector with a more reasonable default date
    default_date = datetime.now() - timedelta(days=7)
    selected_date = st.date_input(
        "Select Date",
        value=default_date,
        max_value=datetime.now(),
        help="Choose a date to view Mars photos"
    )
    
    # Camera selector
    camera_options = [
        "All Cameras",
        "NAVCAM_LEFT",
        "NAVCAM_RIGHT",
        "FRONT_HAZCAM_LEFT_A",
        "FRONT_HAZCAM_RIGHT_A",
        "REAR_HAZCAM_LEFT",
        "REAR_HAZCAM_RIGHT"
    ]
    selected_camera = st.selectbox(
        "Select Camera",
        camera_options,
        help="Choose which camera's photos to display"
    )
    
    # Display options
    max_images = st.slider(
        "Maximum Images",
        min_value=1,
        max_value=10,
        value=4,
        help="Adjust how many images to display"
    )

# Main content
date_str = selected_date.strftime('%Y-%m-%d')
photos_data = fetch_mars_photos(date_str, selected_camera)

if photos_data and 'photos' in photos_data and photos_data['photos']:
    photos = photos_data['photos'][:max_images]
    
    # Display photos in a grid
    cols = st.columns(2)
    for idx, photo in enumerate(photos):
        with cols[idx % 2]:
            st.image(
                photo['img_src'],
                caption=f"Camera: {photo['camera']['name']} - Sol: {photo['sol']}",
                use_column_width=True
            )
            st.markdown(f"**Earth Date:** {photo['earth_date']}")
            
    # Statistics section
    st.subheader("📊 Image Statistics")
    
    # Calculate statistics
    total_photos = len(photos_data['photos'])
    unique_cameras = set(photo['camera']['name'] for photo in photos_data['photos'])
    cameras_used = len(unique_cameras)
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Photos Available", total_photos)
    with col2:
        st.metric("Different Cameras Used", cameras_used)
        
    # Create camera distribution visualization
    camera_df = pd.DataFrame([
        {'camera': photo['camera']['name']} 
        for photo in photos_data['photos']
    ])
    
    camera_counts = camera_df['camera'].value_counts().reset_index()
    camera_counts.columns = ['Camera', 'Count']
    
    fig = px.bar(
        camera_counts,
        x='Camera',
        y='Count',
        title='Distribution of Photos by Camera',
        color='Camera'
    )
    
    fig.update_layout(
        xaxis_title="Camera Type",
        yaxis_title="Number of Photos",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No photos available for {date_str}. Try another date!")
