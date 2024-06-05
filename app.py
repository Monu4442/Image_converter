from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import svgwrite
import os

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(img_path)
    if img is None:
        flash('Error reading the image file')
        return None

    new_filename = ""
    if operation == "cgray":
        img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        new_filename = f"static/{filename}"
        cv2.imwrite(new_filename, img_processed)
    elif operation == "cwebp":
        new_filename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(new_filename, img)
    elif operation == "cjpg":
        new_filename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(new_filename, img)
    elif operation == "cpng":
        new_filename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(new_filename, img)
    elif operation == "cjpeg":
        new_filename = f"static/{filename.split('.')[0]}.jpeg"
        cv2.imwrite(new_filename, img)
    elif operation == "cheic":
        new_filename = f"static/{filename.split('.')[0]}.heic"
        cv2.imwrite(new_filename, img)
    else:
        flash('Invalid operation')
        return None
    return new_filename



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = process_image(filename, operation)
            if new:
                flash(f"Your image has been processed and it is available to <a href='/{new}' target='_blank' style='color: blue;'>Download</a>")
            return render_template("index.html")

    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
