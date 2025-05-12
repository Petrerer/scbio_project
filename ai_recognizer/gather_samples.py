import cv2
import numpy as np
import os

# Counters for saving images
rock_count = 130
paper_count = 130
scissors_count = 130

# Create folders if they don't exist
os.makedirs("dataset/rock", exist_ok=True)
os.makedirs("dataset/paper", exist_ok=True)
os.makedirs("dataset/scissors", exist_ok=True)

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    height, width, _ = frame.shape

    # Define square hand box position and size
    sx = height // 10 * 2
    sy = height // 10 * 1
    size = height - 2 * sx

    # Draw white border box
    for i in range(size):
        frame[sx, sy + i] = [255, 255, 255]
        frame[sx + i, sy] = [255, 255, 255]
        frame[sx + size, sy + i] = [255, 255, 255]
        frame[sx + i, sy + size] = [255, 255, 255]

    cv2.imshow('Rock Paper Scissors Trainer', cv2.flip(frame, 1))

    key = cv2.waitKey(1)

    hand_crop = frame[sx+1:sx + size, sy+1:sy + size]

    if key == ord('q'):
        break
    elif key == ord('1'):
        filename = f"dataset/rock/rock{rock_count}.png"
        cv2.imwrite(filename, hand_crop)
        print(f"Saved {filename}")
        rock_count += 1
    elif key == ord('2'):
        filename = f"dataset/paper/paper{paper_count}.png"
        cv2.imwrite(filename, hand_crop)
        print(f"Saved {filename}")
        paper_count += 1
    elif key == ord('3'):
        filename = f"dataset/scissors/scissors{scissors_count}.png"
        cv2.imwrite(filename, hand_crop)
        print(f"Saved {filename}")
        scissors_count += 1

cap.release()
cv2.destroyAllWindows()
