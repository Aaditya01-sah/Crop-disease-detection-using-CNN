"""
Two-phase transfer learning with MobileNetV2 (section 3.1.2):

  Phase 1: base model frozen, train only the new classification head.
            This preserves the ImageNet-learned low/mid-level features and
            lets the head adapt quickly on the relatively small PlantVillage
            dataset.
  Phase 2: unfreeze the top layers of the base and fine-tune end-to-end at a
            much lower learning rate, to adapt higher-level features to leaf
            imagery specifically.

Usage:
    python train_transfer_learning.py --data_dir ./dataset --epochs_head 15 --epochs_finetune 20
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
from model_architecture import build_mobilenetv2_model, unfreeze_top_layers

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "saved_models")


def train(data_dir, epochs_head=15, epochs_finetune=20, batch_size=32,
          head_lr=1e-3, finetune_lr=1e-5, patience=5, unfreeze_layers=30):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")
    test_dir = os.path.join(data_dir, "test")

    train_gen, val_gen, test_gen = get_data_generators(
        train_dir, val_dir, test_dir, batch_size=batch_size
    )

    with open(os.path.join(OUTPUT_DIR, "class_indices.json"), "w") as f:
        json.dump(train_gen.class_indices, f, indent=2)

    model, base_model = build_mobilenetv2_model(
        num_classes=train_gen.num_classes, freeze_base=True
    )

    common_callbacks = lambda tag: [
        EarlyStopping(monitor="val_loss", patience=patience,
                       restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2,
                           min_lr=1e-7, verbose=1),
        ModelCheckpoint(
            os.path.join(OUTPUT_DIR, f"mobilenetv2_{tag}_best.keras"),
            monitor="val_accuracy", save_best_only=True, verbose=1,
        ),
        CSVLogger(os.path.join(OUTPUT_DIR, f"mobilenetv2_{tag}_log.csv")),
    ]

    # ---------- Phase 1: train the head only ----------
    model.compile(
        optimizer=Adam(learning_rate=head_lr),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    print("\n=== Phase 1: training classification head (base frozen) ===")
    model.fit(
        train_gen, validation_data=val_gen, epochs=epochs_head,
        callbacks=common_callbacks("phase1_head"),
    )

    # ---------- Phase 2: fine-tune top layers of the base ----------
    unfreeze_top_layers(base_model, num_layers=unfreeze_layers)
    model.compile(
        optimizer=Adam(learning_rate=finetune_lr),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    print("\n=== Phase 2: fine-tuning top layers of MobileNetV2 ===")
    model.fit(
        train_gen, validation_data=val_gen, epochs=epochs_finetune,
        callbacks=common_callbacks("phase2_finetune"),
    )

    model.save(os.path.join(OUTPUT_DIR, "mobilenetv2_final.keras"))

    if test_gen is not None:
        results = model.evaluate(test_gen, return_dict=True)
        print("\nTest set performance:", results)
        with open(os.path.join(OUTPUT_DIR, "mobilenetv2_test_results.json"), "w") as f:
            json.dump(results, f, indent=2)

    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train MobileNetV2 transfer model")
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--epochs_head", type=int, default=15)
    parser.add_argument("--epochs_finetune", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--patience", type=int, default=5)
    args = parser.parse_args()

    train(args.data_dir, args.epochs_head, args.epochs_finetune,
          args.batch_size, patience=args.patience)
