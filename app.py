import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from utils.image_utils import load_and_validate_image
from chains.decor_chain import get_decor_suggestions

# --- 1. Load Environment Variables ---
load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- NEW: Define Logo URL ---
# You can replace this with a local path: "logo.png" or your own URL
LOGO_URL = "https://placehold.co/100x100/262730/f0f2f6?text=LOGO"

# --- 2. Page Configuration ---
st.set_page_config(
    page_title="Deco - Customize your Room",
    page_icon=LOGO_URL,  # --- UPDATED: Use logo URL for icon ---
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
# --- Added columns for Logo and Title ---
title_col1, title_col2 = st.columns([1, 5]) # Small column for logo, large for title

with title_col1:
    # --- ADD YOUR LOGO HERE ---
    # --- UPDATED: Use logo URL variable ---
    st.image(LOGO_URL, width=100)

with title_col2:
    st.title("🛋️ AI Interior Designer")
    st.markdown("Upload an image of your room, describe your vision, and I'll give you a complete decoration plan!")

st.divider()

# --- 5. API Key Check ---
if not API_KEY:
    st.error("Error: GOOGLE_API_KEY not found. Please create a .env file with your key.")
    st.stop() # Stop the app if the key is missing

# --- 6. Initialize Session State ---
# This is the key to making results "stick"
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = None
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

# --- 7. Main App Logic ---
col1, col2 = st.columns([1, 1]) # 50/50 split

# --- Logic for handling button clicks ---
# We process the logic *before* drawing the output column
def clear_state():
    """Resets the session state to its defaults."""
    st.session_state.suggestions = None
    st.session_state.uploaded_image = None
    # We don't need to manually clear widgets if we use keys, 
    # but a rerun is cleaner.

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
    
    # --- Button columns for layout ---
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        generate_button = st.button("✨ Generate Decoration Plan", use_container_width=True)
    with btn_col2:
        revert_button = st.button("Clear & Start Over", on_click=clear_state, use_container_width=True)

    # --- Handle Generate Button Click ---
    if generate_button:
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        elif not user_prompt:
            st.warning("Please describe your vision for the room.")
        else:
            try:
                with st.spinner("Analyzing your room and designing your plan..."):
                    # Process the image and get suggestions
                    pil_image = load_and_validate_image(uploaded_file)
                    suggestions = get_decor_suggestions(
                        user_prompt=user_prompt,
                        pil_image=pil_image,
                        api_key=API_KEY
                    )
                    
                    # --- Store results in session state ---
                    st.session_state.suggestions = suggestions
                    st.session_state.uploaded_image = pil_image
                    
                    # Rerun to update the output column immediately
                    st.rerun()

            except ValueError as e:
                st.error(f"Image Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# col2 is for the output
with col2:
    st.subheader("3. Your New Look")

    # --- Display logic is now based on session state ---
    if st.session_state.suggestions:
        # If we have suggestions, display them
        st.image(st.session_state.uploaded_image, caption="Your Uploaded Room", width='stretch') # <-- UPDATED
        st.divider()
        st.markdown(st.session_state.suggestions)
    
    else:
        # This is the "empty state" placeholder
        st.info("Your new design plan will appear here once you click 'Generate'.")
        # Darker placeholder image
        st.image("https://placehold.co/600x400/3d3d4a/9292a0?text=Your%20Plan%20Appears%20Here", width='stretch') # <-- UPDATED

