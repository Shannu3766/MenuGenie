# MenuGenie Server

MenuGenie is a Django-based web application for restaurant owners to digitize and manage their menus. It leverages Google Gemini AI to extract structured menu data from images, making menu creation fast and easy.

## Features
- User registration and authentication (with email verification)
- Restaurant owner and customer roles
- Create and manage restaurants and menus
- Upload menu images and extract menu sections/items/prices using Google Gemini AI
- Organize menu items by sections
- Add, edit, and delete menu items and sections
- Public and private menu views

## Technology Stack
- Python 3.x
- Django 5.2.3
- SQLite (default, can be changed)
- Google Gemini AI (for menu extraction)
- Pillow (image processing)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd menuserver
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Configuration
- **Google Gemini API Key:**
  - Set your Google Gemini API key in `menuserver/settings.py` as `GOOGLE_API_KEY`.
- **Email Settings:**
  - Configure SMTP settings in `menuserver/settings.py` for email verification.
- **Media and Static Files:**
  - Uploaded images are stored in the `media/` directory.

## Usage
- Register as a user (choose restaurant owner if you want to manage menus).
- Create a restaurant and upload a menu image to extract menu data automatically.
- Manage menu sections and items via the web interface.
- Customers can view public menus.

## Example: Extracting Menu from Image (Standalone)
You can test the Gemini AI extraction using `test.py`:
```bash
python test.py
```
Edit `test.py` to set your image path and API key.

## Dependencies
See `requirements.txt` for all dependencies:
- Django >= 5.2.3
- Pillow
- google-generativeai

## License
MIT License

## Contact
For questions or support, contact: 98sh32@gmail.com 