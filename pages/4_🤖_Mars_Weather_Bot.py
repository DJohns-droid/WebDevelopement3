import os
import requests
import streamlit as st
import google.generativeai as genai

NASA_API_KEY = st.secrets["NASA"]
GEMINI_API_KEY = st.secrets["GEMINI"]

genai.configure(api_key=GEMINI_API_KEY)

def fetch_mars_weather():
    try:
        url = f"https://api.nasa.gov/insight_weather/?api_key={NASA_API_KEY}&feedtype=json&ver=1.0"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from NASA API: {e}")
        return None

def main():
    st.title("🚀 Mars Weather Assistant")
    st.write("Get customized Mars weather reports and interact with the Mars Weather Assistant.")

    if 'mars_data' not in st.session_state:
        st.session_state.mars_data = fetch_mars_weather()

    mars_data = st.session_state.mars_data

    if mars_data:
        sol_keys = mars_data.get('sol_keys', [])

        if not sol_keys:
            st.error("No Sol data available.")
            return

        st.write("Select a Martian day (Sol) for weather analysis. A 'Sol' is a Martian day, which is approximately 24 hours and 39 minutes longer than an Earth day.")

        sol_options = []
        for sol in sol_keys:
            first_UTC = mars_data[sol].get('First_UTC', '')
            if first_UTC:
                earth_date = first_UTC.split('T')[0]
                sol_option = f"Sol {sol} (Earth date: {earth_date})"
            else:
                sol_option = f"Sol {sol}"
            sol_options.append((sol, sol_option))

        selected_sol_option = st.selectbox("Select a Martian day (Sol):", [option[1] for option in sol_options])
        selected_sol = next(sol for sol, option in sol_options if option == selected_sol_option)

        activity = st.text_input("Enter the type of activity (e.g., 'Mars rover operations'):")
        style = st.selectbox("Select report style:", ["scientific", "casual", "mission-focused"])

        if st.button("Generate Report"):
            if selected_sol and activity and style:
                weather_data = mars_data[selected_sol]
                st.session_state.weather_data = weather_data
                weather_data['activity'] = activity
                generate_weather_report(weather_data, style)
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

def generate_weather_report(weather_data, style):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Generate a {style} weather report for a Mars mission involving {weather_data['activity']} on Sol {weather_data.get('sol', 'N/A')} with the following data: {weather_data}"
        response = model.generate_content(prompt)
        st.subheader("Generated Weather Report:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating content with Google Gemini: {e}")

def mars_weather_chatbot(weather_data):
    try:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        user_input = st.text_input("You:", key="chat_input")
        if user_input:
            model = genai.GenerativeModel("gemini-1.5-chat")
            prompt = f"Using the following Mars weather data: {weather_data}, answer the question: {user_input}"
            response = model.generate_content(prompt)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Mars Assistant", response.text))
            st.experimental_rerun()
        for speaker, text in st.session_state.chat_history:
            st.write(f"**{speaker}:** {text}")
    except Exception as e:
        st.error(f"Error in chatbot interaction: {e}")

if __name__ == "__main__":
    main()
