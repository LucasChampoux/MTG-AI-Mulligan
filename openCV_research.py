import cv2
import numpy as np
import imutils
import pytesseract

image = cv2.imread("text.png", cv2.IMREAD_COLOR)

file = open("recognized.txt", "w+")
custom_config = r'--oem 3 --psm 6'
file.write(pytesseract.image_to_string(image, config=custom_config))
file.close()

image = imutils.resize(image, width = 500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (3,3), 0)
rect, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)

contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
threshold_min_area = 400
number_of_contours = 0



for c in contours:
    area = cv2.contourArea(c)
    if area > threshold_min_area:
        cv2.drawContours(image, [c], 0, (36,255,12), 3)
        number_of_contours += 1

print(number_of_contours)
cv2.imshow("image", image)
cv2.imshow("thresh", thresh)



cv2.waitKey(0)

cv2.destroyAllWindows()