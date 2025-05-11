from lime.lime_text import LimeTextExplainer
from .model import ensemble_model, tfidf, preprocess_text

# Inisialisasi LIME
explainer = LimeTextExplainer(class_names=["Valid", "Hoax"])

# Fungsi untuk Menjelaskan Prediksi
def explain_prediction(text):
    preprocessed_text = preprocess_text(text)
    tfidf_text = tfidf.transform([preprocessed_text])

    exp = explainer.explain_instance(
        preprocessed_text, 
        lambda x: ensemble_model.predict_proba(tfidf.transform(x)), 
        num_features=10
    )
    
    return exp