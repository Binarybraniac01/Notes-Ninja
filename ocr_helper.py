import google.generativeai as genai

from PIL import Image
import logging
import os

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise ValueError("Gemini API key is not configured")

def extract_text_from_image(image_path):

    try:
        image = Image.open(image_path)

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            contents=["Extract text from this image.", image]
        )

        text = response.text
        return text.strip()
    
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        raise Exception("Failed to extract text from image")





# Below is using the method from google api documentation
# from google import genai
# from google.genai import types

# from PIL import Image
# import logging
# import os

# logger = logging.getLogger(__name__)

# # Configure Gemini API
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# if not GEMINI_API_KEY:
#     logger.error("GEMINI_API_KEY environment variable is not set")
#     raise ValueError("Gemini API key is not configured")

# def extract_text_from_image(image_path):

#     try:
#         image = Image.open(image_path)
#         client = genai.Client(api_key=GEMINI_API_KEY)
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=["Extract text from this image.", image])

#         # print(response.text)
#         text = response.text
#         return text.strip()
    
#     except Exception as e:
#         logger.error(f"Error extracting text from image: {str(e)}")
#         raise Exception("Failed to extract text from image")

