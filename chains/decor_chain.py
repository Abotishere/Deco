import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def get_decor_suggestions(user_prompt: str, pil_image, api_key: str):
    """
    Takes a user's prompt and a PIL image, sends them to the Gemini Vision model,
    and returns the AI-generated decoration suggestions.
    """
    
    # Set the API key
    os.environ["GOOGLE_API_KEY"] = api_key

    # Initialize the ChatGoogleGenerativeAI model for vision
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # This is the main system prompt that instructs the AI on its role and output format.
    system_instruction = """
    You are an expert interior designer AI. A user will provide you with an image 
    of their room and a text prompt describing their desired style, budget, and 
    any other preferences.

    Your task is to analyze the image and the prompt, then provide a 
    comprehensive decoration plan.

    Please format your response clearly and concisely in Markdown:

    ## 1. Decoration Plan
    * **Style Analysis:** Briefly describe the current room and the requested style (e.g., "mid-century modern", "minimalist", "boho").
    * **Color Palette:** Suggest a color scheme (e.g., "Primary: Off-white, Secondary: Sage Green, Accent: Gold"). Add more elements if needed
    * **Furniture & Arrangement:** Suggest new furniture or how to rearrange existing items.
    * **Lighting & Decor:** Recommend lighting, plants, art, wall paintings and other decorative items.

    ## 2. Shopping List
    Provide a bulleted list of suggested items to buy. For each item, 
    include a description and an estimated price range that respects the user's budget.
    
    * **[Item 1]:** [Description] (Est. Price: $X - $Y)
    * **[Item 2]:** [Description] (Est. Price: $X - $Y)
    * ...

    ## 3. Budget Summary
    Briefly confirm that this plan aligns with the user's stated budget. 
    If no budget was given, provide a total estimated cost range for your suggestions.
    """

    # We create a HumanMessage that contains a list of content parts:
    # 1. The main instruction prompt (text)
    # 2. The user's specific request (text)
    # 3. The user's uploaded image
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": system_instruction,
            },
            {
                "type": "text", 
                "text": f"Here is my request: {user_prompt}"
            },
            {
                "type": "image_url",
                "image_url": pil_image,
            },
        ]
    )

    # Invoke the model with the combined message
    try:
        response = llm.invoke([message])
        return response.content
    except Exception as e:
        # Handle potential API errors or other issues
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an error trying to generate suggestions. Please check your API key and try again."