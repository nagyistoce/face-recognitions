__author__ = 'deniz'

import cv2, math

class FaceDetector(object):
    #greift auf Haar-Cascade XML Dateien
    def __init__(self):
        self.faceDefault = "haarcascade_frontalface_default.xml"
        self.faceAlt2 = "haarcascade_frontalface_alt2.xml"
        self.lefteye = cv2.CascadeClassifier("haarcascade_lefteye_2splits.xml")
        self.righteye = cv2.CascadeClassifier("haarcascade_righteye_2splits.xml")
        self.classifier = cv2.CascadeClassifier(self.faceAlt2)
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
            face = self.img[y:y+h, x:x+w]
            success, lefteye, righteye = self.detectEyes(face)
            if success:
                #preprocessing
                pp = FacePreprocessor(lefteye,righteye,face)
                pp.doPreprocess()
        return self.img
    
    def detectEyes(self, face):
        EYE_SX=0.12
        EYE_SY=0.17
        EYE_SW=0.37
        EYE_SH=0.36
        gface = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        #Rechtes und linkes Augenbereich
        lx=int(face.shape[0]*EYE_SX +0.5)
        ty=int(face.shape[1]*EYE_SY +0.5)
        wx=int(face.shape[0]*EYE_SW +0.5)
        hy=int(face.shape[1]*EYE_SH +0.5)
        rx=int(face.shape[0]*(1.0-EYE_SX-EYE_SW)+0.5)
        tlFace = gface[ty:ty+hy,lx:lx+wx]
        trFace = gface[ty:ty+hy,rx:rx+wx]
        #Suchgebiete der Augen
        #cv2.rectangle(face,(lx,ty),(lx+wx,ty+hy),(0,255,255),2)
        #cv2.rectangle(face,(rx,ty),(rx+wx,ty+hy),(0,255,0),2)
        lefteye = self.lefteye.detectMultiScale(tlFace)
        righteye = self.righteye.detectMultiScale(trFace)
        if len(lefteye) and len(righteye):
            for (ex,ey,ew,eh) in lefteye:
                cv2.rectangle(face[ty:ty+hy,lx:lx+wx],(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
            for (ex,ey,ew,eh) in righteye:
                cv2.rectangle(face[ty:ty+hy,rx:rx+wx],(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            return True, lefteye, righteye
        return False, lefteye, righteye

class FacePreprocessor(object):
    def __init__(self, lefteye, righteye, face):
        self.lefteye = lefteye
        self.righteye = righteye
        self.face = face
    def doPreprocess(self):
        self.gTransform()
        self.allHistEqual()
        #img = cv2.bilateralFilter(img,d=0,sigmaColor=20.0, sigmaSpace=2.0)
        self.ellipMask()
    def gTransform(self):
##        #Mittepunkt zw. die Augen
##        ex = (self.lefteye[0]+self.righteye[0])*0.5
##        ey = (self.lefteye[1]+self.righteye[1])*0.5
##        eyeCenter = (ex,ey)
##        #Winkel der Augen
##        dx = (self.righteye[0] - self.lefteye[0])
##        dy = (self.righteye[1] - self.lefteye[1])
##        l = math.sqrt(dx*dx+dy*dy)
##        angle = math.atan2(dy,dx)*180.0/math.pi
##        #Konstante von der Auge, die man braucht
##        LEFT_EYE_X=0.16
##        RIGHT_EYE_X = (1.0-0.16)
##        FACE_WIDTH = 70
##        FACE_HEIGHT = FACE_WIDTH
##        desiredLen = (RIGHT_EYE_X - 0.16)
##        scale = desiredLen*FACE_WIDTH/l
        pass
    def allHistEqual(self):
        pass
    def ellipMask(self):
        pass
