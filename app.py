import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from utils.image_utils import load_and_validate_image
from chains.decor_chain import get_decor_suggestions

# --- 1. Load Environment Variables ---
# Load the .env file (which contains GOOGLE_API_KEY)
load_dotenv()

# Get the API key from the environment
API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- 2. Page Configuration ---
st.set_page_config(
    page_title="Room Decorator AI",
    page_icon="🛋️",
    layout="wide"
)

# --- 3. UI Setup ---
st.title("🛋️ AI Interior Designer")
st.markdown("Upload an image of your room and describe the style you want. I'll give you a complete decoration plan!")

# --- 4. API Key Check ---
if not API_KEY:
    st.error("Error: GOOGLE_API_KEY not found. Please create a .env file with your key.")
    st.stop() # Stop the app if the key is missing

# --- 5. Main App Logic ---
# Use columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Your Room")
    uploaded_file = st.file_uploader(
        "Upload a photo of your room:", 
        type=["jpg", "jpeg", "png"]
    )
    
    user_prompt = st.text_area(
        "2. Your Vision",
        height=150,
        placeholder="e.g., 'I want a cozy, minimalist style with a budget of $500. Focus on neutral colors and natural light.'"
    )
    
    generate_button = st.button("✨ Generate Decoration Plan")

# col2 is for the output
with col2:
    st.subheader("3. Your New Look")

    if generate_button:
        # --- 6. Input Validation ---
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        elif not user_prompt:
            st.warning("Please describe your vision for the room.")
        else:
            # --- 7. Process and Generate ---
            try:
                with st.spinner("Analyzing your room and designing your plan..."):
                    
                    # Load and validate the image using our util
                    pil_image = load_and_validate_image(uploaded_file)
                    
                    # Display the uploaded image
                    st.image(pil_image, caption="Your Uploaded Room", use_column_width=True)
                    
                    # Call the AI chain
                    suggestions = get_decor_suggestions(
                        user_prompt=user_prompt,
                        pil_image=pil_image,
                        api_key=API_KEY
                    )
                    
                    # Display the AI's formatted response
                    st.markdown(suggestions)

            except ValueError as e:
                # Catch errors from load_and_validate_image
                st.error(f"Image Error: {e}")
            except Exception as e:
                # Catch any other general errors
                st.error(f"An unexpected error occurred: {e}")

"""
# How to Run the App

1.  Make sure your virtual environment is activated (you see `(venv)` in your terminal).
2.  Make sure you are in the *root* of your `room_decorator` directory.
3.  Run the following command in your terminal:

    ```bash
    streamlit run app.py
    
"""