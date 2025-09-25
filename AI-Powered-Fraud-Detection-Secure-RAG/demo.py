from src.fraud_model import train_and_save_model
from src.rag import SimpleRAG
from src.app import ingest_documents, predict_transaction

def main():
    # Train model and prepare RAG index
    train_and_save_model()
    rag = SimpleRAG()
    docs = [
        {"id":"doc1", "text":"Customer reported a stolen card and multiple rapid transactions."},
        {"id":"doc2", "text":"Known fraud pattern: unusual IP + high-value purchase."},
        {"id":"doc3", "text":"Chargeback history and account takeover indicators."}
    ]
    ingest_documents(docs, rag=rag)
    q = "multiple transactions from new IP and high amount"
    results = rag.retrieve(q, top_k=2)
    print('RAG retrieval results:', results)
    # Example prediction (random synthetic sample)
    sample = {"amount": 950.0, "oldbalanceOrg": 1000.0, "newbalanceOrig": 50.0}
    print('Prediction example:', predict_transaction(sample))

if __name__ == '__main__':
    main()