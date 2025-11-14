import cv2
import numpy as np
import pyautogui
import time
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: The camera is not opened")
    exit()

prev_y = None
prev_time = time.time()

print("Hand motion detected will now control scrolling.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerskin = np.array([0, 20, 70], dtype=np.uint8)
    upperskin = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lowerskin, upperskin)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        maxcontour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(maxcontour) > 500:
            x, y, w, h = cv2.boundingRect(maxcontour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            centerx = int(x + w / 2)
            centery = int(y + h / 2)
            cv2.circle(frame, (centerx, centery), 5, (0, 0, 255), -1)

            if prev_y is not None:
                if centery < prev_y - 10:
                    pyautogui.scroll(10)
                    print("Scrolled up")
                elif centery > prev_y + 10:
                    pyautogui.scroll(-10)
                    print("Scrolled down")

            prev_y = centery

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Original Frame", frame)
    cv2.imshow("Filtered Frame", result)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()