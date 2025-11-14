import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_birghtness_control as sbc

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils


try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume_range = volume.GetVolumeRange()
    min_vol = volume_range[0]
    max_vol = volume_range[1]
except Exception as e:
    print("Error: ", e)
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Failed to open the camera")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame")
        break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for i , hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[i].classification[0].label
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h,y,_ = img.shape
                thumb_pos = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
                index_pos = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

                cv2.circle(img, thumb_pos, 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, index_pos, 5, (0, 255, 0), cv2.FILLED)
                cv2.line(img, thumb_pos, index_pos, (0, 255, 0), 2)

                length = hypot(index_pos[0] - thumb_pos[0], index_pos[1] - thumb_pos[1])
                vol = np.interp(length, [30, 300], [min_vol, max_vol])

                if hand_label == "Right":
                    vol = np.interp(length, [30, 300], [min_vol, max_vol])
                    try:
                        volume.SetMasterVolumeLevel(vol, None)
                    except Exception as e:
                        print("Error: ", e)
                        exit()
                    
                    vol_bar = np.interp(length, [30, 300], [400, 150])
                    vol_per = np.interp(length, [30, 300], [0, 100])
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"{int(vol_per)}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

                    cv2.putText(img, f"{int(vol_per)}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                
                elif hand_label == "Left":
                    brightness = np.interp(length, [30, 300], [0, 100])

                    try:
                        sbc.set_brightness(brightness)
                    except Exception as e:
                        print("Error: ", e)
                        exit()
                    
                    brightness_bar = np.interp(length, [30, 300], [400, 150])
                    brightness_per = np.interp(length, [30, 300], [0, 100])
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(brightness_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"{int(brightness_per)}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()