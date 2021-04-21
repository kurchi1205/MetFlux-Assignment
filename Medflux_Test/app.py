from flask import Flask, flash, request, redirect, url_for, render_template ,send_from_directory,Response
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2 
import camera
from camera import VideoCamera
app = Flask(__name__,template_folder="Template")
 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
 

     
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    img=cv2.imread(destination)
    face_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))  
    print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
  
    # Detect faces  
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)  
  
    # Draw rectangle around the faces  
    for (x, y, w, h) in faces:  
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  
    
    cv2.imwrite(destination,img)
    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)


@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/video')
def index():
    # rendering webpage
    return render_template('video.html')

def gen(Camera):
    while True:
        #get camera frame
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(camera.VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True)