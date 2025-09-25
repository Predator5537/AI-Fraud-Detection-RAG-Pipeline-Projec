# Utilities and security placeholders
import os
from functools import wraps

# Simple API key decorator for demo purposes (DO NOT use in production)
DEMO_API_KEY = os.environ.get('DEMO_API_KEY', 'changeme')

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request, jsonify
        key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not key or key != DEMO_API_KEY:
            return jsonify({'error': 'unauthorized'}), 401
        return func(*args, **kwargs)
    return wrapper

def encrypt_placeholder(plaintext: str) -> str:
    # Placeholder: in production implement AES-GCM or KMS-based envelope encryption
    return f"enc({plaintext[:30]}...)"

def decrypt_placeholder(ciphertext: str) -> str:
    return ciphertext