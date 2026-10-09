"""
Data preprocessing and augmentation pipeline for the PlantVillage dataset.
Implements Algorithm I from section 3.2.6: resize, normalize, and augment
(rotation, flips, zoom, shifts) to reduce overfitting and improve generalization
to real-world images captured under varying field conditions.

Expected directory layout (after you download PlantVillage and run split_dataset,
or point directly at a pre-split copy):

    dataset/
      train/<class_name>/*.jpg   (70%)
      val/<class_name>/*.jpg     (15%)
      test/<class_name>/*.jpg    (15%)
"""

import os
import shutil
import random

from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224, 224)
BATCH_SIZE = 32


def get_data_generators(train_dir, val_dir, test_dir=None,
                         img_size=IMG_SIZE, batch_size=BATCH_SIZE):
    """
    Builds Keras ImageDataGenerators for train/val/(test).

    Train generator applies augmentation only; validation/test generators only
    rescale, so evaluation reflects true unseen-data performance.
    """
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        brightness_range=(0.8, 1.2),
        fill_mode="nearest",
    )
    eval_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        train_dir, target_size=img_size, batch_size=batch_size,
        class_mode="categorical", shuffle=True,
    )
    val_gen = eval_datagen.flow_from_directory(
        val_dir, target_size=img_size, batch_size=batch_size,
        class_mode="categorical", shuffle=False,
    )
    test_gen = None
    if test_dir:
        test_gen = eval_datagen.flow_from_directory(
            test_dir, target_size=img_size, batch_size=batch_size,
            class_mode="categorical", shuffle=False,
        )
    return train_gen, val_gen, test_gen


def split_dataset(source_dir, output_dir, train_ratio=0.70, val_ratio=0.15,
                   test_ratio=0.15, seed=42):
    """
    Stratified 70/15/15 split (section 3.2.1) of a flat PlantVillage-style
    directory (one subfolder per class) into train/val/test subfolders.
    Copies files rather than moving, so the original dataset stays intact.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6
    random.seed(seed)

    class_names = sorted(
        d for d in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, d))
    )

    for split in ("train", "val", "test"):
        for cls in class_names:
            os.makedirs(os.path.join(output_dir, split, cls), exist_ok=True)

    for cls in class_names:
        cls_dir = os.path.join(source_dir, cls)
        images = [f for f in os.listdir(cls_dir)
                  if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        random.shuffle(images)

        n_train = int(len(images) * train_ratio)
        n_val = int(len(images) * val_ratio)

        splits = {
            "train": images[:n_train],
            "val": images[n_train:n_train + n_val],
            "test": images[n_train + n_val:],
        }
        for split, files in splits.items():
            for fname in files:
                shutil.copy2(
                    os.path.join(cls_dir, fname),
                    os.path.join(output_dir, split, cls, fname),
                )
        print(f"{cls}: {len(images)} images -> "
              f"train={len(splits['train'])}, val={len(splits['val'])}, "
              f"test={len(splits['test'])}")

    print(f"\nDataset split complete. Output written to: {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split PlantVillage dataset")
    parser.add_argument("--source", required=True, help="Raw PlantVillage folder")
    parser.add_argument("--output", required=True, help="Output dataset folder")
    args = parser.parse_args()
    split_dataset(args.source, args.output)
