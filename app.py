import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)

# --- Helper function for text size ---
def get_text_size(font, text):
    """Calculates the bounding box of the text for proper placement."""
    bbox = font.getbbox(text)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])

# --- ID Card Generation Logic ---
def generate_college_id_card(student_info, photo_data):
    """
    Generates a college ID card image based on student information and a photo.

    Args:
        student_info (dict): A dictionary containing student details like 'name',
                             'fname', 'roll_no', 'branch', 'session',
                             'blood_group', 'dob', 'address'.
        photo_data: A file-like object (e.g., from request.files['photo'].stream)
                    containing the student's photo.
    Returns:
        PIL.Image.Image: The generated ID card image.
    """
    width, height = 400, 350
    id_card = Image.new("RGB", (width, height), (255, 255, 255)) # White background
    draw = ImageDraw.Draw(id_card)

    # --- Font Loading ---
    try:
        # Try to load common system fonts. You might need to adjust paths
        # or include a specific .ttf file in your 'static' directory.
        small_font = ImageFont.truetype("arial.ttf", 12)
        medium_font = ImageFont.truetype("arial.ttf", 14)
        large_font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        # Fallback to default Pillow font if specified fonts are not found
        print("Warning: arial.ttf not found, using default font. ID card may look different.")
        small_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        large_font = ImageFont.load_default()

    default_font = ImageFont.load_default() # Used for student details
    text_color = (0, 0, 122)  # Dark blue
    govt_text_color = (0, 128, 0) # Green for Govt. text

    # --- Headers ---
    # Centering text by calculating width and positioning
    govt_text = "Govt. of Bihar"
    w, h = get_text_size(small_font, govt_text)
    draw.text(((width - w) // 2, 10), govt_text, font=small_font, fill=govt_text_color)

    dept_text = "Department of Science & Technology"
    w, h2 = get_text_size(small_font, dept_text)
    draw.text(((width - w) // 2, 10 + h + 5), dept_text, font=small_font, fill=text_color)

    college_text = "GAYA COLLEGE OF ENGINEERING, GAYA"
    w, h3 = get_text_size(large_font, college_text)
    draw.text(((width - w) // 2, 10 + h + h2 + 10), college_text, font=large_font, fill=text_color)

    address_text = "Sri Krishan Nagar P.O Nagriyawan Khizersari, Gaya-823003"
    w, h4 = get_text_size(small_font, address_text)
    draw.text(((width - w) // 2, 10 + h + h2 + h3 + 15), address_text, font=small_font, fill=text_color)

    # --- ID Card Banner (Purple background with white text) ---
    student_id_text = "STUDENT IDENTITY CARD"
    w, h5 = get_text_size(medium_font, student_id_text)
    banner_y_start = 10 + h + h2 + h3 + h4 + 20
    rect_x1, rect_y1 = (width - w) // 2 - 5, banner_y_start - 5
    rect_x2, rect_y2 = rect_x1 + w + 10, rect_y1 + h5 + 10
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill="purple")
    draw.text(((width - w) // 2, rect_y1 + 5), student_id_text, font=medium_font, fill="white")

    # --- Student photo ---
    photo_size = (70, 80)
    photo_position = (width - 80, rect_y2 + 15) # Position from right edge

    try:
        if photo_data:
            # Open photo from the provided file-like object
            photo = Image.open(photo_data).resize(photo_size)
        else:
            # Placeholder if no photo is provided
            photo = Image.new("RGB", photo_size, (200, 200, 200)) # Grey placeholder
            draw_placeholder = ImageDraw.Draw(photo)
            draw_placeholder.text((5, 30), "No Photo", font=small_font, fill=(0,0,0))
    except Exception as e:
        print(f"Error processing photo: {e}")
        # Fallback to a placeholder if photo loading fails
        photo = Image.new("RGB", photo_size, (200, 200, 200))
        draw_placeholder = ImageDraw.Draw(photo)
        draw_placeholder.text((5, 30), "Error Photo", font=small_font, fill=(255,0,0))

    id_card.paste(photo, photo_position)

    # --- Student details ---
    info_x = 10 # Starting X coordinate for text
    y = rect_y2 + 15 # Starting Y coordinate below the banner and photo

    # Use .get() with a default empty string to prevent KeyError if a field is missing
    draw.text((info_x, y), "NAME: " + student_info.get('name', ''), font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "F_NAME: " + student_info.get('fname', ''), font=default_font, fill=text_color); y += 25
    # Mask roll number for privacy/security example (replace 'x' with actual logic if needed)
    draw.text((info_x, y), "Roll NO: " + 'x' * len(student_info.get('roll_no', '')), font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "BRANCH: " + student_info.get('branch', ''), font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "SESSION: " + student_info.get('session', ''), font=default_font, fill=text_color); y += 25

    # Blood group and DOB on the same line
    draw.text((info_x, y), "BLOOD GROUP: ", font=default_font, fill=text_color)
    blood_w, _ = get_text_size(default_font, "BLOOD GROUP: ")
    draw.text((info_x + blood_w, y), student_info.get('blood_group', ''), font=default_font, fill=(255, 0, 0)) # Red for blood group
    draw.text((info_x + blood_w + 50, y), "DOB: " + student_info.get('dob', ''), font=default_font, fill=text_color); y += 25

    # Address
    # This might need word wrapping for long addresses in a real app
    draw.text((info_x, y), "Add.: " + student_info.get('address', ''), font=default_font, fill=text_color)

    return id_card

# --- Flask Routes ---
@app.route('/')
def home():
    """Renders the main form page."""
    return render_template('index.html') # <--- This line looks for templates/index.html

@app.route('/generate', methods=['POST'])
def generate_id_card_web():
    """
    Handles the form submission, generates the ID card, and returns it as an image.
    """
    # Extract student info from the form
    student_info = {
        'name': request.form.get('name', ''),
        'fname': request.form.get('fname', ''),
        'roll_no': request.form.get('roll_no', ''),
        'branch': request.form.get('branch', ''),
        'session': request.form.get('session', ''),
        'blood_group': request.form.get('blood_group', ''),
        'dob': request.form.get('dob', ''),
        'address': request.form.get('address', '')
    }

    # Get the uploaded photo file
    photo = request.files.get('photo')
    photo_data = None
    if photo and photo.filename != '':
        # Use photo.stream to get a file-like object directly
        photo_data = photo.stream

    # Generate the ID card image
    id_card_img = generate_college_id_card(student_info, photo_data)

    # Save the PIL Image to an in-memory BytesIO object
    img_io = BytesIO()
    # Save as JPEG for web efficiency, adjust quality (0-100) as needed
    id_card_img.save(img_io, 'JPEG', quality=85)
    img_io.seek(0) # Rewind the stream to the beginning

    # Send the image back to the browser
    return send_file(img_io, mimetype='image/jpeg', as_attachment=False, download_name='id_card.jpg')

# --- Run the Flask app ---
if __name__ == '__main__':
    # Run in debug mode for development (reloads on code changes, shows errors)
    # Set debug=False for production!
    app.run(debug=True)