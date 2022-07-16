from re import template
from urllib import response
from regex import F
# import base64
from requests import request
from flask import Flask, render_template,request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from PIL import Image
from io import BytesIO
from base64 import b64decode
from object_detection import captionize
from object_detection import keywordize
from object_detection import init

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})

init()

app.debug = False


@app.route('/', methods=['POST'])
def index():
    # print(request.args["image"])
    # data = json.loads(request.data)
    # print(request.data.decode())
    # print(type( json.loads(request.data.decode()) ))
    bimage = json.loads(request.data.decode())['image'];
    image = b64decode(bimage)
    im = Image.open(BytesIO(b64decode(bimage.split(',')[0])))
    rgb_im = im.convert('RGB')
    rgb_im.save("temp.jpg")
    f = open("temp.jpg","wb")
    f.write(image)
    caps = captionize()
    # print(caps[0])
    # print(caps[1])
    # return "<h1>Hello World!</h1>"
    return {'captions':caps[1], 'authors':caps[0]}

@app.route('/bykw', methods=['POST'])
def bykw():
    keywords = json.loads(request.data.decode())['keywords']
    # print(keywords)
    caps = keywordize(keywords)
    # print(keywords)
    return {'captions':caps[1], 'authors':caps[0]}
    
    


if __name__ == '__main__':
    app.run()