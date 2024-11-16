# mars_weather_assistant.py

import streamlit as st
import requests
import google.generativeai as genai
import os
from datetime import datetime, date

# Set your API keys securely
NASA_API_KEY = st.secrets["NASA"]
os.environ['GOOGLE_API_KEY'] = st.secrets["GEMINI"]

# Configure Google Gemini API
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")  # Free model of Google Gemini

# Streamlit App
st.title("NASA Astronomy Picture of the Day")
st.write("Select a date to view the Astronomy Picture of the Day and ask questions about it.")

# User Input: Date Selection
today = date.today()
selected_date = st.date_input("Select a date", min_value=date(1995, 6, 16), max_value=today, value=today)

# Fetch APOD Data from NASA API
def get_apod_data(date):
    formatted_date = date.strftime('%Y-%m-%d')
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={formatted_date}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            st.error(data['error']['message'])
            return None
        return data
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            st.error("Access to the NASA APOD API is forbidden. Please check your API key and try again.")
        elif response.status_code == 404:
            st.error("APOD data for the selected date is not available.")
        else:
            st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Display APOD Image and Description
apod_data = get_apod_data(selected_date)
if apod_data:
    st.header(apod_data.get('title', 'No Title'))

    # Display the explanation above the image
    st.write(apod_data.get('explanation', 'No Explanation Available'))

    if apod_data.get('media_type') == 'image':
        st.image(apod_data.get('url'), caption=apod_data.get('title'))
    elif apod_data.get('media_type') == 'video':
        st.video(apod_data.get('url'))
    else:
        st.write("Media type not supported.")

    # Generate Specialized Text using Google Gemini API
    def generate_apod_summary(apod_data):
        prompt = f"Provide an engaging summary for the following NASA Astronomy Picture of the Day titled '{apod_data.get('title')}'. Description: {apod_data.get('explanation')}"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"An error occurred with the LLM: {e}")
            return None

    st.subheader("Generated Summary")

    # Show a spinner while the summary is being generated
    with st.spinner('Generating summary...'):
        summary = generate_apod_summary(apod_data)
    if summary:
        st.write(summary)

    # Chatbot Interface
    st.subheader("Ask Questions about the Picture")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_question = st.text_input("Enter your question here:")
    if st.button("Ask"):
        if user_question:
            st.session_state['chat_history'].append({"role": "user", "content": user_question})
            # Prepare the conversation history for the model
            conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state['chat_history']])
            prompt = (
                f"You are an expert on astronomy and the NASA Astronomy Picture of the Day (APOD). "
                f"The picture is titled '{apod_data.get('title')}' and was taken on {apod_data.get('date')}. "
                f"Here is a description: {apod_data.get('explanation')}\n"
                f"Conversation:\n{conversation}\nAssistant:"
            )
            try:
                # Show a spinner while the assistant is generating a response
                with st.spinner('Processing your question...'):
                    response = model.generate_content(prompt)
                assistant_reply = response.text.strip()
                st.session_state['chat_history'].append({"role": "assistant", "content": assistant_reply})
            except Exception as e:
                st.error(f"An error occurred with the LLM: {e}")
                assistant_reply = "I'm sorry, I couldn't process that request."

    # Display the conversation history
    for msg in st.session_state['chat_history']:
        if msg['role'] == 'user':
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

else:
    st.warning("Please select a valid date for which APOD data is available.")
