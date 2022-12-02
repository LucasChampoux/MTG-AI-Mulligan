import cv2
import pytesseract
import requests
import urllib.parse
from time import sleep
import difflib
import sys

#check that cardName is located in scryfall api
def APIConfirmCheck(cardName):
    url = "https://api.scryfall.com/cards/search?q=" + urllib.parse.quote(cardName, safe='')

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if(response.status_code == 404):
        return False
    else:
        return True

#get command line input for what image to use
n = len(sys.argv)
if(n == 0):
    print("No file provided. Please include file name in arguments")
    exit()
image = cv2.imread(sys.argv[0])
original_image = image.copy()

#parse JSON
jsonFile = open("NamesOnly.json", "r")
newJson = jsonFile.read().replace("", "").replace("  ", "").splitlines()
jsonFile.close()

#process image for edge detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blur, 10, 100)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(edged, kernel, iterations=1)

#find the contours of the image
contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours =  contours[0] if len(contours) == 2 else contours[1]
image_number = 0

nameList = list()

for c in contours:
    #find the coordinates of each card and draw a rectangle
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)

    #use the card's edges to extract the region of interest into its own image
    ROI = original_image[y:y+h, x:x+w]
    if(ROI.shape[0] > ROI.shape[1]):
        cv2.imwrite("ROI_{}.png".format(image_number), ROI)
        custom_config = r'--oem 3 --psm 6'

        #extract title of the card from the image
        tempVal = pytesseract.image_to_string("ROI_{}.png".format(image_number), config = custom_config).splitlines()

        #validate the card's title
        title_match = difflib.get_close_matches(tempVal[0], newJson)
        if not len(title_match) == 0:
            nameList.append(title_match[0])
        else:
            print("Card " + tempVal[0] + " does not appear to be a valid card name")

    image_number += 1

newFile = open("cardTitles.txt".format(image_number), "w+")

#add each card detected to the cardTitles file if the card is validated by the api
for a in nameList:
    sleep(.01)
    if APIConfirmCheck(a) is True:
        newFile.write(a)
        newFile.write("\n")
    else:
        print("card " + a + " was not found.")


newFile.close()
cv2.imshow("image", image)

cv2.waitKey(0)

cv2.destroyAllWindows()
