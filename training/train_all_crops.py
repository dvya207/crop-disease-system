import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# -------------------------
# CONFIG
# -------------------------
CROPS = ["cotton", "maize", "wheat", "rice", "sugarcane"]

BASE_DATASET_DIR = "dataset"
MODEL_DIR = "models"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------
# DATA GENERATOR
# -------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# -------------------------
# TRAIN EACH CROP
# -------------------------
for crop in CROPS:
    print(f"\n==============================")
    print(f"🚀 Training model for: {crop.upper()}")
    print(f"==============================")

    DATASET_DIR = os.path.join(BASE_DATASET_DIR, crop)
    MODEL_PATH = os.path.join(MODEL_DIR, f"{crop}_model.h5")
    CLASS_PATH = os.path.join(MODEL_DIR, f"{crop}_classes.json")

    train_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training"
    )

    val_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation"
    )

    # -------------------------
    # MODEL
    # -------------------------
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )

    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    output = Dense(train_data.num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # -------------------------
    # TRAIN
    # -------------------------
    model.fit(
        train_data,
        validation_data=val_data,
        epochs=EPOCHS
    )

    # -------------------------
    # SAVE MODEL & CLASSES
    # -------------------------
    model.save(MODEL_PATH)

    class_names = list(train_data.class_indices.keys())
    with open(CLASS_PATH, "w") as f:
        json.dump(class_names, f)

    print(f"✅ Saved model: {MODEL_PATH}")
    print(f"✅ Saved classes: {CLASS_PATH}")

print("\n🎉 ALL CROP MODELS TRAINED SUCCESSFULLY")
