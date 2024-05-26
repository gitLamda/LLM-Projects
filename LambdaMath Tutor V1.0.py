# -*- coding: utf-8 -*-
"""
Created on Mon May 27 00:10:47 2024

@author: user
"""

import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key

genai.configure(api_key= google_gemini_api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# setting the page layout
st.set_page_config(layout = 'wide')

# setting the page title
st.title('LambdaMath Tutor V1.0')

# setting the subheader
st.subheader('Solve any math problem with detailed explanations')

# creating the side bar for user input
with st.sidebar:
    st.title('Input your Math Problem')
    
    st.subheader('Enter the math problem you want to solve')
    
    # math problem
    math_prob = st.text_input('Math Problem')
    
    submit_button = st.button('Solve')
    
if submit_button and math_prob:
    
    # create the prompt with the user input
    user_input = f"""
    You are a math tutor AI. Your task is to solve math problems and provide step-by-step explanations. The input will be a {math_prob}, and you should return the solution along with the steps taken to arrive at the answer. The types of problems can include basic arithmetic, algebra, geometry, calculus, and other advanced mathematics topics. Ensure that your explanations are clear and concise."""
    
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [user_input],
        },
      ]
    )

    response = chat_session.send_message(user_input)

    st.write(response.text)

else:
    st.write("Please enter your math problem")    