import cv2 as cv
import os
import time

# remember to change for each sign
LABEL = "boar"
COUNT_NEEDED = 100
SAVE_PATH = os.path.join("dataset", LABEL)
capture = cv.VideoCapture(0)

print(f"collecting pictures for: {LABEL}")

count = 0
collecting = False

while count < COUNT_NEEDED:
    ret, frame = capture.read()
    
    # mirrored
    frame = cv.flip(frame, 1)
    
    display_frame = frame.copy()
    cv.putText(display_frame, f"{count}/{COUNT_NEEDED}", (10, 30), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv.imshow("frame", display_frame)
    key = cv.waitKey(1)
    if key == ord('s'):
        collecting = True
        print("beginning da captoore in 3 secs...")
        time.sleep(3)

    if collecting:
        img_name = os.path.join(SAVE_PATH, f"{LABEL}_{count}.jpg")
        cv.imwrite(img_name, frame)
        count += 1
        time.sleep(0.5)

print("terminado")
capture.release()
cv.destroyAllWindows()