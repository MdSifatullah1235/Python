import cv2

# load the pretrained Haar Vascade Classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Intialize the video capture from the defualt camera (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open the camera")
    exit()

while True:
    #Capture Frame by Frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    #Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect faces in grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    #Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    #Display the count of faces

    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), font, 1, (0, 255, 0), 2)

    #Display the frame with faces
    cv2.imshow("Face Detection", frame)

    #Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Realease the webcame and destroy the window
cap.release()
cv2.destroyAllWindows()