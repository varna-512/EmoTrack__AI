







import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load your trained model
model = load_model("face_emotion_model.h5")

# Emotion categories
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Path to test images
test_path = "emotion-detection-fer/test"

print("Testing the model...")
print("=" * 50)

# Test one image from each emotion category
for emotion in emotions:
    emotion_folder = os.path.join(test_path, emotion)
    
    if os.path.exists(emotion_folder):
        images = os.listdir(emotion_folder)
        if len(images) > 0:
            img_path = os.path.join(emotion_folder, images[0])
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (48, 48))
            
            img_array = img / 255.0
            img_array = img_array.reshape(1, 48, 48, 1)
            
            predictions = model.predict(img_array, verbose=0)
            predicted_index = np.argmax(predictions[0])
            predicted_emotion = emotions[predicted_index]
            confidence = np.max(predictions[0]) * 100
            
            print(f"Actual: {emotion:12} → Predicted: {predicted_emotion:12} (Confidence: {confidence:.1f}%)")
        else:
            print(f"No images found for {emotion}")
    else:
        print(f"Folder not found: {emotion}")

print("=" * 50)
print("✅ Testing complete!")