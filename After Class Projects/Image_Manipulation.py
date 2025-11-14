import cv2
import numpy as np

image = cv2.imread("Example2.jpeg")

(h,w) = image.shape[:2]
center = (w // 2, h // 2)

degree_input = int(input("Enter the degree: "))
M = cv2.getRotationMatrix2D(center, degree_input, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))

cv2.imshow("Original", image)
cv2.imshow("Rotated", rotated)
cv2.waitKey(0)

brightness_input = int(input("Enter the brightness: "))

brightness_matrix = np.ones(image.shape, dtype="uint8") * brightness_input
brighter = cv2.add(rotated, brightness_matrix)

cv2.imshow("Brighter", brighter)
cv2.waitKey(0)