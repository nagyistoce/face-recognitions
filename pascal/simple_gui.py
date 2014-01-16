'''
Created on 16.01.2014

@author: ptreb001
'''
from PyQt4 import QtCore
from PyQt4 import Qt
from PyQt4 import QtGui
# from PyQt4 import QtOpenGL
import sys
import numpy as np
import cv2

class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.array([])
 
    def captureNextFrame(self):
        """capture frame and reverse RBG BGR and return opencv image"""
        ret, readFrame=self.capture.read()
        if(ret==True):
            print 'lese neues bild...'
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """converts frame to format suitable for QtGui"""
        try:
            height,width=self.currentFrame.shape[:2]
            print 'shape ', height, width
            img=QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            img=QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None
        
class Gui(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        
        # selbst als MainWindow setzen
        widget = QtGui.QWidget(self)
        self.setCentralWidget(widget)
        
        #Layout
        boxLayout = QtGui.QVBoxLayout()    
        widget.setLayout(boxLayout)
        
        # QLabel als Videoframe Container
        self.label = QtGui.QLabel("Ein QLabel")
        boxLayout.addWidget(self.label)

        
        # Video-Instanz um Videobild zu bearbeiten
        self.video = Video(cv2.VideoCapture(0))
        print type(self.video)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
 
    def play(self):
        try:
            self.video.captureNextFrame()
            self.label.setPixmap(self.video.convertFrame())
            
            # Bild in Qlabel anzeigen
#             self.ui.videoFrame.setPixmap(
#                 self.video.convertFrame())
#             self.ui.videoFrame.setScaledContents(True)
        except TypeError:
            print "No frame"
 
def main(args):
    app = QtGui.QApplication(args)
    ex = Gui()
    ex.show()
    return app.exec_()
    
    
class ToggleWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.setCentralWidget(self)
        self.adjustSize()
        
def main2(args):
    app = QtGui.QApplication(args)
    widget = QtGui.QWidget()    
    boxLayout = QtGui.QVBoxLayout()    
    widget.setLayout(boxLayout)
    label = QtGui.QLabel("Nach Ein QLabel")
    boxLayout.addWidget(label)
    widget.show()
    return app.exec_()

if __name__ == '__main__':
    # huebsch gemacht endlosschleifen aufruf app.exec_ als returnwert
    sys.exit(main(sys.argv))