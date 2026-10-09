"""
Human-readable display names and short descriptions for each of the 38
PlantVillage classes. Used by the /api/predict/ endpoint to enrich the raw
class label with a farmer-friendly explanation, as described in section 3.2.4
("a result panel displaying the predicted disease name, confidence score, and
a brief description of the disease").
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "display_name": "Apple - Apple Scab",
        "is_healthy": False,
        "description": "A fungal disease causing dark, scabby lesions on leaves and "
                        "fruit. Spreads in cool, wet spring weather and can defoliate "
                        "trees if untreated.",
        "recommendation": "Remove fallen leaves, prune for airflow, and apply a "
                           "protectant fungicide from bud break through early summer.",
    },
    "Apple___Black_rot": {
        "display_name": "Apple - Black Rot",
        "is_healthy": False,
        "description": "Fungal infection causing purple leaf spots and rotting fruit "
                        "with concentric rings; often enters through wounds or dead wood.",
        "recommendation": "Prune out cankers and mummified fruit, and apply fungicide "
                           "sprays during the growing season.",
    },
    "Apple___Cedar_apple_rust": {
        "display_name": "Apple - Cedar Apple Rust",
        "is_healthy": False,
        "description": "A fungus requiring both apple and cedar/juniper hosts, causing "
                        "bright orange-yellow spots on leaves.",
        "recommendation": "Remove nearby cedar hosts where feasible and apply "
                           "fungicide starting at pink bud stage.",
    },
    "Apple___healthy": {
        "display_name": "Apple - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring and good orchard sanitation.",
    },
    "Blueberry___healthy": {
        "display_name": "Blueberry - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring and balanced fertilization.",
    },
    "Cherry___Powdery_mildew": {
        "display_name": "Cherry - Powdery Mildew",
        "is_healthy": False,
        "description": "Fungal disease producing a white powdery coating on leaves, "
                        "reducing photosynthesis and fruit quality.",
        "recommendation": "Improve air circulation through pruning and apply sulfur "
                           "or a labeled fungicide at first sign of infection.",
    },
    "Cherry___healthy": {
        "display_name": "Cherry - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot": {
        "display_name": "Corn - Gray Leaf Spot",
        "is_healthy": False,
        "description": "Fungal disease causing rectangular gray-brown lesions that "
                        "can merge and blight large areas of the leaf.",
        "recommendation": "Rotate crops, use resistant hybrids, and apply fungicide "
                           "if disease pressure is high.",
    },
    "Corn___Common_rust": {
        "display_name": "Corn - Common Rust",
        "is_healthy": False,
        "description": "Fungal disease producing small, reddish-brown pustules on "
                        "both leaf surfaces.",
        "recommendation": "Plant resistant hybrids; fungicide is rarely needed except "
                           "in severe outbreaks.",
    },
    "Corn___Northern_Leaf_Blight": {
        "display_name": "Corn - Northern Leaf Blight",
        "is_healthy": False,
        "description": "Fungal disease causing long, cigar-shaped gray-green lesions "
                        "on leaves.",
        "recommendation": "Rotate crops, till residue, and use resistant hybrids or "
                           "fungicide under heavy pressure.",
    },
    "Corn___healthy": {
        "display_name": "Corn - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Grape___Black_rot": {
        "display_name": "Grape - Black Rot",
        "is_healthy": False,
        "description": "Fungal disease causing circular brown leaf spots and shriveled, "
                        "mummified fruit.",
        "recommendation": "Remove mummified berries and infected canes; apply "
                           "fungicide from bud break through veraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "display_name": "Grape - Esca (Black Measles)",
        "is_healthy": False,
        "description": "A complex fungal trunk disease causing tiger-stripe leaf "
                        "discoloration and berry spotting.",
        "recommendation": "Prune out and destroy infected wood; avoid pruning wounds "
                           "during wet weather.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "display_name": "Grape - Leaf Blight (Isariopsis Leaf Spot)",
        "is_healthy": False,
        "description": "Fungal disease producing irregular brown spots that can cause "
                        "premature leaf drop.",
        "recommendation": "Improve canopy airflow and apply fungicide during humid "
                           "periods.",
    },
    "Grape___healthy": {
        "display_name": "Grape - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "display_name": "Orange - Citrus Greening (HLB)",
        "is_healthy": False,
        "description": "A serious bacterial disease spread by psyllid insects, causing "
                        "blotchy mottled leaves and misshapen, bitter fruit. No cure "
                        "currently exists.",
        "recommendation": "Remove and destroy infected trees, control psyllid vectors, "
                           "and consult local agricultural extension services promptly.",
    },
    "Peach___Bacterial_spot": {
        "display_name": "Peach - Bacterial Spot",
        "is_healthy": False,
        "description": "Bacterial disease causing small, dark, water-soaked spots on "
                        "leaves and fruit.",
        "recommendation": "Use resistant varieties, avoid overhead irrigation, and "
                           "apply copper-based bactericides during dormancy.",
    },
    "Peach___healthy": {
        "display_name": "Peach - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Bell_pepper___Bacterial_spot": {
        "display_name": "Bell Pepper - Bacterial Spot",
        "is_healthy": False,
        "description": "Bacterial disease causing small, dark, greasy-looking spots on "
                        "leaves and fruit.",
        "recommendation": "Use certified disease-free seed, avoid working in wet "
                           "fields, and apply copper-based sprays preventively.",
    },
    "Bell_pepper___healthy": {
        "display_name": "Bell Pepper - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Potato___Early_blight": {
        "display_name": "Potato - Early Blight",
        "is_healthy": False,
        "description": "Fungal disease producing dark, target-like concentric-ring "
                        "spots on lower, older leaves.",
        "recommendation": "Rotate crops, remove infected debris, and apply fungicide "
                           "at first symptom appearance.",
    },
    "Potato___Late_blight": {
        "display_name": "Potato - Late Blight",
        "is_healthy": False,
        "description": "A fast-spreading oomycete disease (the cause of the historic "
                        "Irish famine) producing water-soaked lesions that rapidly "
                        "blacken and rot foliage and tubers.",
        "recommendation": "Act immediately: remove infected plants, avoid overhead "
                           "watering, and apply an appropriate fungicide without delay.",
    },
    "Potato___healthy": {
        "display_name": "Potato - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Raspberry___healthy": {
        "display_name": "Raspberry - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Soybean___healthy": {
        "display_name": "Soybean - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Squash___Powdery_mildew": {
        "display_name": "Squash - Powdery Mildew",
        "is_healthy": False,
        "description": "Fungal disease producing a white, powdery coating on leaf "
                        "surfaces, weakening the plant over time.",
        "recommendation": "Space plants for airflow, water at the base, and apply "
                           "sulfur or a labeled fungicide early.",
    },
    "Squash___healthy": {
        "display_name": "Squash - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Strawberry___Leaf_scorch": {
        "display_name": "Strawberry - Leaf Scorch",
        "is_healthy": False,
        "description": "Fungal disease causing irregular purple blotches that can "
                        "merge into scorched-looking, dried leaf tissue.",
        "recommendation": "Remove infected leaves after harvest and apply fungicide "
                           "in wet seasons.",
    },
    "Strawberry___healthy": {
        "display_name": "Strawberry - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
    "Tomato___Bacterial_spot": {
        "display_name": "Tomato - Bacterial Spot",
        "is_healthy": False,
        "description": "Bacterial disease causing small, dark, water-soaked spots on "
                        "leaves and fruit that can merge under humid conditions.",
        "recommendation": "Use disease-free seed/transplants and apply copper-based "
                           "bactericide preventively.",
    },
    "Tomato___Early_blight": {
        "display_name": "Tomato - Early Blight",
        "is_healthy": False,
        "description": "Fungal disease producing dark, target-like concentric-ring "
                        "spots, typically starting on lower leaves.",
        "recommendation": "Remove lower infected leaves, mulch to prevent soil splash, "
                           "and apply fungicide as needed.",
    },
    "Tomato___Late_blight": {
        "display_name": "Tomato - Late Blight",
        "is_healthy": False,
        "description": "Fast-spreading disease causing large, water-soaked lesions "
                        "that can destroy a crop within days in cool, wet weather.",
        "recommendation": "Remove and destroy infected plants immediately and apply "
                           "fungicide to protect remaining plants.",
    },
    "Tomato___Leaf_Mold": {
        "display_name": "Tomato - Leaf Mold",
        "is_healthy": False,
        "description": "Fungal disease favored by high humidity, causing pale spots "
                        "on top of leaves and olive-green mold underneath.",
        "recommendation": "Improve ventilation, reduce humidity, and apply fungicide "
                           "if conditions remain favorable for spread.",
    },
    "Tomato___Septoria_leaf_spot": {
        "display_name": "Tomato - Septoria Leaf Spot",
        "is_healthy": False,
        "description": "Fungal disease causing many small, circular spots with dark "
                        "borders and gray centers, mainly on lower leaves.",
        "recommendation": "Remove infected leaves, avoid overhead watering, and apply "
                           "fungicide at first sign.",
    },
    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "display_name": "Tomato - Two-Spotted Spider Mite",
        "is_healthy": False,
        "description": "Pest damage causing fine yellow stippling and, in heavy "
                        "infestations, webbing on the underside of leaves.",
        "recommendation": "Increase humidity, introduce predatory mites, or apply "
                           "a miticide/insecticidal soap.",
    },
    "Tomato___Target_Spot": {
        "display_name": "Tomato - Target Spot",
        "is_healthy": False,
        "description": "Fungal disease producing brown lesions with concentric rings, "
                        "resembling a target.",
        "recommendation": "Improve airflow, remove infected debris, and apply "
                           "fungicide under humid conditions.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "display_name": "Tomato - Yellow Leaf Curl Virus",
        "is_healthy": False,
        "description": "A whitefly-transmitted viral disease causing upward leaf "
                        "curling, yellowing, and stunted growth.",
        "recommendation": "Control whitefly populations, remove infected plants, and "
                           "use virus-resistant varieties where available.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "display_name": "Tomato - Mosaic Virus",
        "is_healthy": False,
        "description": "Viral disease causing mottled light and dark green patterns "
                        "and leaf distortion.",
        "recommendation": "Remove infected plants, disinfect tools, and avoid "
                           "handling plants while smoking (tobacco can carry the virus).",
    },
    "Tomato___healthy": {
        "display_name": "Tomato - Healthy",
        "is_healthy": True,
        "description": "No visible signs of disease detected on this leaf.",
        "recommendation": "Continue routine monitoring.",
    },
}


def get_disease_info(class_name: str) -> dict:
    """Returns display info for a class, falling back to a generic entry."""
    return DISEASE_INFO.get(class_name, {
        "display_name": class_name.replace("___", " - ").replace("_", " "),
        "is_healthy": "healthy" in class_name.lower(),
        "description": "No additional information available for this class.",
        "recommendation": "Consult a local agricultural extension office for guidance.",
    })
