import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# ---------------------------------------
# LOAD FEATURES
# ---------------------------------------

X = np.load("features/X_features.npy")
y = np.load("features/y_labels.npy")

print("Features Loaded:")
print("X Shape:", X.shape)
print("y Shape:", y.shape)

# ---------------------------------------
# NORMALIZE FEATURES
# ---------------------------------------

scaler = StandardScaler()

X = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, "models/scaler.pkl")

print("\nFeature scaling complete!")

# ---------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTrain Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

# ---------------------------------------
# ONE HOT ENCODING
# ---------------------------------------

num_classes = len(np.unique(y))

y_train_cat = to_categorical(y_train, num_classes)
y_test_cat = to_categorical(y_test, num_classes)

# ---------------------------------------
# CLASS WEIGHTS
# ---------------------------------------

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y),
    y=y
)

class_weights = dict(enumerate(class_weights))

print("\nClass Weights:")
print(class_weights)

# ---------------------------------------
# BUILD MODEL
# ---------------------------------------

model = Sequential()

model.add(Dense(256, activation='relu', input_shape=(X.shape[1],)))
model.add(BatchNormalization())
model.add(Dropout(0.3))

model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))

model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(num_classes, activation='softmax'))

# ---------------------------------------
# COMPILE MODEL
# ---------------------------------------

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ---------------------------------------
# EARLY STOPPING
# ---------------------------------------

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

# ---------------------------------------
# TRAIN MODEL
# ---------------------------------------

history = model.fit(
    X_train,
    y_train_cat,
    validation_data=(X_test, y_test_cat),
    epochs=100,
    batch_size=32,
    class_weight=class_weights,
    callbacks=[early_stop]
)

# ---------------------------------------
# EVALUATION
# ---------------------------------------

loss, accuracy = model.evaluate(X_test, y_test_cat)

print("\nTest Accuracy:", accuracy)

# ---------------------------------------
# PREDICTIONS
# ---------------------------------------

y_pred_probs = model.predict(X_test)

y_pred = np.argmax(y_pred_probs, axis=1)

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))

# ---------------------------------------
# SAVE MODEL
# ---------------------------------------

model.save("models/emotion_voice_model.h5")

print("\nModel saved successfully!")