"""
Evaluates a saved model on the held-out test set using accuracy, precision,
recall, and F1-score (section 4.2 Validation Strategy), and writes a
per-class classification report + confusion matrix.
"""

import argparse
import json
import os

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from data_preprocessing import get_data_generators
from class_names import CLASS_NAMES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "saved_models")


def evaluate(model_path, data_dir):
    model = tf.keras.models.load_model(model_path)

    _, _, test_gen = get_data_generators(
        train_dir=os.path.join(data_dir, "train"),
        val_dir=os.path.join(data_dir, "val"),
        test_dir=os.path.join(data_dir, "test"),
    )

    y_true = test_gen.classes
    y_pred_probs = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)

    idx_to_class = {v: k for k, v in test_gen.class_indices.items()}
    target_names = [idx_to_class[i] for i in range(len(idx_to_class))]

    report = classification_report(y_true, y_pred, target_names=target_names,
                                    output_dict=True, zero_division=0)
    print(classification_report(y_true, y_pred, target_names=target_names,
                                 zero_division=0))

    cm = confusion_matrix(y_true, y_pred)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "classification_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    np.save(os.path.join(OUTPUT_DIR, "confusion_matrix.npy"), cm)

    print(f"\nOverall accuracy:  {report['accuracy']:.4f}")
    print(f"Weighted precision: {report['weighted avg']['precision']:.4f}")
    print(f"Weighted recall:    {report['weighted avg']['recall']:.4f}")
    print(f"Weighted F1-score:  {report['weighted avg']['f1-score']:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a trained model")
    parser.add_argument("--model", required=True, help="Path to .keras model file")
    parser.add_argument("--data_dir", required=True)
    args = parser.parse_args()

    evaluate(args.model, args.data_dir)
