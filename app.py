from flask import Flask, render_template, Response, request
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import os

app = Flask(__name__)

# Initial setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("model/keras_model.h5", "model/labels.txt")
offset = 20
imgSize = 300

# Labels
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'espace', 'del']

detected_char = ""
detect_count = 0
last_char = ""
detected_text = ""

@app.route('/')
def index():
    global detected_char, detect_count, last_char, detected_text
    detected_char = ""
    detect_count = 0
    last_char = ""
    detected_text = ""
    return render_template('index.html')

@app.route('/text_to_sign')
def text_to_sign():
    return render_template('text_to_sign.html')

@app.route('/generate_sign_images', methods=['POST'])
def generate_sign_images():
    text = request.form['text']
    sign_images = []
    for char in text:
        if char.lower() in labels:
            sign_images.append(f"/static/signs/{char.lower()}.jpg")
        elif char == " ":
            sign_images.append(f"/static/signs/espace.jpg")
    return render_template('text_to_sign.html', sign_images=sign_images)
    

def is_number(char):
    return char.isdigit()

def is_alphabet(char):
    return char.isalpha()

def generate_frames():
    global detected_char, detect_count, last_char, detected_text
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                detected_label = labels[index]

                if detected_label == detected_char:
                    detect_count += 1
                else:
                    detected_char = detected_label
                    detect_count = 1

                if detect_count == 3 and detected_char != last_char:
                    if detected_char == 'del':
                        detected_text = detected_text[:-1]
                    elif detected_char == 'espace':
                        detected_text += ' '
                    else:
                        if detected_text and (
                            (is_number(detected_text[-1]) and is_alphabet(detected_char)) or
                            (is_alphabet(detected_text[-1]) and is_number(detected_char))
                        ):
                            pass
                        else:
                            detected_text += detected_char
                    last_char = detected_char
                    detect_count = 0

                cv2.rectangle(img, (x-offset, y-offset-70), (x-offset+400, y-offset+60-50), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, detected_label, (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                cv2.rectangle(img, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_detected_text')
def get_detected_text():
    def generate_text():
        global detected_text
        while True:
            yield f'data: {detected_text}\n\n'
    return Response(generate_text(), mimetype='text/event-stream')

if __name__ == "__main__":
    # Ensure the sign images are in the static/signs folder
    if not os.path.exists('static/signs'):
        os.makedirs('static/signs')
    app.run(debug=True)
