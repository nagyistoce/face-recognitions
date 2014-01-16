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
    """Klasse zum konver"""
    def __init__(self,capture):
        self.capture = capture
        self.current_frame=np.ndarray([])
 
    def capture_next_frame(self):
        """Liest naechsten Frame der Kamera und wandelt es von BGR zu RGB"""
        ret, read_frame=self.capture.read()
        if ret:
            self.current_frame = cv2.cvtColor(read_frame, cv2.COLOR_BGR2RGB)
 
    def convert_frame(self):
        """Konvertiert Bild in ein von QtGUI akzeptiertes Format"""
        try:            
            height, width = self.current_frame.shape[:2]
            image = QtGui.QImage(self.current_frame, width, height,
                                 QtGui.QImage.Format_RGB888)
            image = QtGui.QPixmap.fromImage(image)
            #self.previous_frame = self.current_frame
            return image
        except:
            print "Fehler beim konvertieren des Kamerabildes:", sys.exc_info()[0]
            raise

        
class Gui(QtGui.QMainWindow):
    """PyQt GUI fuer Button-Support und effiziente Kameraansteuerung."""
    
    def __init__(self, *args):        
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
        Qt.QObject.connect(self.quit_button, Qt.SIGNAL('clicked()'), Qt.qApp,
                           Qt.SLOT('quit()'))
        boxLayout.addWidget(self.quit_button)
        
        # Video-Bild umwandeln und updaten
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
 
    def play(self):
        """Zum stetig wiederholtem Aufrufen um Kamerabild zu aktualisieren"""
        try:
            # naechsten Frame holen und diesen konvertiert als Pixmap in GUI anzeigen
            self.video.capture_next_frame()            
            self.video_label.setPixmap(self.video.convert_frame())
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