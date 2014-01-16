import fdetection as fd
import cv2

class WebcamController(object):
    #Webcam Zugriff
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
    #oeffnet Webcam Fenster, stoesst Gesichtserkennung an
    def startWebcam(self):
        cv2.namedWindow("preview")
        if self.webcam.isOpened(): # try to get the first frame
            self.test, self.frame = self.webcam.read()
            self.detect = fd.FaceDetector()
        else:
            self.test = False
        
        while self.test:
            img = self.detect.detectFace(self.frame)
            cv2.imshow("preview", img)

            # get next frame
            self.test, self.frame = self.webcam.read()

            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC
                break
        self.webcam.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    start = WebcamController()
    start.startWebcam()
