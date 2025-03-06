from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from typing import Dict, Any, Optional
import logging
import sys
import json
import os
from quantum.bernstein_vazirani import run_bernstein_vazirani
from quantum.exceptions import QuantumCircuitError, InvalidInputError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('html', 'index.html')

@app.route('/doc/<path:filename>')
def serve_doc(filename):
    """Serve documentation files"""
    return send_from_directory('html/doc', filename)

@app.route('/pictures/<path:filename>')
def serve_pictures(filename):
    """Serve picture files"""
    return send_from_directory('pictures', filename)

@app.route('/run_bernstein_vazirani', methods=['POST'])
def handle_algorithm() -> Dict[str, Any]:
    """
    Handle Bernstein-Vazirani algorithm execution requests.
    
    Returns:
        Dict[str, Any]: JSON response containing the result or error
    
    Raises:
        400: If input is invalid
        500: If there's an internal server error
    """
    try:
        logger.info("Received request to run Bernstein-Vazirani algorithm")
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received")
            
        secret = data.get('secret', '')
        logger.info(f"Input secret (left to right): {secret}")
        
        circuit_image_path: Optional[str] = None
        
        # Validate input
        if not secret or not all(bit in '01' for bit in secret) or len(secret) > 7:
            return jsonify({
                'success': False,
                'error': 'Invalid input. Please provide a binary string of up to 7 bits.'
            }), 400
        
        # Run algorithm
        algorithm_result = run_bernstein_vazirani(secret)

        logger.info(f"Algorithm completed. Secret recovered: {algorithm_result['result']}")
        return jsonify({
            'success': True,
            'result': algorithm_result['result'],
            'secret': algorithm_result['secret'],
            'circuit_image': algorithm_result['circuit_image']
        })
        
    except InvalidInputError as e:
        logger.warning(f"Invalid input: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except QuantumCircuitError as e:
        logger.error(f"Quantum circuit error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('pictures/bernstein_vazirani', exist_ok=True)
    
    # Set static folder path
    app.static_folder = 'html'
    app.static_url_path = ''
    
    logger.info("Starting Flask server...")
    app.run(port=5000, debug=True)