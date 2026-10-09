"""
CNN architectures for Crop Disease Detection, matching section 3.1.2 of the report
(fig. 3.2: Input 224x224x3 -> [Conv2D+ReLU -> MaxPool2D] x3 (32,64,128 filters)
-> Flatten -> Dense(256, ReLU) -> Softmax(38)), plus a MobileNetV2 transfer-learning
variant.
"""

import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

from class_names import NUM_CLASSES

INPUT_SHAPE = (224, 224, 3)


def build_custom_cnn(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES, dropout=0.3):
    """
    Custom sequential CNN exactly as described in fig. 3.2:
      Conv2D(32, 3x3, ReLU) -> MaxPool2D
      Conv2D(64, 3x3, ReLU) -> MaxPool2D
      Conv2D(128, 3x3, ReLU) -> MaxPool2D
      Flatten -> Dense(256, ReLU) -> Dropout -> Softmax(num_classes)
    """
    model = models.Sequential(name="crop_disease_custom_cnn")
    model.add(layers.Input(shape=input_shape))

    # Block 1
    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    # Block 2
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    # Block 3
    model.add(layers.Conv2D(128, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    # Classification head
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation="relu",
                            kernel_regularizer=regularizers.l2(1e-4)))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(num_classes, activation="softmax"))

    return model


def build_mobilenetv2_model(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES,
                             freeze_base=True, dropout=0.3):
    """
    Transfer-learning model: MobileNetV2 pretrained on ImageNet as the feature
    extractor, with a new classification head for the 38 PlantVillage classes.

    Two-phase training strategy (see 3.1.2 / 3.2.2):
      Phase 1 - base_model.trainable = False, train only the new head.
      Phase 2 - unfreeze the top N layers of the base and fine-tune at a lower LR.
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = not freeze_base

    inputs = layers.Input(shape=input_shape)
    # MobileNetV2 expects inputs scaled to [-1, 1]
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training=False if freeze_base else None)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="crop_disease_mobilenetv2")
    return model, base_model


def unfreeze_top_layers(base_model, num_layers=30):
    """Unfreeze the top `num_layers` of the MobileNetV2 base for fine-tuning."""
    base_model.trainable = True
    for layer in base_model.layers[:-num_layers]:
        layer.trainable = False
    return base_model


if __name__ == "__main__":
    cnn = build_custom_cnn()
    cnn.summary()

    mobilenet_model, _ = build_mobilenetv2_model()
    mobilenet_model.summary()
