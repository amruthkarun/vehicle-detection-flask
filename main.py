from flask import Flask, render_template, Response, redirect,url_for,request,jsonify
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from OpenVINODetect import VideoCamera
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index_form.html')

def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/input')
def input():
	database = 'data/healthcare'
	key = request.args.get('key',0, type=str)
	print (key)
	output = "what"
	return jsonify(result=output)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
