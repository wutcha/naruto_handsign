import mediapipe as mp
import cv2 as cv
import time

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
BaseOptions = mp.tasks.BaseOptions

latest_result = None

def result_callback(result, output_image, timestamp_ms):
    global latest_result
    latest_result = result

# 7 default handsigns
basic_model_path = 'models/gesture_recognizer.task'

# 12 jutsu handsigns
# add here later

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=basic_model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback,
    num_hands = 2
)

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
            latest_landmarks = latest_result.hand_landmarks
            for landmarks in latest_landmarks:
                for landmark in landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv.circle(frame, (x,y), 5, (0,255,0), -1)
            
            if latest_result.gestures:
                gesture = latest_result.gestures[0][0].category_name
                cv.putText(frame,gesture, (50,50), cv.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 2)

        cv.imshow("frame", frame)

        if cv.waitKey(1) & 0xFF==ord('q'):
            break


capture.release()
cv.destroyAllWindows()