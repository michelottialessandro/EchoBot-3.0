import cv2
import numpy as np

file_name = "roboteyes.mp4"
window_name = "window"
interframe_wait_ms = 30

cap = cv2.VideoCapture(file_name)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.moveWindow(window_name,1920,0)
screen_width, screen_height = cv2.getWindowImageRect(window_name)[:2]

while (True):
    ret, frame = cap.read()
    if not ret:
        print("Reached end of video, exiting.")
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    #frame = cv2.resize(frame, (640, 480))
    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
        print("Exit requested.")
        break

cap.release()
cv2.destroyAllWindows()
