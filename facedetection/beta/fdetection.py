__author__ = 'deniz'

import cv2

class FaceDetector(object):
    #greift auf Haar-Cascade XML Dateien
    def __init__(self):
        self.faceDefault = "haarcascade_frontalface_default.xml"
        self.eye = cv2.CascadeClassifier("haarcascade_eye.xml")
        self.classifier = cv2.CascadeClassifier(self.faceDefault)
    #Sucht nach Gesichter und Augen im frame und zeichnet die Bereiche ein     
    def detectFace(self, frame):
        self.img = frame.copy()
        # detect faces and draw bounding boxes
        assert(self.img.shape[2] == 3)
        g = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        DETECTION_WIDTH = 320
        scale = self.img.shape[1] / float(DETECTION_WIDTH)
        if self.img.shape[1] > DETECTION_WIDTH:
            scaled_height = int(self.img.shape[0]/scale +0.5)
            smallg = cv2.resize(g, (DETECTION_WIDTH,scaled_height))
        else:
            smallg = g
        smallg = cv2.equalizeHist(smallg)
        faces = self.classifier.detectMultiScale(smallg,
                                                 flags=cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT
                                                 )

        for (x,y,w,h) in faces:
            if self.img.shape[1] > DETECTION_WIDTH:
                x = int(x * scale + 0.5)
                y = int(y * scale + 0.5)
                w = int(w * scale + 0.5)
                h = int(h * scale + 0.5)
            cv2.rectangle(self.img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = self.img[y:y+h, x:x+w]

            roi_color = self.img[y:y+h, x:x+w]
            eyes = self.eye.detectMultiScale(roi_gray)

            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        return self.img
