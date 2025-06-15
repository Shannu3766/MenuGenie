from PIL import Image, ImageDraw, ImageFont
import os

def create_template_preview(template_name, description):
    # Create a new image with a white background
    width = 800
    height = 450  # 16:9 aspect ratio
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add a gradient background
    for y in range(height):
        r = int(255 * (1 - y/height))
        g = int(255 * (1 - y/height))
        b = int(255 * (1 - y/height))
        for x in range(width):
            image.putpixel((x, y), (r, g, b))
    
    # Add template name
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Draw template name
    text_width = draw.textlength(template_name, font=font)
    draw.text(((width - text_width) // 2, height // 3), template_name, fill='black', font=font)
    
    # Draw description
    try:
        desc_font = ImageFont.truetype("arial.ttf", 20)
    except:
        desc_font = ImageFont.load_default()
    
    text_width = draw.textlength(description, font=desc_font)
    draw.text(((width - text_width) // 2, height // 2), description, fill='gray', font=desc_font)
    
    # Save the image
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    image.save(os.path.join(os.path.dirname(__file__), f'{template_name}.jpg'))

# Create previews for each template
templates = [
    ('classic', 'Traditional layout with elegant design'),
    ('modern', 'Contemporary design with dynamic layout'),
    ('minimal', 'Clean and simple design')
]

for template_name, description in templates:
    create_template_preview(template_name, description) 