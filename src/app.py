import os

from flask import Flask, Response, render_template

from main import QR

BASE_DIR = os.path.dirname(__file__)
ROOT = os.path.dirname(BASE_DIR)
TEMPLATES_PATH = os.path.join(ROOT, 'templates')

app = Flask(__name__, template_folder=TEMPLATES_PATH)

qr = QR()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(qr.qr_scanner(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/qr_text')
def qr_text():
    return qr.qr_str


if __name__ == '__main__':
    app.run(debug=True)