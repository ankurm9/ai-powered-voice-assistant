import streamlit as st
import os
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import google.generativeai as genai

# Function to handle the conversation
def chat(query):
    global chatStr

    # Configuring generative AI
    genai.configure(api_key=st.secrets["API_KEY"])
    chatStr += f"You: {query} \n Jarvis: "

    # Generation configuration and safety settings
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    # Creating the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Starting the chat and getting response
    response = model.start_chat(history=[])
    response.send_message(chatStr)
    response = response.last.text
    chatStr += f"{response}\n"

    # Choose one of the following methods for text-to-speech:

    # Method 1: Using pyttsx3 (if dependencies are installed)
    try:
        # Create a TTS engine (if pyttsx3 works)
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()
    except (ImportError, OSError):  # Handle potential errors
        st.error("Text-to-speech functionality is unavailable. Consider a cloud service.")

    # Method 2: Using a cloud text-to-speech service (replace with your chosen service)
    # You'll need to implement the logic to interact with the cloud service API
    # here, potentially using libraries like requests.

    st.text(response)
    return response

def main():
    st.title("Jarvis")

    # Initialize conversation history
    global chatStr
    chatStr = " "

    speak("Hello, I'm Jarvis. How can I assist you today?")  # Initial greeting (without TTS)

    query = st.text_input("You:")

    if st.button("Submit"):
        st.write("Jarvis is typing...")
        response = chat(query)
        st.write(f"Jarvis: {response}")

if __name__ == "__main__":
    main()
