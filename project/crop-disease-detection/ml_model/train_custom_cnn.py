"""
Trains the custom CNN (section 3.1.2) on the PlantVillage dataset.

Implements Algorithm II (section 3.2.6): mini-batch SGD via the Adam optimizer,
categorical cross-entropy loss, early stopping on validation loss, LR reduction
on plateau, and checkpointing of the best-performing weights (section 3.2.2).

Usage:
    python train_custom_cnn.py --data_dir ./dataset --epochs 50
"""

import argparse
import json
import os

import tensorflow as tf
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, CSVLogger,
)
from tensorflow.keras.optimizers import Adam

from data_preprocessing import get_data_generators
from model_architecture import build_custom_cnn

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "saved_models")


def train(data_dir, epochs=50, batch_size=32, learning_rate=0.001, patience=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")
    test_dir = os.path.join(data_dir, "test")

    train_gen, val_gen, test_gen = get_data_generators(
        train_dir, val_dir, test_dir, batch_size=batch_size
    )

    # Persist class_indices so inference always maps softmax index -> class name
    # using the exact mapping Keras assigned during training.
    with open(os.path.join(OUTPUT_DIR, "class_indices.json"), "w") as f:
        json.dump(train_gen.class_indices, f, indent=2)

    model = build_custom_cnn(num_classes=train_gen.num_classes)
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"),
                 tf.keras.metrics.Recall(name="recall")],
    )
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=patience,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2,
                           min_lr=1e-6, verbose=1),
        ModelCheckpoint(
            os.path.join(OUTPUT_DIR, "custom_cnn_best.keras"),
            monitor="val_accuracy", save_best_only=True, verbose=1,
        ),
        CSVLogger(os.path.join(OUTPUT_DIR, "custom_cnn_training_log.csv")),
    ]

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
    )

    model.save(os.path.join(OUTPUT_DIR, "custom_cnn_final.keras"))

    if test_gen is not None:
        results = model.evaluate(test_gen, return_dict=True)
        print("\nTest set performance:", results)
        with open(os.path.join(OUTPUT_DIR, "custom_cnn_test_results.json"), "w") as f:
            json.dump(results, f, indent=2)

    return model, history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the custom CNN")
    parser.add_argument("--data_dir", required=True,
                         help="Path to dataset/ with train/val/test subfolders")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--patience", type=int, default=5)
    args = parser.parse_args()

    train(args.data_dir, args.epochs, args.batch_size, args.lr, args.patience)
