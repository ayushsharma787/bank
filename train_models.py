"""
Universal Bank — ML Model Training
Algorithms: Gradient Boosting, XGBoost, LightGBM, Random Forest,
            Decision Tree, Logistic Regression, KNN, SVM, Neural Net (MLP)
"""
import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)
from sklearn.ensemble import (
    GradientBoostingClassifier, RandomForestClassifier,
    AdaBoostClassifier, ExtraTreesClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
try:
    from lightgbm import LGBMClassifier
    LGBM_AVAILABLE = True
except Exception:
    LGBM_AVAILABLE = False
from imblearn.over_sampling import SMOTE
from pathlib import Path

MODELS_DIR = Path(__file__).parent
SCALER_PATH = MODELS_DIR / "scaler.joblib"

# ── ALGORITHM REGISTRY ──────────────────────────────────────────────────────
def get_models():
    models = {
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200, learning_rate=0.1, max_depth=4,
            min_samples_split=10, subsample=0.8, random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=200, learning_rate=0.1, max_depth=4,
            subsample=0.8, colsample_bytree=0.8,
            use_label_encoder=False, eval_metric="logloss", random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=10, min_samples_split=5,
            class_weight="balanced", random_state=42
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=200, max_depth=10, class_weight="balanced", random_state=42
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8, min_samples_split=10,
            class_weight="balanced", random_state=42
        ),
        "AdaBoost": AdaBoostClassifier(
            n_estimators=100, learning_rate=0.5, random_state=42
        ),
        "Logistic Regression": LogisticRegression(
            C=1.0, class_weight="balanced",
            max_iter=1000, random_state=42
        ),
        "KNN": KNeighborsClassifier(n_neighbors=7, weights="distance"),
        "SVM": SVC(
            kernel="rbf", C=1.0, probability=True,
            class_weight="balanced", random_state=42
        ),
        "Neural Network (MLP)": MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation="relu", max_iter=500,
            learning_rate_init=0.001, random_state=42
        ),
    }
    if LGBM_AVAILABLE:
        models["LightGBM"] = LGBMClassifier(
            n_estimators=200, learning_rate=0.05,
            num_leaves=31, class_weight="balanced", random_state=42, verbose=-1
        )
    return models

# ── TRAINING ────────────────────────────────────────────────────────────────
def train_and_evaluate(X, y, use_smote=True):
    """Train all models, return results dict and best estimator."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)
    joblib.dump(scaler, SCALER_PATH)

    # SMOTE on training set to handle class imbalance (9.6% loan rate)
    if use_smote:
        sm = SMOTE(random_state=42)
        X_train_sc, y_train = sm.fit_resample(X_train_sc, y_train)

    models = get_models()
    results = {}
    trained = {}

    for name, clf in models.items():
        clf.fit(X_train_sc, y_train)
        y_pred = clf.predict(X_test_sc)
        y_prob = clf.predict_proba(X_test_sc)[:, 1] if hasattr(clf, "predict_proba") else None

        acc   = round(accuracy_score(y_test, y_pred) * 100, 2)
        prec  = round(precision_score(y_test, y_pred, zero_division=0) * 100, 2)
        rec   = round(recall_score(y_test, y_pred, zero_division=0) * 100, 2)
        f1    = round(f1_score(y_test, y_pred, zero_division=0) * 100, 2)
        auc   = round(roc_auc_score(y_test, y_prob), 4) if y_prob is not None else None
        cm    = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": acc, "precision": prec,
            "recall": rec, "f1": f1, "auc_roc": auc, "confusion_matrix": cm
        }
        trained[name] = clf

    # Persist best model (by AUC)
    best_name = max(results, key=lambda k: results[k]["auc_roc"] or 0)
    joblib.dump(trained[best_name], MODELS_DIR / "best_model.joblib")
    joblib.dump(trained, MODELS_DIR / "all_models.joblib")

    return results, trained, scaler, X_test, y_test, best_name

def load_trained_models():
    path = MODELS_DIR / "all_models.joblib"
    if path.exists():
        return joblib.load(path)
    return None

def load_scaler():
    if SCALER_PATH.exists():
        return joblib.load(SCALER_PATH)
    return None

def predict_single(model, scaler, input_dict: dict) -> dict:
    """Predict for a single customer dict."""
    cols = ["Age","Experience","Income","Family","CCAvg",
            "Education","Mortgage","Securities Account","CD Account","Online","CreditCard"]
    df = pd.DataFrame([input_dict])[cols]
    X_sc = scaler.transform(df)
    pred = model.predict(X_sc)[0]
    prob = model.predict_proba(X_sc)[0][1] if hasattr(model, "predict_proba") else None
    return {"prediction": int(pred), "probability": round(float(prob) * 100, 1) if prob else None}

def get_feature_importance(model, feature_names):
    """Return feature importance as sorted list of (feature, importance)."""
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
    elif hasattr(model, "coef_"):
        imp = np.abs(model.coef_[0])
    else:
        return []
    pairs = sorted(zip(feature_names, imp), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in pairs) or 1
    return [(f, round(v / total * 100, 1)) for f, v in pairs]
