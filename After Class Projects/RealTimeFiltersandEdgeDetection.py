import cv2
import numpy as np

def apply_filters(img, filter_type, filter_input=None):
    filtered_img = img.copy()
    
    if filter_type == "red_tint" and filter_input is not None:
        filtered_img[:,:,1] = 0
        filtered_img[:,:,0] = 0
        filtered_img[:,:,2] = filter_input

    elif filter_type == "green_tint" and filter_input is not None:
        filtered_img[:,:,0] = 0
        filtered_img[:,:,2] = 0
        filtered_img[:,:,1] = filter_input

    elif filter_type == "blue_tint" and filter_input is not None:
        filtered_img[:,:,1] = 0
        filtered_img[:,:,2] = 0
        filtered_img[:,:,0] = filter_input

    elif filter_type == "sobel":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        combined = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
        filtered_img = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)

    elif filter_type == "canny":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        filtered_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    elif filter_type == "black":
        filtered_img[:,:,:] = 0

    elif filter_type == "white":
        filtered_img[:,:,:] = 255

    return filtered_img


image_path = "Example2.jpeg"
img = cv2.imread(image_path)

if img is None:
    print(f"Error: {image_path} not found.")
else:
    print("Press keys to apply filters:\n"
          "r - Red Tint\n"
          "g - Green Tint\n"
          "b - Blue Tint\n"
          "s - Sobel\n"
          "c - Canny\n"
          "q - Quit")

    filter_type = "original"
    filter_input = None
    cv2.imshow("Filtered Image", img)

    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord("r"):
            filter_input = int(input("Enter red intensity (0–255): "))
            filter_type = "red_tint"
        elif key == ord("g"):
            filter_input = int(input("Enter green intensity (0–255): "))
            filter_type = "green_tint"
        elif key == ord("b"):
            filter_input = int(input("Enter blue intensity (0–255): "))
            filter_type = "blue_tint"
        elif key == ord("s"):
            filter_type = "sobel"
        elif key == ord("c"):
            filter_type = "canny"
        elif key == ord("q"):
            print("Exiting...")
            break
        
        filtered = apply_filters(img, filter_type, filter_input)
        cv2.imshow("Filtered Image", filtered)

cv2.destroyAllWindows()