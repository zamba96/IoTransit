import cv2
import sys

# Get user supplied values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
#faceCascade = cv2.HOGDescriptor()
#faceCascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
	image,
#	winStride=(8,8),
#	padding=(32, 32),
#	scale=1.05
    scaleFactor=1.01,
    minNeighbors=5,
    minSize=(30, 30)
#    flags = cv2.CV_HAAR_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))
#for(a) in faces:
#	print(a)
# Draw a rectangle around the faces
#for (x, y, w, h) in faces:
#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

for (xA, yA, xB, yB) in faces:
        #print(i)
	#i++
	cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

cv2.imwrite("out.jpg", image)
cv2.waitKey(0)
