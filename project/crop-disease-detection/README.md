# Crop Disease Detection Using Convolutional Neural Networks

Full implementation matching the proposal defense report (ENCT-354, Advanced
College of Engineering and Management): a CNN-based leaf disease classifier
(38 classes — 26 diseased, 12 healthy) served through a Django REST API, with
a React.js frontend for uploading a leaf photo and viewing the diagnosis.

```
crop-disease-detection/
├── backend/                    Django REST API
│   ├── crop_disease_backend/   Project settings, urls, wsgi/asgi
│   ├── prediction/             The /api/predict/ app (views, preprocessing, inference)
│   ├── ml_model/                (see below — training code lives at repo root of ml pipeline)
│   ├── manage.py
│   └── requirements.txt
├── ml_model/                   Model architecture + training/evaluation scripts
│   ├── class_names.py
│   ├── model_architecture.py   Custom CNN + MobileNetV2 transfer-learning model
│   ├── data_preprocessing.py   Augmentation pipeline + 70/15/15 dataset split
│   ├── train_custom_cnn.py
│   ├── train_transfer_learning.py
│   ├── evaluate.py
│   └── saved_models/           (created after training — .keras weights land here)
└── frontend/                   React.js single-page app
    ├── src/components/         ImageUploader, ResultCard, Header, Footer
    ├── src/api/predictApi.js   Axios client for the backend
    └── public/
```

## How the pieces map to the report

| Report section | Implementation |
|---|---|
| 3.1.1 System Architecture | React SPA → Django REST API → CNN model / PlantVillage dataset |
| 3.1.2 CNN Model Architecture | `ml_model/model_architecture.py` — `build_custom_cnn()` (3× Conv2D+MaxPool, 32/64/128 filters, Dense 256, Softmax 38) and `build_mobilenetv2_model()` |
| 3.2.1 Dataset | `ml_model/data_preprocessing.py::split_dataset()` — stratified 70/15/15 split |
| 3.2.2 Model Training | `train_custom_cnn.py` / `train_transfer_learning.py` — Adam (lr 0.001), categorical cross-entropy, early stopping (patience 5), ReduceLROnPlateau, checkpointing, batch size 32 |
| 3.2.3 Backend API | `backend/prediction/views.py` — `POST /api/predict/`, OpenCV preprocessing in `model_utils.py`, CORS configured in `settings.py` |
| 3.2.4 Frontend Application | `frontend/src` — drag-and-drop upload, submit button, result panel with disease name / confidence / description |
| 3.2.5 System Workflow | Upload → HTTP POST → preprocess+infer → render result (see `App.js`) |
| 3.2.6 Algorithms I–III | Augmentation pipeline, training loop, inference pipeline, respectively |
| 4.2 Validation Strategy | `ml_model/evaluate.py` — accuracy, precision, recall, F1 on held-out test set |

## 1. Get the dataset

Download the **PlantVillage** dataset (54,305 images, 38 classes) — for
example via the Kaggle mirror `emmarex/plantdisease`, or the original
Hughes & Salathé repository. Extract it so you have one folder per class,
then split it:

```bash
cd ml_model
pip install -r ../backend/requirements.txt --break-system-packages   # or use a venv
python data_preprocessing.py --source /path/to/raw_plantvillage --output ./dataset
```

This produces `ml_model/dataset/{train,val,test}/<class_name>/*.jpg` in a
70/15/15 stratified split.

> **Important:** after splitting, run `sorted(os.listdir("dataset/train"))` and
> compare it against `ml_model/class_names.py`. If your download uses
> slightly different folder names, update `class_names.py` to match — Keras
> assigns class indices alphabetically from the folder names it sees, and
> `class_indices.json` (written automatically during training) is the source
> of truth the backend actually loads at inference time.

## 2. Train the model

Custom CNN (fast baseline):

```bash
python train_custom_cnn.py --data_dir ./dataset --epochs 50
```

MobileNetV2 transfer learning (recommended — higher accuracy, per section 4.1):

```bash
python train_transfer_learning.py --data_dir ./dataset --epochs_head 15 --epochs_finetune 20
```

Both scripts write to `ml_model/saved_models/`: the best/final `.keras`
weights, `class_indices.json`, a training log CSV, and test-set metrics.
`model_utils.py` in the backend automatically prefers the MobileNetV2 model
if both are present.

Evaluate any saved model on the held-out test set (accuracy/precision/recall/F1):

```bash
python evaluate.py --model ./saved_models/mobilenetv2_final.keras --data_dir ./dataset
```

## 3. Run the backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # adjust if needed
python manage.py migrate
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/api/`:
- `POST /api/predict/` — multipart field `image` → JSON diagnosis
- `GET /api/health/` — liveness check

If no trained model is found in `ml_model/saved_models/`, `/api/predict/`
returns `503` with a clear message rather than crashing — train a model
first (step 2).

## 4. Run the frontend

```bash
cd frontend
npm install
cp .env.example .env        # adjust REACT_APP_API_BASE_URL if needed
npm start
```

Opens at `http://localhost:3000`. Drop or select a leaf photo, click
**Diagnose this leaf**, and the result panel shows the predicted species/condition,
confidence score, a short description, and a recommended action.

## Notes on this implementation vs. the report draft

- The report's Objectives (1.4) and Significance of Study (1.5) sections were
  identical bullet lists in the source document — likely a copy-paste leftover
  in the proposal. Worth writing distinct content for 1.5 (e.g. framing it
  around impact for smallholder farmers, food security, and reducing reliance
  on scarce agronomists) before your final defense.
- Table 3.1's species/category counts don't all reconcile with a standard
  38-class PlantVillage split (e.g. it lists 2 Squash disease categories and 0
  healthy, and Orange with 1 disease/0 healthy, which would undercount to 37
  classes against the stated "26 diseased + 12 healthy = 38"). `class_names.py`
  ships with the standard 38-class PlantVillage taxonomy so the code is
  internally consistent — re-derive it from your actual downloaded folder
  names as noted in step 1, and reconcile Table 3.1 to match for the defense.
- No trained weights are bundled here (the dataset/training step needs to run
  in an environment with internet access and, ideally, a GPU); everything
  else — architecture, training scripts, API, and UI — is complete and wired
  together end-to-end.
