from flask import Flask, render_template, send_from_directory, request
from flask.ext.cors import CORS

import json
import requests

from input_processor import Comparator

app = Flask(__name__, static_url_path='')

comp = Comparator("similar_words_2016.txt")

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/search/', methods=['GET', 'POST'])
def search():
	text = request.values.keys()[0]
	tags = comp.detect_tags(text)
	json_tags = "{\"tags\":" + json.dumps(tags) + "}";
	return json_tags
	
@app.route('/', methods=['GET', 'POST'])
def default():
  return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)