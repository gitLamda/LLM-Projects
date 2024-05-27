# -*- coding: utf-8 -*-
"""
Created on Sun May 26 10:23:02 2024

@author: user
"""

import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
from openai import OpenAI

header = {
  "authorization": st.secrets['API_KEY'],
  "content-type": "application/json"
}
client = OpenAI(api_key = API_KEY)

genai.configure(api_key=API_KEY)

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

# setting up our model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# setting the page layout
st.set_page_config(layout='wide')

# title of our app
st.title('LambdaBlogGen V1.0: Your AI Blogging Partner')

# create a subheader
st.subheader('Craft the perfect Blog with Lamda AI')

# creating the side bar for user input
with st.sidebar:
    st.title('Input your Blog details')
    st.subheader('Enter details of the Blog you want to create')
    
    # Blog title
    blog_title = st.text_input("Blog Title")
    # Keywords input
    keywords = st.text_input("Keywords (Comma - Separated)")
    
    # number of words the user needs
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=100)
    
    # user input for the number of images
    num_images = st.number_input("Number of images", min_value=0, max_value=10, step=1)
    
    # submit button
    submit_button = st.button("Generate")

# generate and display the blog in the main area
if submit_button and blog_title and keywords:
    
    # create the prompt with user inputs
    user_input = f"""
    Generate a comprehensive, engaging blog post relevant to the given title "{blog_title}" and keywords "{keywords}". 
    Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words in length, 
    suitable for an online audience. Ensure the content is original, informative and maintains a consistent tone throughout.
    """
    
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
    st.write("Please enter your Blog details in the sidebar to generate the Blog!")
