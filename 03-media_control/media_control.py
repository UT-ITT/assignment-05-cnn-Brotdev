import cv2
import numpy as np
from time import sleep
from keras.models import load_model
from pynput.keyboard import Key, Controller
import sys

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

# Create input device for media keys
keyboard = Controller()

# Load model and labels
model = load_model("gesture_recognition.keras")
label_names = ['like', 'no_gesture', 'dislike', 'fist', 'stop']

# Image/Window related parameters
WINDOW_NAME = "Media Controls"
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
box_tl = min(width // 2, height // 2)
box_x = width - box_tl
box_y = height - box_tl
HAND_THRESHOLD = 0.05
PRED_THRESHOLD = 0.8
IMG_SIZE = 64

def contains_hand(frame):
    # Use simple HSV-Color check
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV mask
    lower = np.array([0, 30, 60])
    upper = np.array([20, 150, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return cv2.countNonZero(mask) / mask.size > HAND_THRESHOLD

# Debounce parameters
DEBOUNCE = 6
debounce = DEBOUNCE
previous = 'no_gesture'

def detect_pose():
    global debounce, previous

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    aoi = frame.copy()[box_y:, box_x:]

    # If the area of interest contains no hand
    if not contains_hand(aoi):
        cv2.rectangle(frame, (box_x, box_y), (width, height), (128,128,128), 2)
        cv2.imshow(WINDOW_NAME, frame)
        return 'no_gesture'
    else:
        cv2.rectangle(frame, (box_x, box_y), (width, height), (0,128,0), 2)

    # Predict pose using model
    aoi = cv2.resize(aoi, (IMG_SIZE, IMG_SIZE)).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
    prediction = model.predict(aoi, verbose=0)
    pred_label = label_names[np.argmax(prediction)]
    pred_confidence = np.max(prediction)

    # Show labled image
    cv2.putText(frame, f'{pred_label} - {debounce}', (box_x, box_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,128,0), 2, cv2.LINE_AA)
    cv2.imshow(WINDOW_NAME, frame)

    # Debounce prediction
    if previous == pred_label and pred_confidence > PRED_THRESHOLD:
        debounce -= 1
        match debounce:
            case 0:
                pass
            case _:
                debounce = max(debounce, 0)
                return 'no_gesture'
    else:
        previous = pred_label
        debounce = DEBOUNCE
        return 'no_gesture'

    return pred_label

while 1:
    if cv2.waitKey(1) == 113: # Keycode q
        break

    match detect_pose():
        case 'fist':
            # Play media
            print("Pressing Play/Pause...")
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
        case 'like':
            # Volume up
            print("Pressing Volume up...")
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
        case 'dislike':
            # Volume down
            print("Pressing Volume down...")
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
        case 'stop':
            # Pause media
            print("Pressing Stop...")
            keyboard.press(Key.media_stop)
            keyboard.release(Key.media_stop)
        case _:
            sleep(0.016)

cv2.destroyAllWindows()
cap.release()
