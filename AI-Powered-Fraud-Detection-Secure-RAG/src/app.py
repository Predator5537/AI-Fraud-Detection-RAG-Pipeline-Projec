from flask import Flask, request, jsonify
from .fraud_model import train_and_save_model, predict, load_model
from .rag import SimpleRAG
from .utils import require_api_key, encrypt_placeholder
import os, json

app = Flask(__name__)
rag = SimpleRAG()

@app.route('/train', methods=['POST'])
def train():
    path = train_and_save_model()
    return jsonify({'status': 'trained', 'model_path': path})

@app.route('/ingest', methods=['POST'])
@require_api_key
def ingest():
    payload = request.get_json(force=True)
    docs = payload.get('docs') or []
    rag.ingest(docs)
    return jsonify({'status': 'ingested', 'count': len(docs)})

@app.route('/retrieve', methods=['GET'])
@require_api_key
def retrieve():
    q = request.args.get('q','')
    top_k = int(request.args.get('k', 3))
    results = rag.retrieve(q, top_k=top_k)
    return jsonify({'results': results})

@app.route('/predict', methods=['POST'])
@require_api_key
def predict_endpoint():
    payload = request.get_json(force=True)
    tx = payload.get('transaction') or {}
    res = predict(tx)
    # Example of storing masked/encrypted record (demo only)
    masked = encrypt_placeholder(str(tx))
    return jsonify({'prediction': res, 'masked_record': masked})

# helper functions for demo scripts
def ingest_documents(docs, rag=None):
    if rag is None:
        from .rag import SimpleRAG
        rag = SimpleRAG()
    rag.ingest(docs)
    return rag

def predict_transaction(tx):
    return predict(tx)

if __name__ == '__main__':
    app.run(debug=True)