from flask import Flask, render_template, request
from werkzeug.utils import secure_filename 
import os


app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads') # Constructs path to the folder needed, joins the path using os.path.join
app.config['UPLOAD_FOLDER'] = upload_folder # Sets configuration variable for Upload_folder in flask app 

@app.route('/') # For home route
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST']) # For uploading files
def upload_file():
    if request.method == 'POST':
        file = request.files['img'] # Retrieves file from POST request - ORIGINAL FILE
        if file:
            filename = secure_filename(file.filename) # Secures filename to prevent directory attacks   
            file_path = os.path.join(upload_folder, filename) # Construct full file path static/uploads/<image name>
            file.save(file_path) # Saves file to correct filepath
            img = file_path # Constructs URL for image file 
            return render_template('index.html', img=img)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

# host: allows connection from any IP
# port: needs to match whats exposed in dockerfile
