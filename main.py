import mediapipe as mp
import cv2 as cv
import time
from config import model_path

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
BaseOptions = mp.tasks.BaseOptions

latest_result = None

def result_callback(result, output_image, timestamp_ms):
    global latest_result
    latest_result = result

# 7 default handsigns
basic_model_path = model_path

# 12 jutsu handsigns
# add here later

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=basic_model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback,
    num_hands = 2
)

def draw_hand(frame, latest_result):
    HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),           # Index
    (0, 9), (9, 10), (10, 11), (11, 12),      # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
    (5, 9), (9, 13), (13, 17)                 # Palm
    ]

    latest_landmarks = latest_result.hand_landmarks
    #print(latest_landmarks)
    for landmarks in latest_landmarks:

        #lines
        for idx1, idx2 in HAND_CONNECTIONS:
            if idx1 < len(landmarks) and idx2 < len(landmarks):
                pt1 = landmarks[idx1]
                pt2 = landmarks[idx2]
                shifted_pt1 = (int(pt1.x * frame.shape[1]), int(pt1.y * frame.shape[0]))
                shifted_pt2 = (int(pt2.x * frame.shape[1]), int(pt2.y * frame.shape[0]))     
                cv.line(frame, shifted_pt1, shifted_pt2, (0,0,0), 2)

        #landmarks
        for landmark in landmarks:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv.circle(frame, (x,y), 5, (0,255,0), -1)
    
    



with GestureRecognizer.create_from_options(options) as recognizer:
    capture = cv.VideoCapture(0)

    while capture.isOpened():
        ret, frame = capture.read()

        rgbframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbframe)
        timestamp = int(time.time() * 1000)
        recognizer.recognize_async(mp_image, timestamp)

        # drawing stuff
        if latest_result and latest_result.hand_landmarks:
            draw_hand(frame, latest_result)

            # latest_landmarks = latest_result.hand_landmarks
            # for landmarks in latest_landmarks:
            #     for landmark in landmarks:
            #         x = int(landmark.x * frame.shape[1])
            #         y = int(landmark.y * frame.shape[0])
            #         cv.circle(frame, (x,y), 5, (0,255,0), -1)
            
            if latest_result.gestures:
                #print(latest_result,'\n')
                gesture = latest_result.gestures[0][0].category_name
                score = str(round(latest_result.gestures[0][0].score,2))
                cv.putText(frame,gesture,(50,50), cv.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 2)
                cv.putText(frame,score,(50,75), cv.FONT_HERSHEY_TRIPLEX,1, (0,0,0), 2)

        cv.imshow("frame", frame)

        if cv.waitKey(1) & 0xFF==ord('q'):
            break


capture.release()
cv.destroyAllWindows()