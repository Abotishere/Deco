from PIL import Image
import io

# A set of allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# A sensible maximum size for the AI to analyze
# The AI doesn't need an 8K photo. 1024x1024 is more than enough.
MAX_SIZE = (1024, 1024)

def load_and_validate_image(uploaded_file):
    """
    Loads an uploaded file from Streamlit, validates its extension,
    resizes it, and returns a PIL Image object.

    Args:
        uploaded_file: The file object from st.file_uploader()

    Returns:
        A PIL.Image.Image object if successful.
    Raises:
        ValueError: If the file type is not allowed or the file is corrupt.
    """
    
    if uploaded_file is None:
        return None

    # 1. Validate the file extension
    try:
        filename = uploaded_file.name
        file_ext = filename.split('.')[-1].lower()
        if not ('.' in filename and file_ext in ALLOWED_EXTENSIONS):
            raise ValueError(f"Invalid file type. Please upload a .png, .jpg, or .jpeg file.")
            
    except Exception:
        raise ValueError(f"Invalid file. Please upload a valid image file.")

    # 2. Load the file into a PIL Image object
    try:
        image_data = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_data))
        
        # 3. Resize the Image 
        # This is the crucial step to prevent long waits.
        # Image.thumbnail preserves the aspect ratio.
        image.thumbnail(MAX_SIZE, Image.LANCZOS)
        
        # 4. Convert to RGB (as before)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image
        
    except Exception as e:
        print(f"Error opening or processing image: {e}")
        raise ValueError("The uploaded file appears to be corrupt or is not a valid image.")

