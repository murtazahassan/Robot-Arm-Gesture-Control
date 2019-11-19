import cv2
import numpy as np
from RobotHandGestures import utlis

##############################################################################

cameraNo = 1
portNo ="COM4"
cropVals = 100,100,300,400 # StartPointY StartPointX h w
frameWidth = 640
frameHeight = 480
brightnessImage = 230

##############################################################################

cap = cv2.VideoCapture(cameraNo)
cap.set(10, brightnessImage)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
utlis.initializeTrackBar()
utlis.connectToRobot(portNo)

while True:
    _, img = cap.read()
    imgResult = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    trackBarPos = utlis.getTrackbarValues()
    imgMask, imgColorFilter = utlis.colorFilter(imgHSV,trackBarPos)

    imgCropped = imgMask[cropVals[1]:cropVals[2]+cropVals[1],cropVals[0]:cropVals[0]+cropVals[3]]
    imgResult = imgResult[cropVals[1]:cropVals[2] + cropVals[1], cropVals[0]:cropVals[0] + cropVals[3]]
    imgOpen =cv2.morphologyEx(imgCropped, cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    imgClosed = cv2.morphologyEx(imgOpen, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
    imgFilter = cv2.bilateralFilter(imgClosed, 5, 75, 75)
    imgContour,imgResult = utlis.getContours(imgFilter,imgResult)

    ## TO DISPLAY
    cv2.rectangle(img, (cropVals[0], cropVals[1]), (cropVals[0]+cropVals[3], cropVals[2]+cropVals[1]), (0, 255, 0), 2)
    stackedImage = utlis.stackImages(0.7,([img,imgMask,imgColorFilter],[imgCropped,imgContour,imgResult]))



    #imgBlank = np.zeros((512, 512, 3), np.uint8)
    #stackedImage = utlis.stackImages(0.7, ([img, imgBlank, imgBlank], [imgBlank, imgBlank, imgBlank]))

    cv2.imshow('Stacked Images', stackedImage)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()