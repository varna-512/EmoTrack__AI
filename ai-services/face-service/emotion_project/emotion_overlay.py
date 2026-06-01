import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time
from collections import deque

# Load your trained model
print("Loading model...")
model = load_model("face_emotion_model.h5")
print("Model loaded!")

# Emotion categories
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Load face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Emotion history
emotion_history = deque(maxlen=100)

# Stress mapping
emotion_stress = {
    'happy': 1,
    'neutral': 2,
    'surprised': 4,
    'fearful': 7,
    'sad': 8,
    'disgusted': 8,
    'angry': 9
}

# Activity suggestions
suggestions = {
    1: ["🌟 Keep up the great mood!"],
    2: ["😊 You're doing well!"],
    3: ["🧘 Take a short breathing break"],
    4: ["🚶 Take a 5-minute walk"],
    5: ["📝 Write down what's bothering you"],
    6: ["🧘 5-minute meditation"],
    7: ["🛑 Take a deep breath"],
    8: ["🏃 Physical activity helps"],
    9: ["💪 Take a break now"],
    10: ["🚨 High stress! Take a break"]
}

def calculate_stress(emotion_counts, total_frames):
    if total_frames == 0:
        return 5
    weighted_stress = 0
    for emotion, count in emotion_counts.items():
        weighted_stress += emotion_stress.get(emotion, 5) * count
    avg_stress = weighted_stress / total_frames
    return round(avg_stress, 1)

def draw_overlay(frame, emotion_counts, total_frames, current_emotion, current_confidence):
    h, w = frame.shape[:2]
    
    # Create a semi-transparent overlay at TOP-RIGHT corner
    overlay_width = 280
    overlay_height = 320
    overlay_x = w - overlay_width - 10  # 10px from right edge
    overlay_y = 10  # 10px from top edge
    
    # Draw semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (overlay_x, overlay_y), 
                  (overlay_x + overlay_width, overlay_y + overlay_height), 
                  (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    
    # Calculate stress
    stress = calculate_stress(emotion_counts, total_frames)
    stress_int = int(stress)
    
    y_offset = overlay_y + 20
    
    # Title
    cv2.putText(frame, "STRESS METER", (overlay_x + 10, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y_offset += 25
    
    # Stress value
    if stress_int > 6:
        color = (0, 0, 255)
    elif stress_int > 3:
        color = (0, 255, 255)
    else:
        color = (0, 255, 0)
    
    cv2.putText(frame, f"{stress_int}/10", (overlay_x + 10, y_offset + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
    
    # Stress bar
    bar_width = overlay_width - 20
    bar_height = 12
    bar_x = overlay_x + 10
    bar_y = y_offset + 35
    fill_width = int((stress_int / 10) * bar_width)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (80, 80, 80), -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), color, -1)
    
    y_offset = bar_y + 25
    
    # Separator line
    cv2.line(frame, (overlay_x + 10, y_offset), (overlay_x + overlay_width - 10, y_offset), (100, 100, 100), 1)
    y_offset += 15
    
    # Emotion breakdown title
    cv2.putText(frame, "EMOTIONS", (overlay_x + 10, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y_offset += 20
    
    # Show top 3 emotions only (to save space)
    if total_frames > 0:
        percentages = [(emotion, (count / total_frames) * 100) for emotion, count in emotion_counts.items()]
        percentages.sort(key=lambda x: x[1], reverse=True)
        
        for i, (emotion, pct) in enumerate(percentages[:3]):
            cv2.putText(frame, f"{emotion[:3].upper()}: {int(pct)}%", (overlay_x + 10, y_offset + i*20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        y_offset += 70
    
    # Current emotion
    cv2.putText(frame, f"CURRENT: {current_emotion.upper()}", (overlay_x + 10, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    y_offset += 25
    
    # Suggestion
    suggestion = suggestions.get(stress_int, suggestions[5])[0]
    cv2.putText(frame, "TIP:", (overlay_x + 10, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 200, 100), 1)
    cv2.putText(frame, suggestion[:25], (overlay_x + 10, y_offset + 18), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
    
    return frame, stress_int

def main():
    print("\n" + "="*50)
    print("EMOTION DASHBOARD - OVERLAY MODE")
    print("="*50)
    print("Dashboard appears at TOP-RIGHT corner")
    print("Press 'q' to quit")
    print("-"*50)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam!")
        return
    
    emotion_counts = {emotion: 0 for emotion in emotions}
    total_frames = 0
    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        current_emotion = "none"
        current_confidence = 0
        
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48, 48))
            face_array = face / 255.0
            face_array = face_array.reshape(1, 48, 48, 1)
            
            predictions = model.predict(face_array, verbose=0)
            predicted_index = np.argmax(predictions[0])
            current_emotion = emotions[predicted_index]
            current_confidence = np.max(predictions[0]) * 100
            
            emotion_counts[current_emotion] += 1
            total_frames += 1
            
            # Draw rectangle around face
            if current_emotion in ['angry', 'fearful', 'sad']:
                color = (0, 0, 255)
            elif current_emotion == 'happy':
                color = (0, 255, 255)
            else:
                color = (0, 255, 0)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, current_emotion.upper(), (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw overlay dashboard
        frame, stress_level = draw_overlay(frame, emotion_counts, total_frames, 
                                            current_emotion, current_confidence)
        
        # Show FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to quit", (10, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow('Emotion Dashboard', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\nDashboard closed!")

if __name__ == "__main__":
    main()