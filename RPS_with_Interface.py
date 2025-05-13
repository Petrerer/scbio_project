import cv2
import numpy as np
import random
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model

# Load model and gesture labels
model = load_model('ai_recognizer/my_classifier.h5')
gestures = ['paper', 'rock', 'scissors']

# Initialize scores
user_score = 0
ties_score = 0
machine_score = 0

# Series-related variables
mode_rounds = 0
user_wins_series = 0
machine_wins_series = 0
series_mode = False

# Create main window
root = tk.Tk()
root.title("Rock, Paper, Scissors Game")
root.geometry("800x600")

# Load and place background image
background_image = Image.open("background_image.jpg").resize((2000, 1000))
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Main content frame
content_frame = tk.Frame(root, bg='white')
content_frame.place(relx=0.5, rely=0.5, anchor='center')

# Video label
label_video = Label(content_frame)
label_video.pack()

# Result label in a separate frame to isolate background color
result_frame = tk.Frame(content_frame, bg="white")
result_frame.pack(pady=10)
label_result = Label(result_frame, text="", font=("Arial", 16), bg="white", fg="black")
label_result.pack()

# Score labels
label_score_title = Label(content_frame, text="Score", font=("Arial", 16, "bold"), bg="white")
label_score_title.pack()

label_score_values = Label(content_frame, text="🧟 You: 0   ⚖️ Ties: 0   💻 Machine: 0", font=("Arial", 14), bg="white")
label_score_values.pack(pady=5)

# Game mode selector
def game_mode(val):
    global mode_rounds, user_wins_series, machine_wins_series, series_mode, user_score, ties_score, machine_score
    user_score = 0
    ties_score = 0
    machine_score = 0
    user_wins_series = 0
    machine_wins_series = 0
    update_score()
    if val == "Single Match":
        series_mode = False
        mode_rounds = 0
        label_result.config(text="Mode: Single Match")
    else:
        series_mode = True
        mode_rounds = int(val)
        user_wins_series = 0
        machine_wins_series = 0
        label_result.config(text=f"Mode: Best of {mode_rounds}")

mode_frame = tk.Frame(content_frame, bg="white")
mode_frame.pack(pady=5)
tk.Label(mode_frame, text="Mode:", font=("Arial", 12), bg="white").pack(side=tk.LEFT)
mode_option = tk.StringVar(root)
mode_option.set("Single Match")
mode_menu = tk.OptionMenu(mode_frame, mode_option, "Single Match", "3", "5", "10", command=game_mode)
mode_menu.config(font=("Arial", 12))
mode_menu.pack(side=tk.LEFT)

# Webcam
cap = cv2.VideoCapture(0)

# Use the model to understand the gesture from the image
def get_prediction(frame):
    height, width, _ = frame.shape
    sx = height // 10 * 2
    sy = height // 10 * 1
    size = height - 2 * sx
    hand_crop = frame[sx+1:sx + size, sy+1:sy + size]
    img = cv2.resize(hand_crop, (180, 180)) / 255.0
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    return gestures[np.argmax(preds)]

# Update de score
def update_score():
    label_score_values.config(text=f"🧟 You: {user_score}   ⚖️ Ties: {ties_score}   💻 Machine: {machine_score}")

# Flash background with color
def flash_result(color):
    background_label.config(image='', bg=color)
    label_result.config(bg='white')  # mantener el recuadro del texto blanco
    root.after(500, lambda: background_label.config(image=background_photo))

# Play the game
def play():
    global user_score, ties_score, machine_score, user_wins_series, machine_wins_series
    ret, frame = cap.read()
    if not ret:
        label_result.config(text="Camera error")
        return

    player = get_prediction(frame)
    machine = random.choice(gestures)

    if player == machine:
        result = "It's a tie!"
        ties_score += 1
        flash_result("#e2e3e5")
    elif (player == "rock" and machine == "scissors") or (player == "scissors" and machine == "paper") or (player == "paper" and machine == "rock"):
        result = "You Win! 🎉"
        user_score += 1
        flash_result("#28a745")
        if series_mode:
            user_wins_series += 1
    else:
        result = "You Lose 😞"
        machine_score += 1
        flash_result("#dc3545")
        if series_mode:
            machine_wins_series += 1

    label_result.config(text=f"You: {player} | Machine: {machine}\n{result}")
    update_score()

    if series_mode:
        half = mode_rounds // 2 + 1
        if user_wins_series == half:
            label_result.config(text=f"You won the best of {mode_rounds}! 🏆")
            user_wins_series = 0
            machine_wins_series = 0
        elif machine_wins_series == half:
            label_result.config(text=f"Machine won the best of {mode_rounds} 😔")
            user_wins_series = 0
            machine_wins_series = 0

# Countdown to begin the game
def countdown(seconds=3):
    if seconds > 0:
        label_result.config(text=f"{seconds}")
        root.after(1000, countdown, seconds - 1)
    else:
        play()

# Reset de score
def reset_score():
    global user_score, ties_score, machine_score, user_wins_series, machine_wins_series
    user_score = 0
    ties_score = 0
    machine_score = 0
    user_wins_series = 0
    machine_wins_series = 0
    update_score()
    label_result.config(text="Score reset")

# Close the game
def close():
    cap.release()
    root.destroy()

# Update the video frame
def update_video():
    ret, frame = cap.read()
    if ret:
        height, width, _ = frame.shape
        sx = height // 10 * 2
        sy = height // 10 * 1
        size = height - 2 * sx

        for i in range(size):
            frame[sx, sy + i] = [255, 255, 255]
            frame[sx + i, sy] = [255, 255, 255]
            frame[sx + size, sy + i] = [255, 255, 255]
            frame[sx + i, sy + size] = [255, 255, 255]

        frame = cv2.flip(frame, 1)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img))
        label_video.imgtk = img
        label_video.configure(image=img)

    root.after(30, update_video) # Refresh every 30 ms

# Buttons
buttons_frame = tk.Frame(content_frame, bg="white")
buttons_frame.pack(pady=10)

button_play = Button(buttons_frame, text="📷 Play", font=("Arial", 12), bg="#4CAF50", fg="white", command=countdown)
button_play.pack(side=tk.LEFT, padx=10)

button_reset = Button(buttons_frame, text="🔄 Reset", font=("Arial", 12), bg="#FFC107", command=reset_score)
button_reset.pack(side=tk.LEFT, padx=10)

button_exit = Button(buttons_frame, text="🚪 Exit", font=("Arial", 12), bg="#F44336", fg="white", command=close)
button_exit.pack(side=tk.LEFT, padx=10)

# Start video loop
update_video()
root.mainloop()