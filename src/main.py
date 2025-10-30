import cv2
import numpy as np
import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

print("Loading detectors...")
from face_detector_advanced import AdvancedFaceDetector
from emotion_detector import AdvancedEmotionDetector

def main():
    print("\n" + "="*60)
    print("FACIAL RECOGNITION WITH EMOTION DETECTION")
    print("="*60)
    
    print("\n[Loading] Face Detector...")
    face_detector = AdvancedFaceDetector()
    
    print("[Loading] Emotion Detector...")
    emotion_detector = AdvancedEmotionDetector()
    
    print("[Loading] Camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("\n✅ All systems ready!")
    print("Press 'q' to quit\n")
    print("="*60 + "\n")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        frame = cv2.flip(frame, 1)
        
        # Detect faces
        faces = face_detector.detect_faces(frame)
        
        # Process each face and get emotion
        for face in faces:
            x, y, w, h = face['bbox']
            
            # Validate coordinates
            if w < 30 or h < 30 or x < 0 or y < 0:
                continue
            
            x = max(0, x)
            y = max(0, y)
            w = min(w, frame.shape[1] - x)
            h = min(h, frame.shape[0] - y)
            
            # Extract face region
            face_img = frame[y:y+h, x:x+w]
            
            if face_img is not None and face_img.size > 0:
                # Get emotion prediction
                emotion, confidence = emotion_detector.predict_emotion(face_img)
                
                # Draw face box
                face_detector.draw_faces(frame, [face])
                
                # Draw emotion label
                if emotion:
                    label = f"{emotion.upper()}: {confidence*100:.0f}%"
                    color = (0, 255, 0)
                    
                    # Emotion colors
                    if emotion == 'happy':
                        color = (0, 255, 0)
                    elif emotion == 'sad':
                        color = (255, 0, 0)
                    elif emotion == 'angry':
                        color = (0, 0, 255)
                    elif emotion == 'fear':
                        color = (255, 0, 255)
                    elif emotion == 'neutral':
                        color = (128, 128, 128)
                    
                    cv2.putText(frame, label, (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Display stats
        cv2.putText(frame, f"Faces: {len(faces)} | Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Face & Emotion Detection', frame)
        
        # Exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ System closed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()