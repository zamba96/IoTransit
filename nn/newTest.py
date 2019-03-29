import cv2
import sys
import numpy as np
import os

# Get user supplied values
imagePath = sys.argv[1]
#protoPath = sys.argv[2]
#modelPath = sys.argv[3]

# Create the haar cascade
#faceCascade = cv2.CascadeClassifier(cascPath)
#faceCascade = cv2.HOGDescriptor()
#faceCascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

proto = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

nh, nw = 500, 500

print("[INFO] loading model...")
# net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
net = cv2.dnn.readNetFromCaffe(proto, model)
print("[INFO] loading Image...")
# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print("[INFO] Image Size:" + format(image.shape[:2]))
(h, w) = image.shape[:2]

(H, W) = image.shape[:2]
(h, w) = (300, 300)
print("[INFO] Image Scaled to:" + format((nh, nw)))
# blob = cv2.dnn.blobFromImage(cv2.resize(image, (500, 500)), 0.007843,
# (500, 500), 127.5)
blob = cv2.dnn.blobFromImage(cv2.resize(image, (nh, nw)),
        0.007843, (nh, nw), 127.5)
# blob = cv2.dnn.blobFromImage(image, 0.007843, image.shape[:2], 127.5)

minConf = 0.7

print("[INFO] computing object detections...")
print("[INFO] Confidence level = {}%".format(minConf*100))
net.setInput(blob)
detections = net.forward()

j = 0
# loop over the detections
for i in np.arange(0, detections.shape[2]):
    # extract the confidence (i.e., probability) associated with the
    # prediction
    confidence = detections[0, 0, i, 2]

    # filter out weak detections by ensuring the `confidence` is
    # greater than the minimum confidence
    if confidence > minConf:
		# extract the index of the class label from the `detections`,
		# then compute the (x, y)-coordinates of the bounding box for
		# the object
		idx = int(detections[0, 0, i, 1])
		if CLASSES[idx] != "person":
					continue
		box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
		(startX, startY, endX, endY) = box.astype("int")

		j+=1

		# display the prediction
		#label = ":{:.1f}%".format(confidence * 100)
		label = "{}:{:.1f}%".format(CLASSES[idx],confidence * 100)
		print("[INFO] {}".format(label))
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 0, 255), 1)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(image, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

# show the output image
print("Found {0} persons!".format(j))
print("/pic/OUTPUT_"+imagePath.split(os.sep)[len(imagePath.split(os.sep))-1])
cv2.imwrite("./pic/OUTPUT__"+imagePath.split(os.sep)[len(imagePath.split(os.sep))-1], image)
cv2.waitKey(0)
