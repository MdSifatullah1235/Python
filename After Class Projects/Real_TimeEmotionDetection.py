from fer import FER
import cv2

# Initialize detector
detector = FER(mtcnn=True)

# Open webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Emotion Detection", cv2.WINDOW_NORMAL)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect emotions
    emotions = detector.detect_emotions(frame)

    if emotions:
        box = emotions[0]["box"]
        emotion, score = max(emotions[0]["emotions"].items(), key=lambda item: item[1])

        (x, y, w, h) = box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{emotion} ({score:.2f})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()