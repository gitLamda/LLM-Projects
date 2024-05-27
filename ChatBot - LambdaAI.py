# -*- coding: utf-8 -*-
"""
Created on Tue May 28 00:18:55 2024

@author: user
"""

import os
import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key

# Configure the Gemini API
genai.configure(api_key=google_gemini_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Setting up the Streamlit page layout
st.set_page_config(page_title="Lambda.ai", layout='wide')

# Add logo
#st.image("path_to_logo.png", use_column_width=True)  # Replace "path_to_logo.png" with the path to your logo file

# Title and subheader
st.title('⋀ LambdaAI - v5.0')
st.subheader('Your AI Companion')

# User input section
user_input = st.text_input("You:")

# Creating a button
submit = st.button("Hit me! ➤")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if submit and user_input:
    # Generate a title based on user input
    title_prompt = f"Generate a concise, catchy title based on the following context: {user_input}"
    
    # Start chat session with the model
    title_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [title_prompt],
            },
        ]
    )

    # Get the title from the model
    title_response = title_session.send_message(title_prompt)
    generated_title = title_response.text.strip().split('\n')[0]  # Assuming the first line is the title

    # Start chat session for the main response
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [user_input],
            },
        ]
    )

    # Get the response from the model
    response = chat_session.send_message(user_input)

    # Update chat history
    st.session_state.chat_history.append({"user": user_input, "bot": response.text, "title": generated_title})

    # Display the generated title and response
    st.write("### Generated Title")
    st.write(generated_title)
    st.write("### Chatbot Response")
    st.write(response.text)

# Sidebar for chat history
st.sidebar.title("Chat History")
clear_history = st.sidebar.button("Clear Chat History")

if clear_history:
    st.session_state.chat_history = []

for i, chat in enumerate(st.session_state.chat_history):
    st.sidebar.write(f"**You:** {chat['user']}")
    st.sidebar.write(f"**LambdaAI:** {chat['bot']}")
    st.sidebar.write(f"**Title:** {chat['title']}")
    st.sidebar.write("---")
