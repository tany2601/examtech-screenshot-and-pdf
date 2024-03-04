import os
from flask import Flask, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename
from screenshot_tool import ScreenshotTool  # Import the ScreenshotTool class

app = Flask(__name__)

# Path to save uploaded PDFs and screenshots
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'pdf' not in request.files:
            return 'No file part'
        
        pdf = request.files['pdf']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if pdf.filename == '':
            return 'No selected file'
        
        if pdf and allowed_file(pdf.filename):
            filename = secure_filename(pdf.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf.save(pdf_path)
            return render_template('index.html', pdf_path=url_for('static', filename=pdf_path))
        else:
            return 'Invalid file format'

    return render_template('index.html', pdf_path=None)

@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    screenshot_file = request.files['screenshot']
    if screenshot_file:
        screenshot = Image.open(screenshot_file)
        screenshot_path = save_screenshot(screenshot)
        return screenshot_path

@app.route('/view_pdf')
def view_pdf():
    pdf_path = request.args.get('pdf_path')
    return render_template('pdf_viewer.html', pdf_path=pdf_path)

# New route to trigger the screenshot tool
@app.route('/run_screenshot_tool', methods=['POST'])
def run_screenshot_tool():
    screenshot_tool = ScreenshotTool()
    screenshot_tool.take_screenshot()
    return "Screenshot taken and saved."

if __name__ == '__main__':
    app.run(debug=True)
