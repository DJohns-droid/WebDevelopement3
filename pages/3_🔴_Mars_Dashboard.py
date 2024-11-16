import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Mars Weather Dashboard", layout="wide")

nasaApiKey = st.secrets["NASA"]

baseUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos"

@st.cache_data(ttl=3600)
def fetchMarsPhotos(dateStr, camera=None):
    params = {
        'api_key': nasaApiKey,
        'earth_date': dateStr,
    }
    if camera and camera != "All Cameras":
        params['camera'] = camera

    try:
        response = requests.get(baseUrl, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

st.title("Mars Imagery Dashboard 🔴")
st.markdown("""
Explore the latest images from NASA's Perseverance rover on Mars! 
Select a date and camera type to view photos and statistics.
""")

with st.sidebar:
    st.header("Dashboard Controls")

    defaultDate = datetime.now() - timedelta(days=7)
    selectedDate = st.date_input(
        "Select Date",
        value=defaultDate,
        max_value=datetime.now(),
        help="Choose a date to view Mars photos"
    )

    cameraOptions = [
        "All Cameras",
        "NAVCAM_LEFT",
        "NAVCAM_RIGHT",
        "FRONT_HAZCAM_LEFT_A",
        "FRONT_HAZCAM_RIGHT_A",
        "REAR_HAZCAM_LEFT",
        "REAR_HAZCAM_RIGHT"
    ]
    selectedCamera = st.selectbox(
        "Select Camera",
        cameraOptions,
        help="Choose which camera's photos to display"
    )

    maxImages = st.slider(
        "Maximum Images",
        min_value=1,
        max_value=10,
        value=4,
        help="Adjust how many images to display"
    )

dateStr = selectedDate.strftime('%Y-%m-%d')
photosData = fetchMarsPhotos(dateStr, selectedCamera)

if photosData and 'photos' in photosData and photosData['photos']:
    photos = photosData['photos'][:maxImages]

    cols = st.columns(2)
    for idx, photo in enumerate(photos):
        colIndex = idx % 2
        with cols[colIndex]:
            imageUrl = photo['img_src']
            cameraName = photo['camera']['name']
            sol = photo['sol']
            caption = f"Camera: {cameraName} - Sol: {sol}"
            st.image(
                imageUrl,
                caption=caption,
                use_column_width=True
            )
            earthDate = photo['earth_date']
            st.markdown(f"**Earth Date:** {earthDate}")

    st.subheader("📊 Image Statistics")

    totalPhotos = len(photosData['photos'])
    cameraNames = [photo['camera']['name'] for photo in photosData['photos']]
    uniqueCameras = set(cameraNames)
    camerasUsed = len(uniqueCameras)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Photos Available", totalPhotos)
    with col2:
        st.metric("Different Cameras Used", camerasUsed)

    cameraList = [{'camera': name} for name in cameraNames]
    cameraDf = pd.DataFrame(cameraList)

    cameraCounts = cameraDf['camera'].value_counts().reset_index()
    cameraCounts.columns = ['Camera', 'Count']

    fig = px.bar(
        cameraCounts,
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

    st.plotly_chart(fig)
else:
    st.error("No photos found for the selected date and camera.")
