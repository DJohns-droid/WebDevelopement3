import streamlit as st
import google.generativeai as genai
import os
import requests

# Set API Keys
os.environ['GOOGLE_API_KEY'] = "AIzaSyD_BgTRB-GDl_QK6-Mfb0n3JWV-R5zIlk4"
NASA_API_KEY = "h54FtvyFY4TGpzp7tBFCD2pmmAiC1rN74joa3hgE"

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Helper function to fetch APOD data from NASA API
def fetch_apod(date=None):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    if date:
        url += f"&date={date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Error fetching APOD data: " + str(e))
        return {}

# Helper function to fetch EPIC data from NASA API
def fetch_epic_images():
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Error fetching EPIC data: " + str(e))
        return []

# Helper function to call Google Gemini for text generation
def generate_text(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error("Error generating text: " + str(e))
        return "Error generating response. Please try again."

# Streamlit UI
def main():
    st.title("NASA Data Assistant")

    # Astronomy Picture of the Day (APOD)
    st.header("Astronomy Picture of the Day")
    date = st.date_input("Select a date for the APOD:")
    if st.button("Get APOD Data"):
        apod_data = fetch_apod(date=date.isoformat())
        if apod_data:
            st.image(apod_data.get("url"), caption=apod_data.get("title"))
            st.write(apod_data.get("explanation"))
        else:
            st.error("No data available for the selected date.")

    # EPIC (Earth Polychromatic Imaging Camera) Images
    st.header("EPIC Images")
    if st.button("Get Latest EPIC Images"):
        epic_images = fetch_epic_images()
        if epic_images:
            for image in epic_images[:5]:  # Display up to 5 images
                image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{image['date'].replace('-', '/')}/png/{image['image']}.png"
                st.image(image_url, caption=image.get("caption"))
        else:
            st.error("No EPIC images available.")

    # Chatbot interaction
    st.header("Chat with NASA Data Assistant")
    user_question = st.text_input("Ask a question about NASA data:")

    if st.button("Ask Assistant"):
        if user_question:
            chatbot_prompt = (
                f"Provide an informative response based on NASA's data: {user_question}"
            )
            answer = generate_text(chatbot_prompt)
            st.write("Assistant Response:", answer)
        else:
            st.error("Please enter a question.")

if __name__ == "__main__":
    main()
