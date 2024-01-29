from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('image_render.html', img=img)
    return render_template('image_render.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

# host: allows connection from any IP
# port: needs to match whats exposed in dockerfile