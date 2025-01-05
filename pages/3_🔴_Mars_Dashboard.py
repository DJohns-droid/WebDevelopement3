import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

nasaApiKey = st.secrets["NASA"]  # NEW

apiBaseUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos"

@st.cache_data(ttl=3600)  # NEW
def fetchMarsPhotos(selectedDate, selectedCamera=None):
    apiParameters = {
        'api_key': nasaApiKey,
        'earth_date': selectedDate,
    }
    if selectedCamera and selectedCamera != "All Cameras":
        apiParameters['camera'] = selectedCamera

    try:
        apiResponse = requests.get(apiBaseUrl, params=apiParameters)
        apiResponse.raise_for_status()
        return apiResponse.json()
    except requests.exceptions.RequestException as error:
        st.error(f"Error fetching data: {error}")  # Existing
        return None

st.title("Mars Imagery Dashboard 🔴")
st.markdown("""
Explore the latest images from NASA's Perseverance rover on Mars! 
Select a date and camera type to view photos and statistics.
""")

# Sidebar
st.sidebar.header("Dashboard Controls")

defaultDate = datetime.now() - timedelta(days=7)
selectedDate = st.sidebar.date_input(  # NEW
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
selectedCamera = st.sidebar.selectbox(
    "Select Camera",
    cameraOptions,
    help="Choose which camera's photos to display"
)

maximumImages = st.sidebar.slider(
    "Maximum Images",
    min_value=1,
    max_value=10,
    value=4,
    help="Adjust how many images to display"
)

formattedDate = selectedDate.strftime('%Y-%m-%d')
marsPhotosData = fetchMarsPhotos(formattedDate, selectedCamera)

if marsPhotosData and 'photos' in marsPhotosData and marsPhotosData['photos']:
    marsPhotos = marsPhotosData['photos'][:maximumImages]

    imageColumns = st.columns(2)  # NEW
    for photoIndex, marsPhoto in enumerate(marsPhotos):
        columnIndex = photoIndex % 2
        column = imageColumns[columnIndex]
        imageUrl = marsPhoto['img_src']
        cameraName = marsPhoto['camera']['name']
        photoSol = marsPhoto['sol']
        photoCaption = f"Camera: {cameraName} - Sol: {photoSol}"
        column.image(
            imageUrl,
            caption=photoCaption,
            use_container_width=True
        )
        earthDate = marsPhoto['earth_date']
        column.markdown(f"**Earth Date:** {earthDate}")

    st.subheader("📊 Image Statistics")

    totalPhotosAvailable = len(marsPhotosData['photos'])
    cameraNameList = [photo['camera']['name'] for photo in marsPhotosData['photos']]
    uniqueCameraNames = set(cameraNameList)
    uniqueCamerasCount = len(uniqueCameraNames)

    metricsColumns = st.columns(2)  # NEW
    metricsColumns[0].metric("Total Photos Available", totalPhotosAvailable)  # NEW
    metricsColumns[1].metric("Different Cameras Used", uniqueCamerasCount)  # NEW

    cameraData = [{'camera': cameraName} for cameraName in cameraNameList]
    cameraDataFrame = pd.DataFrame(cameraData)

    cameraPhotoCounts = cameraDataFrame['camera'].value_counts().reset_index()
    cameraPhotoCounts.columns = ['Camera', 'Count']

    barChartFigure = px.bar(
        cameraPhotoCounts,
        x='Camera',
        y='Count',
        title='Distribution of Photos by Camera',
        color='Camera'
    )

    barChartFigure.update_layout(
        xaxis_title="Camera Type",
        yaxis_title="Number of Photos",
        showlegend=False
    )

    st.plotly_chart(barChartFigure)  # NEW
else:
    st.error("No photos found for the selected date and camera.")
