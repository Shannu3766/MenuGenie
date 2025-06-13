import google.generativeai as genai
import os
import json
from PIL import Image
from django.conf import settings

def extract_menu_data(image_path):
    # Configure Gemini API
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Load Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Open and process image
    image = Image.open(image_path)
    
    prompt = """
    This is a restaurant menu. Extract all sections and within each section, list items and their prices.
    
    Return the result in this JSON format:
    [
      {
        "section": "Section Name",
        "items": [
          { "item": "Item Name", "price": "Price" },
          ...
        ]
      },
      ...
    ]

    Do not include decorative or non-menu text.
    Only return valid menu items grouped under appropriate sections.
    """

    response = model.generate_content(
        [prompt, image],
        stream=False
    )

    try:
        # Parse Gemini's output into JSON
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("Error parsing response:", e)
        print("Raw response text:\n", response.text)
        return None 