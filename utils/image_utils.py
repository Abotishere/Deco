from PIL import Image
import io

# A set of allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def load_and_validate_image(uploaded_file):
    """
    Loads an uploaded file from Streamlit, validates its extension,
    and returns a PIL Image object.

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
        # Check if there is a '.' and the part after it is in our allowed set
        file_ext = filename.split('.')[-1].lower()
        if not ('.' in filename and file_ext in ALLOWED_EXTENSIONS):
            raise ValueError(f"Invalid file type. Please upload a .png, .jpg, or .jpeg file.")
            
    except Exception:
        raise ValueError(f"Invalid file. Please upload a valid image file.")

    # 2. Load the file into a PIL Image object
    try:
        # Read the file's bytes from the uploaded file
        image_data = uploaded_file.getvalue()
        
        # Open the image from the in-memory bytes
        # io.BytesIO creates an "in-memory file" from the raw bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Best practice: Convert image to RGB. 
        # This standardizes the image format and removes the alpha (transparency) 
        # channel from PNGs, which is good for model compatibility.
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image
        
    except Exception as e:
        print(f"Error opening image: {e}")
        raise ValueError("The uploaded file appears to be corrupt or is not a valid image.")
