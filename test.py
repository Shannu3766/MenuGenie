import google.generativeai as genai
import os
import json
from PIL import Image

# STEP 1: Set your API key
GOOGLE_API_KEY = 'AIzaSyA6vLseI5Aq3Fhgua8qPF_yGq-qj4o6mfk'  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# STEP 2: Load Gemini multimodal model
model = genai.GenerativeModel('gemini-1.5-flash')

# STEP 3: Function to extract structured menu data with sections
def extract_menu_with_sections(image_path):
    image = Image.open(image_path)

    prompt = """
    This is a restaurant menu. Extract all sections and within each section, list items and their prices.
    
    Return the result in this JSON format:
    [
      {
        "section": "Section Na
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
        # Try parsing Gemini's output into JSON
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("Error parsing response:", e)
        print("Raw response text:\n", response.text)
        return None

# STEP 4: Example usage
if __name__ == "__main__":
    image_path = 'OIP.jpg'  # Replace with the path to your image
    extracted_data = extract_menu_with_sections(image_path)
    if extracted_data:
        print(json.dumps(extracted_data, indent=2))
