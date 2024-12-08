from flask import Flask, render_template, send_file, request, redirect, url_for
import os
import mimetypes

app = Flask(__name__)

# Directory where videos are stored
VIDEO_FOLDER = 'videos'
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER

@app.route('/')
def index():
    # List available videos
    videos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv'))]
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        
        # Save the uploaded file
        file.save(os.path.join(app.config['VIDEO_FOLDER'], file.filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/video/<filename>')
def stream_video(filename):
    file_path = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(file_path):
        return "Video not found", 404

    mime_type, _ = mimetypes.guess_type(file_path)
    return send_file(file_path, mimetype=mime_type)

# Custom 404 page handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    os.makedirs(VIDEO_FOLDER, exist_ok=True)
    app.run(debug=True)
