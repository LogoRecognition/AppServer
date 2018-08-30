from flask import Flask, request
import sys
sys.path.append('/home/CarLogo')
from Faster_RCNN_TF.tools.extract_features import extractor

app = Flask(__name__)
the_extractor = extractor()


@app.route('/detection/<image_name>')
def detect(image_name):
    the_extractor.get_feature(image_name)


app.run(host='127.0.0.1', port=8000)
