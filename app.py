from flask import Flask, request, jsonify
import requests
import json
import os
from functools import wraps

app = Flask(__name__)

# Configuration
API_BASE_URL = "https://www.smcinsurance.com/central/centralcall"
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'origin': 'https://www.smcinsurance.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.smcinsurance.com/',
    'accept-language': 'en-GB,en;q=0.9,hi;q=0.8',
    'priority': 'u=1, i'
}

# Simple rate limiting
from time import time
request_history = {}

def rate_limit(max_requests=10, window=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time()
            
            if client_ip not in request_history:
                request_history[client_ip] = []
            
            # Clean old requests
            request_history[client_ip] = [
                req_time for req_time in request_history[client_ip] 
                if current_time - req_time < window
            ]
            
            if len(request_history[client_ip]) >= max_requests:
                return jsonify({
                    "success": False,
                    "error": "Rate limit exceeded. Max 10 requests per minute."
                }), 429
            
            request_history[client_ip].append(current_time)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def clean_vehicle_number(vehicle_no):
    """Remove spaces and convert to uppercase"""
    return vehicle_no.replace(" ", "").replace("-", "").upper()

def fetch_vehicle_details(vehicle_no):
    """Fetch vehicle details from SMC Insurance API"""
    url = f"{API_BASE_URL}/CallReqWithHeader"
    
    payload = {
        "URL": "GetVaahanDetailsByVehicleNo",
        "Props": [vehicle_no],
        "Token": ""
    }
    
    try:
        response = requests.post(
            url, 
            data=json.dumps(payload), 
            headers=DEFAULT_HEADERS,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def home():
    return jsonify({
        "message": "Vehicle Lookup API",
        "version": "1.0",
        "endpoints": {
            "/lookup/<vehicle_number>": "GET - Fetch vehicle details",
            "/lookup": "POST - Fetch vehicle details (JSON body)"
        },
        "example": "/lookup/MH14ML9572"
    })

@app.route('/lookup/<vehicle_number>', methods=['GET'])
@rate_limit(max_requests=10, window=60)
def lookup_vehicle(vehicle_number):
    """
    Lookup vehicle details by vehicle number
    Example: /lookup/MH14ML9572 or /lookup/MH14%20ML%209572
    """
    clean_number = clean_vehicle_number(vehicle_number)
    
    # Basic validation
    if len(clean_number) < 5 or len(clean_number) > 15:
        return jsonify({
            "success": False,
            "error": "Invalid vehicle number format"
        }), 400
    
    result = fetch_vehicle_details(clean_number)
    return jsonify(result)

@app.route('/lookup', methods=['POST'])
@rate_limit(max_requests=10, window=60)
def lookup_vehicle_post():
    """
    Lookup vehicle details via POST
    Body: {"vehicle_number": "MH14ML9572"}
    """
    data = request.get_json()
    
    if not data or 'vehicle_number' not in data:
        return jsonify({
            "success": False,
            "error": "vehicle_number is required in JSON body"
        }), 400
    
    vehicle_number = data['vehicle_number']
    clean_number = clean_vehicle_number(vehicle_number)
    
    if len(clean_number) < 5 or len(clean_number) > 15:
        return jsonify({
            "success": False,
            "error": "Invalid vehicle number format"
        }), 400
    
    result = fetch_vehicle_details(clean_number)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "vehicle-lookup-api"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
