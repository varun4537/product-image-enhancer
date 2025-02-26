from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import re

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.config['UPLOAD_FOLDER'] = 'static/images'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to sanitize filenames
def sanitize_filename(filename):
    # Replace spaces and special characters with underscores
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

@app.route('/')
def index():
    return render_template('index.html')

# Serve static files (CSS, JS) from the frontend folder
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../frontend/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../frontend/js', filename)

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Get attributes from the form
    attribute1 = request.form.get('attribute1', 'N/A')
    attribute2 = request.form.get('attribute2', 'N/A')
    attribute3 = request.form.get('attribute3', 'N/A')

    # Sanitize the filename
    sanitized_filename = sanitize_filename(file.filename)

    # Save the uploaded image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename)
    file.save(image_path)

    # Debug: Print the uploaded image path
    print(f"Uploaded image saved to: {image_path}")

    # Open the image and overlay attributes
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Get image dimensions
        width, height = image.size

        # Load a custom font with a larger size
        font_path = "SansSerifCollection.ttf"  # Replace with the path to your .ttf font file
        font_size = int(height * 0.05)  # Font size as 5% of image height
        font = ImageFont.truetype(font_path, font_size)

        # Define relative positions (as percentages of image dimensions)
        attributes = [
            {"text": attribute1, "position": (0.05 * width, 0.25 * height)},  # 5% from left, 25% from top
            {"text": attribute2, "position": (0.05 * width, 0.50 * height)},  # 5% from left, 50% from top
            {"text": attribute3, "position": (0.05 * width, 0.75 * height)},  # 5% from left, 75% from top
        ]

        # Add text overlay with a faint grey background
        for attr in attributes:
            # Calculate text size using textbbox
            text_bbox = draw.textbbox(attr["position"], attr["text"], font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Draw a semi-transparent grey background rectangle
            background_color = (252, 252, 252, 191)  # Grey with 75% opacity
            background_rectangle = Image.new('RGBA', (int(text_width * 1.2), int(text_height * 1.2)), background_color)
            image.paste(background_rectangle, (int(attr["position"][0] - 10), int(attr["position"][1] - 10)), background_rectangle)

            # Draw the text
            draw.text(attr["position"], attr["text"], fill="black", font=font)

        # Save the enhanced image
        enhanced_image_name = f"enhanced_{sanitized_filename}"
        enhanced_image_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_image_name)
        image.save(enhanced_image_path)

        # Debug: Print the enhanced image path
        print(f"Enhanced image saved to: {enhanced_image_path}")

        # Return the URL of the enhanced image
        enhanced_image_url = f"/static/images/{enhanced_image_name}"
        return jsonify({"enhanced_image_url": enhanced_image_url})

    except Exception as e:
        # Debug: Print any errors that occur during image processing
        print(f"Error processing image: {e}")
        return jsonify({"error": "Failed to process image"}), 500

if __name__ == '__main__':
    app.run(debug=True)