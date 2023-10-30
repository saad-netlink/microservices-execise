from flask import Flask, jsonify, request, abort
import requests
import os  # Import the os package
import platform  # Import the platform package
import sys  # Import the sys package

app = Flask(__name__)


AUTH_SERVER_URL = os.environ.get('AUTH_SERVER_URL', 'localhost')  # Replace with your actual auth server URL

# Get the server port from the 'PORT' environment variable, default to 5000 if not set
server_port = int(os.environ.get('PORT', 5000))

def validate_token(auth_key, auth_version):
    # Create the request body
    request_body = {
        "token": auth_key,
        "version": auth_version
    }

    # Send the POST request to the auth server
    response = requests.post(AUTH_SERVER_URL, json=request_body)

    if response.status_code == 200:
        try:
            response_json = response.json()
            return "valid" in response_json and response_json["valid"] is True
        except ValueError:
            return False
    return False

@app.route('/api/sysinfo', methods=['GET'])
def get_system_info():
    # Check if the 'x-auth-key' and 'x-authkey-version' headers are present in the request
    if 'x-auth-key' not in request.headers or 'x-authkey-version' not in request.headers:
        abort(401)  # Unauthorized

    # Extract the values of the 'x-auth-key' and 'x-authkey-version' headers
    auth_key = request.headers['x-auth-key']
    auth_version = request.headers['x-authkey-version']

    # Verify the authentication key and version by making a request to the auth server
    if not validate_token(auth_key, auth_version):
        abort(403)  # Forbidden

    sys_info = {
        "Environment Variables": dict(os.environ),
        "OS Type": platform.system(),
        "OS Version": platform.version(),
        "Python Version": sys.version,
        "Request Details": {
            "Method": request.method,
            "URL": request.url,
            "Headers": dict(request.headers),
            "Query Parameters": request.args.to_dict(),
        }
    }
    return jsonify(sys_info)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=server_port)
