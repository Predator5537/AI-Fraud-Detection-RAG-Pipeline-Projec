import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, 'fraud_rf.joblib')

def _generate_synthetic(n=2000, random_state=42):
    # Very simple synthetic dataset for demo purposes
    rng = np.random.RandomState(random_state)
    amt = rng.exponential(scale=200, size=n)
    oldbal = rng.normal(loc=1000, scale=300, size=n)
    newbal = oldbal - amt
    # Label: high amount and abnormal balance change => fraud
    labels = ((amt > 800) & (newbal < 0)).astype(int)
    X = np.vstack([amt, oldbal, newbal]).T
    return X, labels

def train_and_save_model():
    X, y = _generate_synthetic()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    clf = RandomForestClassifier(n_estimators=50, random_state=0)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))
    joblib.dump(clf, MODEL_PATH)
    print('Model saved to', MODEL_PATH)
    return MODEL_PATH

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError('Model not found. Run train_and_save_model() first.')
    return joblib.load(MODEL_PATH)

def predict(transaction_dict):
    model = load_model()
    amt = float(transaction_dict.get('amount', 0.0))
    old = float(transaction_dict.get('oldbalanceOrg', 0.0))
    new = float(transaction_dict.get('newbalanceOrig', old-amt))
    X = [[amt, old, new]]
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0].tolist() if hasattr(model, 'predict_proba') else None
    return {'label': int(pred), 'probability': proba}