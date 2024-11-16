import requests
import streamlit as st
import google.generativeai as genai

# Access your Google Gemini API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI"]

# Configure the Google Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

# Function to fetch Mars weather data from MAAS2 API
def fetch_mars_weather():
    try:
        url = "https://api.maas2.apollorion.com/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from MAAS2 API: {e}")
        return None

def main():
    st.title("🚀 Mars Weather Assistant")
    st.write("Get customized Mars weather reports and interact with the Mars Weather Assistant.")

    # Fetch Mars weather data and store it in session state
    if 'mars_data' not in st.session_state:
        st.session_state.mars_data = fetch_mars_weather()

    mars_data = st.session_state.mars_data

    if mars_data:
        # Provide a brief explanation about Sol and Earth dates
        st.write("""
            **Sol**: A Martian day, approximately 24 hours and 39 minutes.

            **Latest Mars Weather Data:**
        """)
        st.write(f"**Sol {mars_data['sol']}, Earth Date: {mars_data['terrestrial_date']}**")

        # Display weather information
        st.write(f"**Season:** {mars_data['season'].capitalize()}")
        st.write(f"**Min Temperature:** {mars_data['min_temp']} °C")
        st.write(f"**Max Temperature:** {mars_data['max_temp']} °C")
        st.write(f"**Pressure:** {mars_data['pressure']} Pa")
        st.write(f"**Atmosphere Opacity:** {mars_data['atmo_opacity'].capitalize()}")
        st.write(f"**Sunrise:** {mars_data['sunrise']}")
        st.write(f"**Sunset:** {mars_data['sunset']}")

        # User inputs
        activity = st.text_input("Enter the type of activity (e.g., 'Mars rover operations'):")
        style = st.selectbox("Select report style:", ["scientific", "casual", "mission-focused"])

        if st.button("Generate Report"):
            if activity and style:
                st.session_state.weather_data = mars_data.copy()  # Use a copy to avoid modifying the original data
                # Add activity context to weather data
                st.session_state.weather_data['activity'] = activity
                # Generate weather report
                generate_weather_report(st.session_state.weather_data, style)
            else:
                st.error("Please fill in all the fields.")

        st.subheader("🛰️ Mars Weather Chatbot")
        st.write("Ask questions about Mars weather conditions, atmospheric phenomena, mission planning, and more.")

        if 'weather_data' in st.session_state and st.session_state.weather_data:
            mars_weather_chatbot(st.session_state.weather_data)
        else:
            st.info("Please generate a weather report first to start the chatbot.")
    else:
        st.error("Unable to fetch Mars weather data at this time.")

# Function to generate a weather report using Google Gemini LLM
def generate_weather_report(weather_data, style):
    try:
        # Construct the prompt
        prompt = f"Generate a {style} weather report for a Mars mission involving {weather_data['activity']} on Sol {weather_data['sol']} with the following data:\n\n"
        prompt += f"- Season: {weather_data['season'].capitalize()}\n"
        prompt += f"- Min Temperature: {weather_data['min_temp']} °C\n"
        prompt += f"- Max Temperature: {weather_data['max_temp']} °C\n"
        prompt += f"- Pressure: {weather_data['pressure']} Pa\n"
        prompt += f"- Atmosphere Opacity: {weather_data['atmo_opacity'].capitalize()}\n"
        prompt += f"- Sunrise: {weather_data['sunrise']}\n"
        prompt += f"- Sunset: {weather_data['sunset']}\n"

        # Generate text using the correct method
        response = genai.generate_text(prompt=prompt)
        st.subheader("Generated Weather Report:")
        st.write(response.result)
    except Exception as e:
        st.error(f"Error generating content with Google Gemini: {e}")

# Function to handle chatbot interaction
def mars_weather_chatbot(weather_data):
    try:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("You:", key="chat_input")

        if user_input:
            messages = [
                {"author": "system", "content": "You are a helpful Mars Weather Assistant."},
            ]

            # Include previous chat history
            for i in range(0, len(st.session_state.chat_history), 2):
                messages.append({"author": "user", "content": st.session_state.chat_history[i][1]})
                messages.append({"author": "assistant", "content": st.session_state.chat_history[i+1][1]})

            # Add the latest user input
            messages.append({"author": "user", "content": f"Using the following Mars weather data:\n\n{weather_data}\n\n{user_input}"})

            response = genai.generate_chat_message(messages=messages)
            assistant_reply = response.result

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Mars Assistant", assistant_reply))

            # Clear the input after submission
            st.experimental_rerun()

        # Display chat history
        for speaker, text in st.session_state.chat_history:
            st.write(f"**{speaker}:** {text}")
    except Exception as e:
        st.error(f"Error in chatbot interaction: {e}")

if __name__ == "__main__":
    main()
