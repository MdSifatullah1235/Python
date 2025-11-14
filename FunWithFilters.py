import cv2
import numpy as np

def apply_color_filters(image,filter_type):
    filtered_image = image.copy()
    if filter_type =="red_tint":
        filtered_image[:,:,1] = 0 #green channel to 0
        filtered_image[:,:,0] = 0 #blue channel to 0
    
    elif filter_type == "green_tint":
        filtered_image[:,:,0] = 0 #blue channel to 0
        filtered_image[:,:,2] = 0 #red channel to 0

    elif filter_type == "blue_tint":
        filtered_image[:,:,1] = 0 #green channel to 0
        filtered_image[:,:,2] = 0 #red channel to 0
    
    elif filter_type == "increase_red":
        #Increase the intensity of the red channel
        filtered_image[:,:,2] = cv2.add(filtered_image[:,:,2],50)
    
    elif filter_type == "decrease_blue":
        #Decrease the intensity of the red channel
        filtered_image[:,:,2] = cv2.subtract(filtered_image[:,:,2],50)
    
    return filtered_image


#Load the img
img_path = "Example2.jpeg"
img = cv2.imread(img_path)

if img is None:
    print("Failed to load the image.")

else:
    filter_type = "original"

    print("Press the folollowing keys to apply filters: ")
    print("r - Red Tint")
    print("g - Green Tint")
    print("b - Blue Tint")
    print("i - Increase Red")
    print("d - Decrease Blue")
    print("e - Exit")
    while True:
        filtered_img = apply_color_filters(img,filter_type)
        cv2.imshow("Filtered Image",filtered_img)

        key = cv2.waitKey(0) & 0xFF
        if key == ord("r"):
            filter_type = "red_tint"
        elif key == ord("g"):
            filter_type = "green_tint"
        elif key == ord("b"):
            filter_type = "blue_tint"
        elif key == ord("i"):
            filter_type = "increase_red"
        elif key == ord("d"):
            filter_type = "decrease_blue"
        elif key == ord("e"):
            print("Exiting...")
            break
        else:
            print("Invalid key pressed. Please try again.")

cv2.destroyAllWindows()