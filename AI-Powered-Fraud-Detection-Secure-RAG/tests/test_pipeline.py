from src.rag import SimpleRAG
from src.fraud_model import train_and_save_model, predict

def test_rag_and_model_train():
    # train model (ensures model file is generated)
    train_and_save_model()
    rag = SimpleRAG()
    docs = [{'id':'1','text':'fraud pattern: high amount and overseas IP'}, {'id':'2','text':'regular purchase'}]
    rag.ingest(docs)
    res = rag.retrieve('high amount', top_k=1)
    assert len(res) == 1
    sample = {'amount': 1000.0, 'oldbalanceOrg': 50.0, 'newbalanceOrig': -950.0}
    p = predict(sample)
    assert 'label' in p