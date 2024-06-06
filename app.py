from flask import Flask, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
import cv2
import os
from flask import send_from_directory

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
    new_file_path = ""
    
    # Handling different operations
    if operation == "cgray":
        img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        new_filename = f"{filename.rsplit('.', 1)[0]}.png"
        new_file_path = f"static/{new_filename}"
        cv2.imwrite(new_file_path, img_processed)
    elif operation in {"cwebp", "cjpg", "cpng", "cjpeg"}:
        new_extension = operation[1:]
        new_filename = f"{filename.rsplit('.', 1)[0]}.{new_extension}"
        new_file_path = f"static/{new_filename}"
        cv2.imwrite(new_file_path, img)
    else:
        flash('Invalid operation')
        return None
    return new_file_path

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
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file_path = process_image(filename, operation)
            if new_file_path:
                flash("Your image has been processed.")
                return render_template("index.html", new_file_url=new_file_path)
    
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
