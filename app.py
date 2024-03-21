import streamlit as st
import os
import pyttsx3  # Import pyttsx3 for potential text-to-speech
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

    # **Isolate Text-to-Speech Issues:**
    # Comment out the speak call temporarily to see if the error persists.

    # speak(response)  # Uncomment if text-to-speech is working

    st.text(response)
    return response

def main():
    st.title("Jarvis")

    # Initialize conversation history
    global chatStr
    chatStr = " "

    # Initial greeting (without TTS for now)
    st.write("Hello, I'm Jarvis. How can I assist you today?")

    query = st.text_input("You:")

    if st.button("Submit"):
        st.write("Jarvis is typing...")
        response = chat(query)
        st.write(f"Jarvis: {response}")

if __name__ == "__main__":
    main()
