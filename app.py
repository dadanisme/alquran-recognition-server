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

@app.route('/upload_blob', methods=['POST', 'GET'])
def upload_blob():
  filename = request.args.get('filename')
  blob = request.data
  with open('./audio/' + filename + '.wav', 'ab') as f:
    f.write(blob)
  
  import os
  file_size = os.path.getsize('./audio/' + filename + '.wav')
  return {
    'status': 'success',
    'filename': filename + '.wav',
    'filesize': file_size
  }
    
  path = './audio/' + blob.filename.replace(' ', '_')


  return {
    'status': 'success',
    'result': path
  }


@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    print('getting response...')
    filename = request.args.get('filename')
    sample_rate_hertz = int(request.args.get('sample_rate_hertz'))
    file_path ='./audio/' + filename
    result = transcribe_file(file_path, sample_rate_hertz)

    response = {
      'status': 'success',
      'result': result
    }
    return response

@app.route('/predict', methods=['GET', 'POST'])
def predict_ayat():
  print('predicting ayat...')
  text = request.args.get('text')
  result = search_in_ayat(text)
  response = {
    'status': 'success',
    'result': result
  }
  return response