import sys
import os
import io
from flask import Flask, request, send_file, jsonify

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymeo_lite import obfuscate

app = Flask(__name__)

@app.route('/obfuscate', methods=['POST', 'OPTIONS'])
def obfuscate_api():
    if request.method == 'OPTIONS':
        return '', 200
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    code = file.read().decode('utf-8', errors='ignore')
    mode = int(request.form.get('mode', 2))
    more_obf = request.form.get('more_obf', 'false').lower() == 'true'
    antidebug = request.form.get('antidebug', 'true').lower() == 'true'
    anticrack = request.form.get('anticrack', 'true').lower() == 'true'
    username = request.form.get('username', 'Vercel_User')
    
    try:
        obfuscated_code = obfuscate(code, mode, more_obf, antidebug, anticrack, username)
        return send_file(io.BytesIO(obfuscated_code.encode('utf-8')), mimetype='text/x-python', as_attachment=True, download_name=f'obfuscated_{file.filename}')
    except Exception as e:
        return jsonify({"error": str(e)}), 500