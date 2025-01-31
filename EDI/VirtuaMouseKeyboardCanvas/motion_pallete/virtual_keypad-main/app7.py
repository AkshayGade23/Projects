import cv2
import numpy as np
import time
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Constants
ml = 150
max_x, max_y = 250 + ml, 50
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 7
prevx, prevy = 0, 0
running = True  # Flag for the main loop




# Get tools function
def getTool(x):
    if x < 50 + ml:
        return "line"
    elif x < 100 + ml:
        return "rectangle"
    elif x < 150 + ml:
        return "draw"
    elif x < 200 + ml:
        return "circle"
    else:
        return "erase"

def index_raised(yi, y9):
    if (y9 - yi) > 40:
        return True
    return False

# Drawing tools
tools = cv2.imread("tools.png")
tools = tools.astype('uint8')

mask = np.ones((480, 640)) * 255
mask = mask.astype('uint8')

# Initialize Tkinter window
root = tk.Tk()
root.title("Virtual Painter")

# Create a canvas to display the image
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Create a label to display the current tool
tool_label = tk.Label(root, text="Current Tool: ")
tool_label.pack()

# Function to update the tool label and canvas
def update_tool_label():
    tool_label_text = "Current Tool: " + curr_tool
    tool_label.config(text=tool_label_text)

def update_gui():
    update_tool_label()
    update_canvas(frm)

# Function to update the canvas with a new image
def update_canvas(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    img = ImageTk.PhotoImage(img)
    canvas.img = img  # Keep a reference to avoid garbage collection
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Function to update the tool label


# Function for image preprocessing
def preprocess_image(image):
    # Check the number of channels
    if image.ndim == 2:  # Single-channel image
        preprocessed_image = image
    else:
        # Convert to grayscale
        preprocessed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(preprocessed_image, 127, 255, cv2.THRESH_BINARY)
    
    # Optional: Denoising (uncomment the line below if needed)
    # thresh = cv2.fastNlMeansDenoising(thresh, None, h=10)

    return thresh

# Function to recognize text
def recognize_text():
    global recognized_text

    # # Preprocess the mask image
    # preprocessed_image = preprocess_image(mask)

    # # Perform OCR on the preprocessed image
    # pil_image = Image.fromarray(preprocessed_image)
    pil_image = Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
    recognized_text = pytesseract.image_to_string(pil_image, config='--psm 6')

    # Post-process recognized text
    recognized_text = filter_unwanted_characters(recognized_text)

    # Clear existing text on the canvas with the "text" tag
    canvas.delete("text")

    # Display the recognized text on the canvas with the "text" tag
    canvas.create_text(250, 250, text=recognized_text, font=("Helvetica", 12), fill="blue", tags="text")

    # Update the mask with the recognized text
    mask[:] = 255  # Clear the mask
    cv2.putText(mask, recognized_text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

    # Erase scribble immediately
    erase_scribble()


# Function to filter unwanted characters
def filter_unwanted_characters(text):
    # Define characters to keep (adjust as needed)
    allowed_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?! "

    # Filter out unwanted characters
    filtered_text = ''.join(char for char in recognized_text if char in allowed_characters)

    return filtered_text


# Function to erase scribble
def erase_scribble():
    # Clear only the items with the tag "scribble" on the canvas
    canvas.delete("scribble")


# Create a button for text recognition
recognize_button = tk.Button(root, text="Recognize Text", command=recognize_text)
recognize_button.pack()


# Setup mediapipe hands
hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)

draw = mp.solutions.drawing_utils

# Setup webcam
cap = cv2.VideoCapture(0)

# Function to check if thumb and index finger are close together
def is_thumb_index_close(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[hands.HandLandmark.INDEX_FINGER_TIP]
    
    # Define a threshold for closeness (adjust as needed)
    threshold = 0.03
    
    # Check if the thumb and index finger are close together
    distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    return distance < threshold

# Function to handle window close event
def on_close():
    global running
    running = False
    root.destroy()

# Bind the close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Main loop
while running:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    op = hand_landmark.process(rgb)

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)
            x, y = int(i.landmark[8].x * 640), int(i.landmark[8].y * 480)

            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()
                    time_init = False
                ptime = time.time()

                cv2.circle(frm, (x, y), rad, (0, 255, 255), 2)
                rad -= 1

                if (ptime - ctime) > 0.8:
                    curr_tool = getTool(x)
                    print("your current tool set to : ", curr_tool)
                    time_init = True
                    rad = 40

            else:
                time_init = True
                rad = 40

            if curr_tool == "draw":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    cv2.line(mask, (prevx, prevy), (x, y), 0, thick)
                    prevx, prevy = x, y

                else:
                    prevx = x
                    prevy = y

            elif curr_tool == "line":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not(var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.line(frm, (xii, yii), (x, y), (50, 152, 255), thick)

                else:
                    if var_inits:
                        cv2.line(mask, (xii, yii), (x, y), 0, thick)
                        var_inits = False

            elif curr_tool == "rectangle":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not(var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.rectangle(frm, (xii, yii), (x, y), (0, 255, 255), thick)

                else:
                    if var_inits:
                        cv2.rectangle(mask, (xii, yii), (x, y), 0, thick)
                        var_inits = False

            elif curr_tool == "circle":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not(var_inits):
                        xii, yii = x, y
                        var_inits = True

                    cv2.circle(frm, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (255, 255, 0),
                               thick)

                else:
                    if var_inits:
                        cv2.circle(mask, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (0, 255, 0),
                                   thick)
                        var_inits = False

            elif curr_tool == "erase":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    cv2.circle(frm, (x, y), 30, (0, 0, 0), -1)
                    cv2.circle(mask, (x, y), 30, 255, -1)
                    
                    
            if is_thumb_index_close(i):
                # Perform text recognition when the gesture is detected
                recognize_text()

    op = cv2.bitwise_and(frm, frm, mask=mask)
    frm[:, :, 1] = op[:, :, 1]
    frm[:, :, 2] = op[:, :, 2]

    frm[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, frm[:max_y, ml:max_x], 0.3, 0)

    cv2.putText(frm, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Update the GUI
    update_gui()

    root.update()  # Update the Tkinter window

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()