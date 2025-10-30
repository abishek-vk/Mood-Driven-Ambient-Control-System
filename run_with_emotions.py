#!/usr/bin/env python
"""
Facial Recognition with Emotion Detection
Uses OpenCV for face detection and TensorFlow for emotion classification
"""

import cv2
import numpy as np
import sys
import os
import warnings

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

def load_emotion_model():
    """Load the pre-trained emotion model"""
    try:
        print("Loading TensorFlow and emotion model...")
        import tensorflow as tf
        from tensorflow import keras
        
        # Try to load existing model
        model_path = os.path.join('models', 'emotion_model.h5')
        if os.path.exists(model_path):
            print(f"Loading emotion model from {model_path}...")
            model = keras.models.load_model(model_path, compile=False)
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            return model
        else:
            print("⚠️  Emotion model not found at models/emotion_model.h5")
            print("Will use face detection only.")
            return None
    except Exception as e:
        print(f"Error loading emotion model: {e}")
        print("Will use face detection only.")
        return None

def preprocess_face(face_img):
    """Preprocess face image for emotion detection"""
    try:
        # Resize to 48x48 (standard for emotion models)
        face_resized = cv2.resize(face_img, (48, 48))
        
        # Convert to grayscale if needed
        if len(face_resized.shape) == 3:
            face_resized = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        face_resized = face_resized.astype('float32') / 255.0
        
        # Add batch dimension and channel dimension
        face_resized = np.expand_dims(face_resized, axis=0)
        face_resized = np.expand_dims(face_resized, axis=-1)
        
        return face_resized
    except Exception as e:
        print(f"Error preprocessing face: {e}")
        return None

def predict_emotion(model, face_img):
    """Predict emotion for a face image"""
    if model is None:
        return None, None
    
    try:
        processed = preprocess_face(face_img)
        if processed is None:
            return None, None
        
        prediction = model.predict(processed, verbose=0)
        emotion_idx = np.argmax(prediction[0])
        confidence = prediction[0][emotion_idx]
        
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        emotion = emotions[emotion_idx]
        
        return emotion, confidence
    except Exception as e:
        print(f"Error predicting emotion: {e}")
        return None, None

def get_emotion_color(emotion):
    """Get color for emotion label"""
    colors = {
        'angry': (0, 0, 255),      # Red
        'disgust': (0, 165, 255),  # Orange
        'fear': (255, 0, 0),       # Blue
        'happy': (0, 255, 0),      # Green
        'sad': (255, 0, 255),      # Magenta
        'surprise': (0, 255, 255), # Yellow
        'neutral': (128, 128, 128) # Gray
    }
    return colors.get(emotion, (255, 255, 255))

def main():
    print("=" * 70)
    print("Facial Recognition with Emotion Detection System")
    print("=" * 70)
    print("\nInitializing...")
    
    # Load face cascade
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    print("✓ OpenCV Haar Cascade face detector loaded")
    
    # Load emotion model
    emotion_model = load_emotion_model()
    if emotion_model:
        print("✓ Emotion detection model loaded")
    else:
        print("⚠️  Emotion detection unavailable - face detection only")
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Error: Could not open camera")
        print("System will use a test image instead.")
        
        # Create a test image
        img = np.ones((480, 640, 3), dtype=np.uint8) * 200
        cv2.putText(img, "No Camera Available", (150, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        cv2.putText(img, "Press 'q' to exit", (150, 280), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow('Facial Recognition System', img)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        return
    
    # Configure camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    print("✓ Camera initialized successfully")
    
    print("\nStarting live detection...")
    print("Press 'q' to quit\n")
    
    frame_count = 0
    emotion_frame_skip = 3  # Detect emotion every 3 frames for speed
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        frame_count += 1
        frame = cv2.flip(frame, 1)  # Mirror effect
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(40, 40),
            maxSize=(500, 500)
        )
        
        # Draw rectangles around faces and detect emotions
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = frame[y:y+h, x:x+w]
            
            # Predict emotion (every few frames for performance)
            emotion = None
            confidence = None
            
            if emotion_model and frame_count % emotion_frame_skip == 0:
                emotion, confidence = predict_emotion(emotion_model, face_roi)
            
            # Draw bounding box
            color = (0, 255, 0)
            if emotion:
                color = get_emotion_color(emotion)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw emotion label
            if emotion and confidence:
                label = f"{emotion}: {confidence:.2f}"
                cv2.putText(frame, label, (x, y-30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            else:
                cv2.putText(frame, "Face", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Display frame count and face count
        cv2.putText(frame, f"Faces: {len(faces)} | Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if emotion_model:
            cv2.putText(frame, "With Emotion Detection", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Facial Recognition with Emotion Detection', frame)
        
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\nSystem shut down gracefully.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
