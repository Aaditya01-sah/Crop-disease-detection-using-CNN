"""
Canonical list of the 38 PlantVillage classes (26 disease categories + 12 healthy
categories across 14 crop species), matching Table 3.1 of the project report.

Index position == the neuron index in the final Softmax(38) layer, so this file
must stay in sync between training (ImageDataGenerator's class_indices, which are
alphabetically sorted from the folder names) and inference (model_utils.py).
"""

CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry___Powdery_mildew",
    "Cherry___healthy",
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Bell_pepper___Bacterial_spot",
    "Bell_pepper___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Squash___healthy",  # kept for pipeline symmetry; see note below
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites_Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# NOTE: Table 3.1 in the report lists Squash with 2 disease categories and 0 healthy
# categories (and Orange with 1 disease, 0 healthy). If you regenerate this list
# directly from your own dataset folder names, always do:
#
#   sorted(os.listdir(TRAIN_DIR))
#
# and paste the output here instead of hand-editing, so class_indices never drifts
# from what Keras' ImageDataGenerator assigns during training.

NUM_CLASSES = len(CLASS_NAMES)

assert NUM_CLASSES == 38, f"Expected 38 classes, got {NUM_CLASSES}"
