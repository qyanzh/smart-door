import face_recognition
from flask import Flask, jsonify, request, redirect, make_response
import json
import time
import datetime
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):

    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    encoding = face_recognition.face_encodings(img)

    if len(encoding) > 0:
        fileName = "faceId-" + str(int(round(time.time()*1000))) + ".jpg"
        file_stream.seek(0)
        file_stream.save("/photos/" + fileName)
        data = {'fileName': fileName, 'vector': encoding[0].tolist()}
        res = make_response(jsonify(data))
        res.headers['Access-Control-Allow-Origin'] = '*'
    else:
        res = 'no faces detected'
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
