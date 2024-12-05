import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytesseract
import os
from langchain_google_genai import GoogleGenerativeAI
from gtts import gTTS
import tempfile

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = "Enter your API-Key"  
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit UI elements
st.set_page_config(layout="wide")
st.title(":red[***Empowering lives with an AI assistant designed to illuminate the world for the visually impaired.***]🤖")
st.subheader(':violet[***Bringing vision to life with image-based AI support.***]')
st.image(
    r"C:\Users\Riddhi\Desktop\Project Innomatics\myimage.png", 
    caption="Empowering Vision",  
    use_container_width=True 
)


# Streamlit Sidebar
st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #E6E6FA;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.title(":blue[Visual Empowerment Hub🚀]")
st.sidebar.markdown("### :red[Functions:]")
st.sidebar.markdown("""
- **Scene Understanding :**
  Gain insightful and detailed descriptions of your uploaded images, making the unseen comprehensible.
  
- **Text Recognition**: 
  Effortlessly extract text from images, whether it's from signs, documents, or product labels, ensuring nothing goes unread.
  
- **Text-to-Speech**: 
  Experience enhanced accessibility as extracted text and image descriptions come alive through clear and natural speech output.
  """)


# Apply custom CSS for styling file uploader label 
st.markdown(
    """
    <style>
    .file-uploader-label {
        font-size: 24px;  
        font-weight: bold;  
        color: green; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Apply custom CSS for styling for Select functionality
st.markdown(
    """
    <style>
    /* Style the selectbox label */
    label[for="Select Functionality"] {
        font-size: 18px; /* Adjust font size */
        font-weight: bold; /* Make it bold */
        color: green; /* Change label color */
    }

    /* Style the dropdown box */
    div[data-baseweb="select"] {
        background-color: #f0f8ff; /* Light blue background */
        border: 2px solid #4caf50; /* Green border */
        border-radius: 8px; /* Rounded corners */
        padding: 5px; /* Add padding inside the box */
    }

    /* Style the dropdown options */
    ul[role="listbox"] li {
        font-size: 16px; /* Option font size */
        color: #333; /* Option text color */
        background-color: #fff; /* Option background color */
        padding: 10px; /* Add padding for options */
        border-bottom: 1px solid #ddd; /* Divider between options */
    }

    /* Highlighted option style on hover */
    ul[role="listbox"] li:hover {
        background-color: #cfe2f3; /* Light blue hover background */
        color: #000; /* Text color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Functions
def generate_scene_description(prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([user_prompt, image_data])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error during OCR: {e}"

def generate_contextual_guidance(prompt,extracted_text):
    """Generate task-specific guidance using Google Generative AI."""
    try:
        input_text = f"{prompt}\nExtracted text: {extracted_text}"
        response = llm.generate(prompts=[input_text])  
        # Extract the generated text
        if response.generations and len(response.generations[0]) > 0:
            guidance_text = response.generations[0][0].text 
            return guidance_text
        else:
            return "No guidance could be generated. Please try again."
    except Exception as e:
        return f"Error: {e}"  

def text_to_speech(text):
    """Converts the given text to speech using gTTS."""
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            st.audio(temp_audio.name, format="audio/mp3")
    except Exception as e:
        st.error(f"Error during Text-to-Speech: {e}")

def prepare_image(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return {
            "mime_type": uploaded_file.type,
            "data": bytes_data,
        }
    else:
        st.warning("No file uploaded.")
        return None

# Input Prompt for Scene Understanding
user_prompt = """
As an AI assistant, your task is to provide detailed and insightful descriptions of images to aid visually impaired individuals. Analyze the given image and deliver a clear, comprehensive summary that includes the following:

***Scene Overview:*** Summarize the environment or setting (e.g., indoor, outdoor, nature, city, etc.).
***Location:*** Identify the specific location or context of the image.
***Key Objects and Features:*** Describe important objects in the scene, their placement, and any notable characteristics.
***People and Actions:*** If present, describe the individuals in the image, including their appearance, activities, or interactions.
***Colors and Lighting:*** Emphasize the primary colors, lighting conditions (bright, dim, etc.), and the overall mood or ambiance.
***Accessibility Guidance:*** Provide practical suggestions or warnings for individuals navigating the space (e.g., "Watch for steps" or "Be cautious of obstacles on the floor").
"""

# Main App Logic

# Display a custom label above the file uploader
st.markdown('<p class="file-uploader-label">Upload your image for analysis</p>', unsafe_allow_html=True)


#File Upload
uploaded_file = st.file_uploader(':violet[***Select your image🧐***]', type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
   
    
# Prepare image data
if uploaded_file:
    image_data = prepare_image(uploaded_file)

# Functionality selection with colors
    functionality = st.selectbox(
    "Select Functionality", 
    ["Describe Scene", "Extract Text", "Text to Speech","Context-Specific Guidance"],
    index=None,
    placeholder="Select function...",
   )
    
    # Scene Understanding
    if functionality == "Describe Scene":
        #st.markdown("<h3 style='color: blue;'>You selected 'Describe Image'.</h3>", unsafe_allow_html=True)
        with st.spinner("Analyzing the image..."):
            if image_data:
                description = generate_scene_description(user_prompt, image_data)
                st.success("### 🔍 Scene Description")
                st.write(description)
                 # Convert scene description to speech
                st.subheader("🔊 Play the Description of scene")
                text_to_speech(description)
            else:
                st.warning("Could not process the image. Please try again.")

    # Extract Text
    elif functionality == "Extract Text":
        #st.markdown("<h3 style='color: green;'>You selected 'Extract Text'.</h3>", unsafe_allow_html=True)
        with st.spinner("Extracting the text..."):
            extracted_text = extract_text_from_image(image)
            if extracted_text.strip():
                st.success("###  📝Text Extracted Successfully")
                st.text_area("Extracted Text", extracted_text, height=150)
            else:
                st.warning("No text found in the image. 😕.")

    # Text-to-Speech
    elif functionality == "Text to Speech":
        #st.markdown("<h3 style='color: orange;'>You selected 'Text to Speech'.</h3>", unsafe_allow_html=True)
        with st.spinner("Converting text to speech..."):
            extracted_text = extract_text_from_image(image)
            if extracted_text.strip():
                text_to_speech(extracted_text)
                st.success("Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text available for speech.")

    # Provide context-specific guidance
    elif functionality == "Context-Specific Guidance":
        with st.spinner("Generating context-specific guidance..."):
            extracted_text = extract_text_from_image(image)
            prompt = """
            You are an AI assistant helping visually impaired individuals. Based on the provided image:
            1. Analyze the extracted text for relevance.
            2. Provide context-specific recommendations based on the text.
            3. Suggest actions or precautions for the visually impaired.
            """
            guidance = generate_contextual_guidance(prompt, extracted_text)
            if guidance:
                st.success("Context-Specific Guidance:")
                st.write(guidance)
                st.subheader("🔊 Listen to Guidance")
                text_to_speech(guidance)
            else:
                st.warning("Could not generate guidance.")


