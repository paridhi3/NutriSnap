from dotenv import load_dotenv
load_dotenv()      # loading all environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini Pro Model and get responses
model = genai.GenerativeModel('gemini-pro-vision')
def get_gemini_response(input_prompt, image):
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_details(uploaded_file):

    # Check if file is uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# STREAMLIT APP
st.set_page_config(page_title="NutriSnap 🥗🍎")
st.markdown("<h1>NutriSnap 🥗🍎</h1>", unsafe_allow_html=True)
st.markdown("<h2>Capture, Analyze, and Optimize Your Meals with NutriSnap!</h2>", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize session state for chat history visibility if it doesn't exist
if 'show_chat_history' not in st.session_state:
    st.session_state['show_chat_history'] = False

uploaded_file = st.file_uploader("Upload food image: ", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake
is below format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----

Finally, you must also mention if the food is healthy or not (as briefly as possible), also 
mentioning the percentage split of the ratio of carbohydrates, fats, fibres, sugar, proteins, 
and other important nutrients required for human body.
"""

caption_prompt = """
You are a foodie and know all kinds of foods around the world. Based
on the image, generate a short caption describing the food in the image. After
the caption, add the word "image".
For example, if the caption is "mushroom soup", then the final caption will be "mushroom soup image".
Give only the caption and no other explanation.
Refrain from using racial words like "punjabi", "gujarati" etc. Include actual name of the dish.
"""

submit = st.button("Submit")
# When submit is clicked
if submit and uploaded_file:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)  
    caption = get_gemini_response(caption_prompt, image_data)
    
    # Append user input and response to chat history
    # st.session_state['chat_history'].append(("You", caption))
    # st.session_state['chat_history'].append(("BOT", response))
    st.session_state['chat_history'].append((f"**YOU**", caption))
    st.session_state['chat_history'].append((f"**BOT**", response))

    st.subheader("Answer")
    st.write(response)

# Button to toggle chat history visibility
if st.button("Show Chat History"):
    if not st.session_state['chat_history']:
        st.write("No chat history yet.")
    else:
        st.session_state['show_chat_history'] = not st.session_state['show_chat_history']

# Only display chat history if the button has been toggled to show
if st.session_state['show_chat_history'] and st.session_state['chat_history']:
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
