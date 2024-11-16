import streamlit as st
import google.generativeai as genai
import os
import requests

# Set API Keys
os.environ['GOOGLE_API_KEY'] = "AIzaSyD_BgTRB-GDl_QK6-Mfb0n3JWV-R5zIlk4"
NASA_API_KEY = "h54FtvyFY4TGpzp7tBFCD2pmmAiC1rN74joa3hgE"

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Helper function to fetch Mars weather data from NASA API
def fetch_mars_weather():
    url = f"https://api.nasa.gov/insight_weather/?api_key={NASA_API_KEY}&feedtype=json&ver=1.0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error("Error fetching Mars weather data: " + str(e))
        return {}

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
    st.title("Mars Weather Assistant Page")

    # User Inputs
    st.write("Mars uses a time system based on sols, which are roughly 24 hours and 39 minutes long. Below is a list of available dates for Mars weather.")
    mars_weather_data = fetch_mars_weather()
    if mars_weather_data:
        available_sols = list(mars_weather_data.get("sol_keys", []))
        if available_sols:
            selected_sol = st.selectbox("Select a Sol date (Martian day):", available_sols)
            activity_type = st.selectbox(
                "Select an activity type:",
                ["Rover Operations", "Outdoor Exploration", "Mission Planning"]
            )

            specific_concern = st.text_area("Describe specific weather concerns or questions:")

            if st.button("Get Mars Weather Data"):
                weather_data = mars_weather_data.get(selected_sol, {})
                if weather_data:
                    st.write(f"Mars Weather Data for Sol {selected_sol}:", weather_data)
                    # Generate daily weather report
                    prompt = (
                        f"Generate a {activity_type.lower()} weather report for Mars on Sol {selected_sol}. "
                        f"Include details on weather conditions and recommendations for activities."
                    )
                    report = generate_text(prompt)
                    st.write("Generated Weather Report:", report)
                else:
                    st.error("Weather data is not available for the selected Sol date.")
        else:
            st.error("No available Sol dates found in the data.")
    else:
        st.error("Unable to fetch Mars weather data. Please try again later.")

    # Chatbot interaction
    st.write("### Chat with the Mars Weather Assistant")
    user_question = st.text_input("Ask a question about Mars weather conditions:")

    if st.button("Ask Mars Assistant"):
        if user_question:
            chatbot_prompt = (
                f"Answer the following question based on Mars weather data and knowledge of Mars: {user_question}"
            )
            answer = generate_text(chatbot_prompt)
            st.write("Assistant Response:", answer)
        else:
            st.error("Please enter a question.")

if __name__ == "__main__":
    main()
