from math import floor
import random
from flask import Flask, request, jsonify, send_from_directory
import os
import hashlib
from werkzeug.utils import secure_filename


def hash_to_1_12(input_string):
    # Create a hash object using SHA-256
    hash_object = hashlib.sha256(input_string.encode())
    # Get the hexadecimal digest of the hash
    hash_hex = hash_object.hexdigest()
    # Convert the hexadecimal digest to an integer
    hash_int = int(hash_hex, 16)
    # Map the integer to the range 1 to 12
    result = (hash_int % 12) + 1
    return result

def getRandomFileName(path : str):
    # Generate a random filename

    name = ""
    with open(path, 'r') as file:
        for _ in range(floor(random.randint(1,10)/9) + 1):
            lines = file.readlines()
            if lines:
                name += random.choice(lines).strip() + "_"
            else:
                return None
            file.seek(0)
        lines = file.readlines()
        if lines:
            name += random.choice(lines).strip() + ".pdf"
        else:
            return None
    return name

fileSet = set()
for _ in range(4000):
    fileSet.add(getRandomFileName("ZionDict.txt"))
app = Flask(__name__)
UPLOAD_DIR = './uploads'
USER_CREDENTIALS = {
    'badguyrulz4ever': hashlib.sha256('aDmInAdMiN'.encode()).hexdigest()
}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads

print(len(fileSet))

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/files', methods=['GET'])
def list_files():
    return jsonify(list(fileSet))

@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_DIR, str(hash_to_1_12(filename)) + ".jpg")
    except FileNotFoundError:
        return 'File not found.', 404

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)
        return 'File uploaded successfully.', 200
    else:
        return 'Invalid upload request. Only PDF files are allowed.', 400

@app.route('/delete', methods=['POST'])
def delete_file():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    filename = request.form.get('filename', '')
    if USER_CREDENTIALS.get(username) == hashlib.sha256(password.encode()).hexdigest():
        if filename:
            if filename in fileSet:
                fileSet.remove(filename)
                return 'File deleted successfully.', 200
            else:
                return 'File not found.', 404
        else:
            return 'Filename is required.', 400
    else:
        return 'Access denied.', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

