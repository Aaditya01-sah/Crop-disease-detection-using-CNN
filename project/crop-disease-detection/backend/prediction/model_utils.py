"""
Model loading + inference utilities for the /api/predict/ endpoint.

Implements Algorithm III from section 3.2.6 (Disease Prediction / Inference):
preprocess the uploaded image with OpenCV to match the model's expected input,
run a forward pass through the trained CNN, and return the top predicted class
with its confidence score.

The model is loaded once per process (module-level singleton) rather than on
every request, since loading a Keras model from disk is expensive.
"""

import json
import os
import sys

import cv2
import numpy as np
from django.conf import settings

# Make ml_model/ importable so we can reuse class_names.py without duplicating it.
ML_MODEL_DIR = os.path.join(settings.BASE_DIR.parent, "ml_model")
if ML_MODEL_DIR not in sys.path:
    sys.path.insert(0, ML_MODEL_DIR)

try:
    from class_names import CLASS_NAMES  # noqa: E402
except ImportError:
    CLASS_NAMES = None

IMG_SIZE = (224, 224)

_model = None
_idx_to_class = None


def _resolve_model_path():
    """
    Picks whichever trained model is present, preferring the fine-tuned
    MobileNetV2 model (typically the stronger of the two per section 4.1)
    over the custom CNN.
    """
    candidates = [
        os.path.join(settings.MODEL_DIR, "mobilenetv2_final.keras"),
        os.path.join(settings.MODEL_DIR, "mobilenetv2_phase2_finetune_best.keras"),
        os.path.join(settings.MODEL_DIR, "custom_cnn_final.keras"),
        os.path.join(settings.MODEL_DIR, "custom_cnn_best.keras"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _load_class_mapping():
    """
    Loads the index->class_name mapping saved during training
    (class_indices.json), falling back to the canonical CLASS_NAMES list if
    that file isn't present yet (e.g. before any training run).
    """
    mapping_path = os.path.join(settings.MODEL_DIR, "class_indices.json")
    if os.path.exists(mapping_path):
        with open(mapping_path) as f:
            class_to_idx = json.load(f)
        return {v: k for k, v in class_to_idx.items()}
    if CLASS_NAMES:
        return {i: name for i, name in enumerate(CLASS_NAMES)}
    return {}


def get_model():
    """Lazily loads and caches the trained Keras model."""
    global _model, _idx_to_class
    if _model is not None:
        return _model

    import tensorflow as tf  # imported lazily so Django can boot without TF installed

    model_path = _resolve_model_path()
    if model_path is None:
        raise FileNotFoundError(
            "No trained model found in "
            f"{settings.MODEL_DIR}. Train a model first with "
            "ml_model/train_custom_cnn.py or ml_model/train_transfer_learning.py, "
            "or place a .keras file at that path."
        )
    _model = tf.keras.models.load_model(model_path)
    _idx_to_class = _load_class_mapping()
    return _model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    OpenCV preprocessing pipeline matching section 3.2.3 / fig. 3.3:
    decode -> resize to 224x224 -> convert BGR->RGB -> normalize to [0, 1] ->
    add batch dimension.
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Uploaded file could not be decoded as an image.")

    img = cv2.resize(img, IMG_SIZE, interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_disease(image_bytes: bytes, top_k: int = 3) -> dict:
    """
    Runs the full inference pipeline and returns the top prediction plus the
    top_k class probabilities, for the JSON response described in 3.2.3.
    """
    model = get_model()
    x = preprocess_image(image_bytes)
    probs = model.predict(x, verbose=0)[0]

    top_indices = np.argsort(probs)[::-1][:top_k]
    top_predictions = [
        {
            "class_name": _idx_to_class.get(int(i), f"class_{i}"),
            "confidence": float(probs[i]),
        }
        for i in top_indices
    ]

    best = top_predictions[0]
    return {
        "predicted_class": best["class_name"],
        "confidence": best["confidence"],
        "top_predictions": top_predictions,
    }
