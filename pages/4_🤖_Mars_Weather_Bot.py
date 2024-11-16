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
selectedDate = st.date_input("Select a date", min_value=date(1995, 6, 16), max_value=today, value=today)

# Fetch APOD Data from NASA API
def getApodData(date):
    formattedDate = date.strftime('%Y-%m-%d')
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={formattedDate}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            errorMessage = data['error']['message']
            st.error(errorMessage)
            return None
        return data
    except requests.exceptions.HTTPError as httpErr:
        statusCode = response.status_code
        if statusCode == 403:
            st.error("Access to the NASA APOD API is forbidden. Please check your API key and try again.")
        elif statusCode == 404:
            st.error("APOD data for the selected date is not available.")
        else:
            st.error(f"HTTP error occurred: {httpErr}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Display APOD Image and Description
apodData = getApodData(selectedDate)
if apodData:
    title = apodData.get('title', 'No Title')
    explanation = apodData.get('explanation', 'No Explanation Available')
    mediaType = apodData.get('media_type')
    mediaUrl = apodData.get('url')

    st.header(title)

    # Display the explanation above the image
    st.write(explanation)

    if mediaType == 'image':
        st.image(mediaUrl, caption=title)
    elif mediaType == 'video':
        st.video(mediaUrl)
    else:
        st.write("Media type not supported.")

    # Generate Specialized Text using Google Gemini API
    def generateApodSummary(apodData):
        title = apodData.get('title')
        description = apodData.get('explanation')
        prompt = (
            f"Provide an engaging summary for the following NASA Astronomy Picture of the Day titled '{title}'. "
            f"Description: {description}"
        )
        try:
            response = model.generate_content(prompt)
            summaryText = response.text
            return summaryText
        except Exception as e:
            st.error(f"An error occurred with the LLM: {e}")
            return None

    st.subheader("Generated Summary")

    # Show a spinner while the summary is being generated
    with st.spinner('Generating summary...'):
        summary = generateApodSummary(apodData)
    if summary:
        st.write(summary)

    # Chatbot Interface
    st.subheader("Ask Questions about the Picture")
    if 'chatHistory' not in st.session_state:
        st.session_state['chatHistory'] = []

    userQuestion = st.text_input("Enter your question here:")
    if st.button("Ask"):
        if userQuestion:
            # Update chat history with user's question
            st.session_state['chatHistory'].append({"role": "user", "content": userQuestion})

            # Prepare the conversation history for the model
            messages = []
            for msg in st.session_state['chatHistory']:
                role = msg['role'].capitalize()
                content = msg['content']
                message = f"{role}: {content}"
                messages.append(message)
            conversation = "\n".join(messages)

            # Build the prompt for the LLM
            pictureTitle = apodData.get('title')
            pictureDate = apodData.get('date')
            pictureDescription = apodData.get('explanation')
            prompt = (
                f"You are an expert on astronomy and the NASA Astronomy Picture of the Day (APOD). "
                f"The picture is titled '{pictureTitle}' and was taken on {pictureDate}. "
                f"Here is a description: {pictureDescription}\n"
                f"Conversation:\n{conversation}\nAssistant:"
            )
            try:
                # Show a spinner while the assistant is generating a response
                with st.spinner('Processing your question...'):
                    response = model.generate_content(prompt)
                assistantReply = response.text.strip()
                # Update chat history with assistant's reply
                st.session_state['chatHistory'].append({"role": "assistant", "content": assistantReply})
            except Exception as e:
                st.error(f"An error occurred with the LLM: {e}")
                assistantReply = "I'm sorry, I couldn't process that request."

    # Display the conversation history
    for msg in st.session_state['chatHistory']:
        role = msg['role']
        content = msg['content']
        if role == 'user':
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Assistant:** {content}")

else:
    st.warning("Please select a valid date for which APOD data is available.")
