import cv2
import numpy as np
import imutils
import pytesseract

image = cv2.imread("realMagicCards.png", cv2.IMREAD_COLOR)

file = open("recognized.txt", "w+")
custom_config = r'--oem 3 --psm 6'
file.write(pytesseract.image_to_string(image, config=custom_config))
file.close()

image = imutils.resize(image, width = 1500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
edged = cv2.Canny(blur, 10, 100)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

dilate = cv2.dilate(edged, kernel, iterations=1)

contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image_copy = image.copy()

cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)

cv2.imshow("image", image)
cv2.imshow("edged", edged)
cv2.imshow("Contours", image_copy)

cv2.waitKey(0)

cv2.destroyAllWindows()