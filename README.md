# Deco 🛋️

Room decoration AI agent.
A submission for Gemini Hackdays 2025 by Team khela hobe.

# 💡 About The Project

Deco is an interactive web application that acts as your personal AI interior designer. Users can upload a photo of their room, describe their desired style, and instantly receive a complete, AI-generated decoration plan.

This app leverages the power of Google's multimodal models (Gemini 2.5) to analyze the room's image and the user's text prompt, providing a customized plan, shopping list, and budget-aware suggestions.

# ✨ Features

Image Analysis: Understands the layout and content of the user's room from a photo.

AI Design: Generates a complete interior design plan based on user prompts (e.g., "minimalist," "boho," "mid-century modern").

Budget-Aware: Provides a shopping list with estimated price ranges, respecting the user's budget.

Interactive UI: Built with Streamlit for a simple, fast, and responsive user experience.

# 🛠️ Tech Stack

Frontend (UI): Streamlit

AI Orchestration: LangChain

AI Model: Google Gemini 2.5 Flash (via langchain-google-genai)

Image Handling: Pillow

Environment: Python 3.10+

# 🚀 Getting Started

Follow these steps to set up and run the project locally.

## Prerequisites

Python (3.10 or newer is recommended)

A Google API Key with the Gemini 2.5 models enabled. Get one from Google AI Studio.

## Project Structure
```
room_decorator/
│
├── app.py              # Streamlit entry point (UI + orchestration)
│
├── chains/
│   └── decor_chain.py  # LangChain logic: prompt templates, chain setup
│
├── utils/
│   └── image_utils.py  # Helpers: load image, validate, resize
│
├── .gitignore          # Tells Git what to ignore
│
├── requirements.txt    # All dependencies
│
└── README.md           # This file
```

## Installation & Setup

Step 1: Clone the repository (if applicable)
```
git clone https://github.com/Abotishere/Deco.git
cd Deco
```

Step 2: Create and activate a virtual environment

This is a best practice to keep dependencies isolated.

- On macOS/Linux:
```
python3 -m venv myvenv
source myvenv/bin/activate
```

- On Windows:
```
python -m venv venv
.\venv\Scripts\activate
```

Step 3: Install the required packages
```
pip install -r requirements.txt
```

Step 4: Create your API key file

Create a new file in the root directory named *.env* and add your API key to it:
```
.env
GOOGLE_API_KEY="YOUR_API_KEY_GOES_HERE"
```

## Running the Application

With your virtual environment still active, run the Streamlit app:
```
streamlit run app.py
```

Your default web browser should open automatically, pointing to your running application!
