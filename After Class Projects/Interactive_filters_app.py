import cv2
import numpy as np

def apply_color_filters(image, filter_type, filter_input=0):
    filtered_image = image.copy()

    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0  # remove green
        filtered_image[:, :, 0] = 0  # remove blue

    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0  # remove blue
        filtered_image[:, :, 2] = 0  # remove red

    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  # remove green
        filtered_image[:, :, 2] = 0  # remove red

    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], filter_input)

    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], filter_input)

    return filtered_image


# Load the image
img_path = str(input("Enter the path of the image: "))
img = cv2.imread(img_path)

if img is None:
    print("Failed to load the image.")
else:
    filter_type = "original"
    filter_input = 0

    print("Press the following keys to apply filters: ")
    print("r - Red Tint")
    print("g - Green Tint")
    print("b - Blue Tint")
    print("i - Increase Red")
    print("d - Decrease Blue")
    print("o - Original Image")
    print("e - Exit")

    while True:
        if filter_type == "original":
            filtered_img = img
        else:
            filtered_img = apply_color_filters(img, filter_type, filter_input)

        cv2.imshow("Filtered Image", filtered_img)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("r"):
            filter_type = "red_tint"
        elif key == ord("g"):
            filter_type = "green_tint"
        elif key == ord("b"):
            filter_type = "blue_tint"
        elif key == ord("i"):
            filter_input = int(input("Enter the amount to increase red: "))
            filter_type = "increase_red"
        elif key == ord("d"):
            filter_input = int(input("Enter the amount to decrease blue: "))
            filter_type = "decrease_blue"
        elif key == ord("o"):
            filter_type = "original"
        elif key == ord("e"):
            print("Exiting...")
            break
        else:
            print("Invalid key pressed.")

    cv2.destroyAllWindows()
