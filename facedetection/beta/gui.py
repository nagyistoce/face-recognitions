# -*- coding: utf-8 -*-
'''
PyQt-GUI-Modul, Benutzeroberflaeche der gesamten Anwendung sowie noetige
Video-Bild-Konvertierungen für PyQt Support.
 

'''
import sys
import numpy as np
import cv2

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

import fdetection as fd

class Video():
    """Klasse zum konvertieren des Videobilds"""
    def __init__(self, webcam, face_id=None, save_face=False):
        self.webcam = webcam
        self.face_id = face_id
        self.save_face = save_face
        self.current_frame=np.ndarray([])
        
        # Facedetekor-Objekt
        self.detect = fd.FaceDetector()
 
    def capture_next_frame(self):
        """Liest naechsten Frame der Kamera und wandelt es von BGR zu RGB und startet die Gesichtserkennung"""
        success, read_frame=self.webcam.read()
        if success:              
            read_frame = cv2.cvtColor(read_frame, cv2.COLOR_BGR2RGB)
            self.current_frame = self.detect.detectFace(read_frame, self.face_id,self.save_face)
            
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
            print "Fehler beim konvertieren des Kamerabildes: ", sys.exc_info()[0]
            raise

        
class Gui(QtGui.QMainWindow):
    """PyQt GUI fuer Button-Support und effiziente Kameraansteuerung."""
    
    def __init__(self, *args):
        """Buttons und ein Label fuer das Videobild sowie ein Timer zum 
        periodischen Ausfuehren der play() Methode
        
        """      
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

        # ID Textfeld
        self.id_text = QtGui.QLineEdit("ID", self)
        Qt.QObject.connect(self.id_text, Qt.SIGNAL('textChanged(const QString&)'), self.do_training_set)
        boxLayout.addWidget(self.id_text)
        
        # Training-Set-Aufnehmen-Button
        self.training_set_button = QtGui.QPushButton("Training-Set", self)
        self.training_set_button.setCheckable(True)
        boxLayout.addWidget(self.training_set_button)
        self.training_set_button.clicked.connect(self.training_set_clicked)
        Qt.QObject.connect(self.training_set_button, Qt.SIGNAL('clicked()'), self.training_set_clicked)
                        
        # Wer-Bin-Ich-Button
        self.who_am_i_button = QtGui.QPushButton("Wer-Bin-Ich?", self)
        boxLayout.addWidget(self.who_am_i_button)
        self.who_am_i_button.clicked.connect(self.who_i_clicked)
        
        
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
        self.webcam = cv2.VideoCapture(0)
        if self.webcam.isOpened(): 
            self.video = Video(self.webcam)
            self._timer = QtCore.QTimer(self)
            self._timer.timeout.connect(self.play)
            self._timer.start(27)
            self.update()
        else:
            self.test = False
            print "Web-Cam nicht angeschlossen"

    
    def do_training_set(self, text):
        print 'do_training_set(): ', text
        
    def play(self):
        """Zum stetig wiederholtem Aufrufen um Kamerabild zu aktualisieren"""
        try:
            # naechsten Frame holen und diesen konvertiert als Pixmap in GUI anzeigen
            self.video.capture_next_frame()            
            self.video_label.setPixmap(self.video.convert_frame())            
        except TypeError:
            print "Kein Bild von Kamera oder Bild-Konvertierungsproblem!"
            
    def training_set_clicked(self):
        if self.training_set_button.isChecked():
            self.training_set_button.setText("Anhalten")
            print "Foto Machen"
            # shost is a QString object
            print 'der TEXT ', self.id_text
            self.video.save_face = True
            self.video.face_id = self.id_text.text()
        else:
            self.training_set_button.setText("Training-Set")
        
        
    def who_i_clicked(self):
        print "Who i am"

 
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