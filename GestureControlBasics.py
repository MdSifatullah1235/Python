import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open the camera")
    exit()


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    result = cv2.bitwise_and(frame, frame, mask=skin_mask)

    contours, _ = cv2.findContours(skin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 500:
            x,y,w,h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center_x = x + w // 2
            center_y = y + h // 2

            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Skin Detection", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break