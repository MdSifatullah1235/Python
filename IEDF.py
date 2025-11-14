import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize=((10,10)))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis("off")
    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load the image.")
        return
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original GrayScale Image", gray_image)

    print("Select a option:")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Guassian Smoothing")
    print("5. Median Filtering")
    print("6. Exit")


    while True:
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_image("Sobel Edge Detection", combined_sobel)
        
        elif choice == "2":
            print("Enter the threshold values for Canny Edge Detection:")
            lower_thresh = int(input("Lower Threshold: "))
            upper_thresh = int(input("Upper Threshold: "))
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            display_image("Canny Edge Detection", edges)
        
        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))
        
        elif choice == "4":
            print("Enter the kernel size for Guassian Smoothing:")
            kernel_size = int(input("Kernel Size: "))
            blurred_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
            display_image("Guassian Smoothing", blurred_image)
        
        elif choice == "5":
            print("Enter the kernel size for Median Filtering:")
            kernel_size = int(input("Kernel Size: "))
            median_filtered = cv2.medianBlur(gray_image, kernel_size)
            display_image("Median Filtering", median_filtered)
        
        elif choice == "6":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")


interactive_edge_detection("Example2.jpeg")