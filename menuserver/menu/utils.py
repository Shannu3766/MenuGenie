import google.generativeai as genai
import os
import json
from PIL import Image
from django.conf import settings

def extract_menu_data(image_path):
    try:
        # Configure Gemini API
        GOOGLE_API_KEY = settings.GOOGLE_API_KEY
        if not GOOGLE_API_KEY:
            print("Error: GOOGLE_API_KEY is not set in settings")
            return None
            
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Load Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Open and process image
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {str(e)}")
            return None
        
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
        Make sure to return valid JSON format.
        """

        try:
            response = model.generate_content(
                [prompt, image],
                stream=False
            )
            
            if not response or not response.text:
                print("Error: Empty response from Gemini API")
                return None
                
            # Clean the response text to ensure it's valid JSON
            response_text = response.text.strip()
            
            # If the response is wrapped in markdown code blocks, remove them
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            try:
                # Parse Gemini's output into JSON
                data = json.loads(response_text)
                
                # Validate the data structure
                if not isinstance(data, list):
                    print("Error: Response is not a list")
                    return None
                    
                for section in data:
                    if not isinstance(section, dict) or 'section' not in section or 'items' not in section:
                        print("Error: Invalid section format")
                        return None
                    if not isinstance(section['items'], list):
                        print("Error: Items is not a list")
                        return None
                    for item in section['items']:
                        if not isinstance(item, dict) or 'item' not in item or 'price' not in item:
                            print("Error: Invalid item format")
                            return None
                
                return data
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")
                print("Raw response text:\n", response_text)
                return None
                
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Unexpected error in extract_menu_data: {str(e)}")
        return None 