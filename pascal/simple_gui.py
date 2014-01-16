#-*- coding: utf-8 -*-
'''
Created on 16.01.2014

@author: ptreb001

'''
import sys

import numpy as np
import cv2

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.ndarray([])
 
    def captureNextFrame(self):
        """capture frame and reverse RBG BGR and return opencv image"""
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """converts frame to format suitable for QtGui"""
        try:
            height,width=self.currentFrame.shape[:2]
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
        """PyQt GUI fuer Button-Support und effiziente Kameraansteuerung."""
        QtGui.QWidget.__init__(self, *args)
        # selbst als Vater und Hauptwidget setzen 
        widget = QtGui.QWidget(self)
        self.setCentralWidget(widget)
        # vertikales Layout setzen
        boxLayout = QtGui.QVBoxLayout()    
        widget.setLayout(boxLayout)
        # QLabel als Videoframe Container
        self.video_label = QtGui.QLabel("Videobild")
        boxLayout.addWidget(self.video_label)

        # Foto-Button
        self.foto_button = QtGui.QPushButton("Foto", self)
        boxLayout.addWidget(self.foto_button)
        # Wer-Bin-Ich-Button
        self.who_am_i_button = QtGui.QPushButton("Wer-Bin-Ich?", self)
        boxLayout.addWidget(self.who_am_i_button)
        # Beenden-Button        
        self.quit_button = QtGui.QPushButton("Ende", self)
        boxLayout.addWidget(self.quit_button)
        palette = QtGui.QPalette()
        palette.setColor(self.quit_button.foregroundRole(),Qt.QColor("red"))
        self.quit_button.setPalette(palette)
        Qt.QObject.connect(self.quit_button,
                           Qt.SIGNAL('clicked()'),
                           Qt.qApp,
                           Qt.SLOT('quit()')
                           )
        boxLayout.addWidget(self.quit_button)
        
        # Video-Bild umwandeln und updaten
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
 
    def play(self):
        try:
            self.video.captureNextFrame()
            self.video_label.setPixmap(self.video.convertFrame())
        except TypeError:
            print "No frame"
 
def main(args):
    """Hauptfenster, Hauptanwendung Initialisierung und Schliessen Signal anbinden""" 
    app = QtGui.QApplication(args)
    win = Gui()
    win.show()
    app.connect(app,                             # Sender-Widget
                Qt.SIGNAL('lastWindowClosed()'), # Signal
                app,                             # Empfaenger
                Qt.SLOT('quit()')                # aktivierter Slot
            )
    return app.exec_()
    
if __name__ == '__main__':
    # Endlosschleifen aufruf app.exec_ als returnwert
    sys.exit(main(sys.argv))