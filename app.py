import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from utils.image_utils import load_and_validate_image
from chains.decor_chain import get_decor_suggestions

# --- 1. Load Environment Variables ---
load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- 2. Page Configuration ---
st.set_page_config(
    page_title="Room Decorator AI",
    page_icon="🛋️",
    layout="wide"
)

# --- 3. Custom CSS for Styling (Dark Mode Friendly) ---
st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* Style for the columns to create "cards" */
    /* Adjusted for Dark Mode */
    [data-testid="column"] {
        background-color: #262730; /* Darker grey for dark mode */
        border: 1px solid #3d3d4a; /* Darker border */
        border-radius: 10px;
        padding: 20px !important; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Darker shadow */
        transition: box-shadow 0.3s ease-in-out;
    }
    
    [data-testid="column"]:hover {
         box-shadow: 0 6px 12px rgba(0,0,0,0.3); /* Even darker shadow on hover */
    }

    /* Style the "Generate" button */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        background-color: #0068c9;
        color: white;
        border-radius: 10px;
        border: none;
        transition: background-color 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
    }

    /* Style the file uploader */
    /* Adjusted for Dark Mode - subtle changes for visibility */
    .stFileUploader {
        background-color: #2e2f38; /* Slightly lighter than column background */
        border: 2px dashed #4a4b5b; /* Visible dashed border */
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Style the title and subheaders for dark mode readability */
    h1, h2, h3, h4, h5, h6 {
        color: #f0f2f6; /* Light text for dark background */
    }
    /* Ensure other text is readable */
    p, label, .stMarkdown {
        color: #c9c9d1; /* Lighter grey for general text */
    }


    </style>
    """, unsafe_allow_html=True)

# --- 4. UI Setup ---
st.title("🛋️ AI Interior Designer")
st.markdown("Upload an image of your room, describe your vision, and I'll give you a complete decoration plan!")

st.divider()

# --- 5. API Key Check ---
if not API_KEY:
    st.error("Error: GOOGLE_API_KEY not found. Please create a .env file with your key.")
    st.stop() # Stop the app if the key is missing

# --- 6. Main App Logic ---
col1, col2 = st.columns([1, 1]) # 50/50 split

with col1:
    st.subheader("1. Your Room & Vision")
    uploaded_file = st.file_uploader(
        "Upload a photo of your room:", 
        type=["jpg", "jpeg", "png"]
    )
    
    user_prompt = st.text_area(
        "Describe your desired style, budget, and colors:",
        height=150,
        placeholder="e.g., 'I want a cozy, minimalist style with a budget of $500. Focus on neutral colors and natural light.'"
    )
    
    generate_button = st.button("✨ Generate Decoration Plan")

# col2 is for the output
with col2:
    st.subheader("3. Your New Look")

    if generate_button:
        # --- 7. Input Validation ---
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        elif not user_prompt:
            st.warning("Please describe your vision for the room.")
        else:
            # --- 8. Process and Generate ---
            try:
                with st.spinner("Analyzing your room and designing your plan..."):
                    
                    # Load and validate the image using our util
                    pil_image = load_and_validate_image(uploaded_file)
                    
                    # Display the uploaded image
                    # --- FIX: Replaced use_column_width=True with width='stretch' ---
                    st.image(pil_image, caption="Your Uploaded Room", width='stretch')
                    
                    st.divider()

                    # Call the AI chain
                    suggestions = get_decor_suggestions(
                        user_prompt=user_prompt,
                        pil_image=pil_image,
                        api_key=API_KEY
                    )
                    
                    # Display the AI's formatted response
                    st.markdown(suggestions)

            except ValueError as e:
                st.error(f"Image Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    
    else:
        # This is the "empty state" placeholder, adjusted for dark mode
        st.info("Your new design plan will appear here once you click 'Generate'.")
        # Darker placeholder image
        # --- FIX: Replaced use_container_width=True with width='stretch' ---
        st.image("https://placehold.co/600x400/3d3d4a/9292a0?text=Your%20Plan%20Appears%20Here", width='stretch')

