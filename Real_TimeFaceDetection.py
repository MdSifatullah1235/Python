import cv2

#Load the pretrained Haar Vascade Classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Start the video capture from the defualt camera (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open the camera")
    exit()

while True:
    #Capture frame by frame
    ret, frame = cap.read()
    #If frame is read correctly ret will be True
    if not ret:
        print("Error: Failed to capture frame")
        break

    #Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    #Draw rectangles aorund the faces
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    #Display the resulting face
    cv2.imshow('Face Detection - press q to quit', frame)

    #Break the loop is q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Realese the capture and destroy all windows
cap.release()
cv2.destroyAllWindows() 
