from setup import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

if __name__ == '__main__':
  app.run('127.0.0.1', 5600, debug=True, ssl_context=('cert.pem', 'key.pem'))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
  file = request.files['file']
  file.save('./audio/' + file.filename.replace(' ', '_'))
  path = './audio/' + file.filename.replace(' ', '_')

  return {
    'status': 'success',
    'filename': file.filename.replace(' ', '_')
  }

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
  print('getting response...')
  filename = request.args.get('filename')
  file_path = './audio/' + filename
  print('converting to flac...')
  flac_file = convert_to_flac(file_path)
  print('getting annotation...')
  result = transcribe_file(flac_file['filename'], flac_file['sample_rate_hertz'])
  print(result)
  return {
    'status': 'success',
    'result': result
  }