from cv2 import *
import cv2
import sys
import numpy as np
import os
import argparse
import time
from kafka import KafkaProducer

# Get user supplied values

#protoPath = sys.argv[2]
#modelPath = sys.argv[3]

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", type=str,
                default="MobileNetSSD_deploy.prototxt.txt",
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", type = str, default = "MobileNetSSD_deploy.caffemodel",
                help="path to Caffe pre-trained model")
ap.add_argument("-i", "--input", type=str,
                help="path to optional input image file")
ap.add_argument("-c", "--confidence", type=float, default=0.7,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

imagePath = args["input"]
# Create the haar cascade
#faceCascade = cv2.CascadeClassifier(cascPath)
#faceCascade = cv2.HOGDescriptor()
#faceCascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

proto = args["prototxt"]
model = args["model"]

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
def captura():
	if not args.get("input", False):
		print("[INFO] starting image stream...")
		cam = VideoCapture(0)
		s, image = cam.read()
		imagePath = "nuevaImg.jpg"
	else:
		print("[INFO] opening image file...")
		imagePath = args["input"]
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
	return blob, H, W, image

def identificar(blob, H, W,image):
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
	return j

while True:
    (bs, H, W, image) = captura()
    j = identificar(bs, H, W, image)
    #send info to Kafka
    id = 1
    print("Found {0} persons".format(j))
    print("[INFO] sending to Kafka")
    producer = KafkaProducer(bootstrap_servers='54.149.247.97:9092')
    for i in range(31):
	    producer.send('input', key=i.to_bytes(4, byteorder='little'),value=j.to_bytes(4, byteorder='little'))
    producer.flush()
    print("[INFO] message sent")
    time.sleep(1)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        # if we are not using a video file, stop the camera video stream
        if not args.get("input", False):
            cam.release()

        # close any open windows
        break


# show the output image
print("Found {0} persons!".format(j))
print("/pic/OUTPUT_"+imagePath.split(os.sep)[len(imagePath.split(os.sep))-1])
cv2.imwrite("./pic/OUTPUT__"+imagePath.split(os.sep)[len(imagePath.split(os.sep))-1], image)
cv2.waitKey(0)
