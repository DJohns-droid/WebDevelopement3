# NASA Space Exploration Dashboard

## Overview
This interactive web application provides access to NASA's space imagery through two main components:
1. **Mars Imagery Dashboard**: Displays real-time photos from NASA's Perseverance rover on Mars
2. **NASA Astronomy Picture of the Day (APOD) Explorer**: Browse daily astronomy pictures with AI-enhanced features

## Features

### Mars Imagery Dashboard 🔴
- Select specific dates to view Martian photos
- Filter by different rover cameras (navigation cameras, hazard avoidance cameras)
- Adjust how many images to display (1-10)
- View statistics about photo distribution across different cameras
- See metadata including Earth date and Martian sol (day count)

### NASA Astronomy Picture of the Day Explorer 📷
- Browse or randomly select astronomy pictures from 2024
- View high-quality images or embedded videos
- Read official NASA explanations
- Get AI-generated summaries of each picture (using Google's Gemini AI)
- Chat with an AI assistant to ask questions about the astronomy content

## Technical Highlights
- **Streamlit Framework**: Built using Python's Streamlit for rapid web application development
- **NASA APIs**: Integrated with NASA's Mars Rover Photos API and Astronomy Picture of the Day API
- **AI Integration**: Uses Google's Gemini AI to generate summaries and answer user questions
- **Data Visualization**: Includes interactive charts showing photo distribution statistics
- **Responsive Design**: Adapts layout based on screen size and number of images
- **Caching**: Implements data caching to improve performance and reduce API calls
- **Session Management**: Maintains user state across interactions

## Setup and Installation

### Prerequisites
- Python 3.7+
- Streamlit
- NASA API key
- Google Gemini AI API key

## Usage
- Access the Mars Imagery Dashboard to explore Mars rover photos
- Use the NASA APOD Explorer to view and learn about astronomical phenomena
- Interact with the AI assistant to get more information about space imagery
