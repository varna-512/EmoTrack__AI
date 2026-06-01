



import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained model
print("Loading model...")
model = load_model("face_emotion_model.h5")
print("Model loaded successfully!")

# Emotion categories
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Load face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
print("\nStarting webcam...")
print("Press 'q' to quit")
print("Press 's' to save a screenshot")
print("-" * 40)

cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam!")
    exit()

while True:
    # Read frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Process each face
    for (x, y, w, h) in faces:
        # Extract face
        face = gray[y:y+h, x:x+w]
        
        # Resize to model input size
        face = cv2.resize(face, (48, 48))
        
        # Prepare for model
        face_array = face / 255.0
        face_array = face_array.reshape(1, 48, 48, 1)
        
        # Predict
        predictions = model.predict(face_array, verbose=0)
        predicted_index = np.argmax(predictions[0])
        predicted_emotion = emotions[predicted_index]
        confidence = np.max(predictions[0]) * 100
        
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Set color based on emotion
        if predicted_emotion in ['angry', 'fearful', 'sad']:
            color = (0, 0, 255)  # Red for negative emotions
        elif predicted_emotion == 'happy':
            color = (0, 255, 255)  # Yellow for happy
        else:
            color = (255, 255, 255)  # White for neutral
        
        # Display emotion
        text = f"{predicted_emotion.upper()} ({confidence:.1f}%)"
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    # Show instructions on screen
    cv2.putText(frame, "Press 'q' to quit | 's' to save", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Display
    cv2.imshow('Live Emotion Detector', frame)
    
    # Handle keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite('screenshot.png', frame)
        print("Screenshot saved as 'screenshot.png'")

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\nWebcam closed. Goodbye!")