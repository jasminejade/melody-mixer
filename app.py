from flask import Flask, request, render_template, jsonify, send_file
import json
import flask # flask==2.1.3
import os
from main import *
from flask_cors import CORS

os.environ["FLASK_APP"]="app.py"
app = Flask(__name__, template_folder="./frontend")
app.static_folder = 'static'
CORS(app)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/gen")
def gen():
    return render_template('gen.html')

@app.route("/next")
def next():
    return render_template('next.html')

# this starts the neural net, parameter will be the filename later
@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    parameter = data['parameter']
    parameter = parameter.split('.')[0]
    print(parameter)
    inputName = 'humanlifeleadsheet'
    run_main(inputName) # can you make run_main return the first one
    gen_result = ''
    return jsonify({'gen_result', gen_result})


@app.route('/input', methods=['POST'])
def input_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file
    # You can save the file to a specific directory or process it as needed

    # Access file properties
    file_name = file.filename
    file_size = len(file.read())
    file.seek(0)

    return jsonify({'file_name': file_name, 'file_size': file_size})

@app.route('/result', methods=['GET'])
def result():
    return send_file(GEN_RESULT, as_attachment=True)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)