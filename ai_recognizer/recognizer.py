from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
import time

model = load_model('ai_recognizer/my_classifier.h5')

if not os.path.exists('test'):
    os.makedirs('test')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

counter = 0
prediction_name = 'none'
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    height, width, _ = frame.shape

    sx = height // 10 * 2
    sy = height // 10 * 1
    size = height - 2 * sx

    hand_crop = frame[sx+1:sx + size, sy+1:sy + size].copy()

    # Draw white border box
    for i in range(size):
        frame[sx, sy + i] = [255, 255, 255]
        frame[sx + i, sy] = [255, 255, 255]
        frame[sx + size, sy + i] = [255, 255, 255]
        frame[sx + i, sy + size] = [255, 255, 255]

    display_frame = cv2.flip(frame, 1)
    cv2.putText(display_frame, prediction_name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Rock Paper Scissors Trainer', display_frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    hand_crop_resized = cv2.resize(hand_crop, (180, 180))
    
    hand_crop_normalized = hand_crop_resized / 255.0
    
    hand_crop_input = np.expand_dims(hand_crop_normalized, axis=0)
    
    predictions = model.predict(hand_crop_input)
    
    predicted_class = np.argmax(predictions)
    
    prediction_name = 'rock' if predicted_class==1 else 'paper' if predicted_class==0 else 'scissors'

    print(f"Predicted class: {predicted_class}")


    counter += 1  # Increment counter after saving

cap.release()
cv2.destroyAllWindows()
