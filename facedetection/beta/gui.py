# -*- coding: utf-8 -*-
"""
PyQt-GUI-Modul, Benutzeroberflaeche der gesamten Anwendung sowie noetige
Video-Bild-Konvertierungen für PyQt Support.
 
"""
import sys

from PyQt4 import Qt, QtCore, QtGui
import numpy as np
import cv2

import controller as c
import log as l

class Video():
    """Klasse zum konvertieren des Videobilds"""
    def __init__(self, webcam, face_id=None, save_face=False, recognize_face=False, recognize_face_stopped=False):
        self.webcam = webcam
        self.face_id = face_id
        self.save_face = save_face
        self.recognize_face = recognize_face
        self.stop = recognize_face_stopped
        self.current_frame=np.ndarray([])
        self.controller = c.Controller()

    def capture_next_frame(self):
        """Liest naechsten Frame der Kamera und wandelt es von BGR zu RGB und startet die Gesichtserkennung"""
        success, read_frame=self.webcam.read()
        if success:              
            read_frame = cv2.cvtColor(read_frame, cv2.COLOR_BGR2RGB)
            self.current_frame = self.controller.frame_to_face(read_frame,self.face_id,self.save_face, self.recognize_face)            
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
        
class GUI(QtGui.QMainWindow):
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
        Qt.QObject.connect(self.id_text, Qt.SIGNAL('textChanged(const QString&)'), self.on_input_id)
        boxLayout.addWidget(self.id_text)
        
        # Training-Set-Aufnehmen-Button
        self.training_set_button = QtGui.QPushButton("Training-Set", self)
        self.training_set_button.setCheckable(True)
        boxLayout.addWidget(self.training_set_button)
        Qt.QObject.connect(self.training_set_button, Qt.SIGNAL('clicked()'), self.training_set_clicked)
                        
        # Wer-Bin-Ich-Button
        self.who_am_i_button = QtGui.QPushButton("Wer-Bin-Ich?", self)
        self.who_am_i_button.setCheckable(True)
        boxLayout.addWidget(self.who_am_i_button)
        Qt.QObject.connect(self.who_am_i_button, Qt.SIGNAL('clicked()'), self.who_i_clicked)
        #self.who_am_i_button.clicked.connect(self.who_i_clicked)
        
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

    def on_input_id(self, text):
        """Wird automatisch bei Eingabe ins Textfeld aufgerufen"""
        pass
        
    def play(self):
        """Zum stetig wiederholtem Aufrufen um Kamerabild zu aktualisieren"""
        try:
            # naechsten Frame holen und diesen konvertiert als Pixmap in GUI anzeigen
            self.video.capture_next_frame()            
            self.video_label.setPixmap(self.video.convert_frame())            
        except TypeError:
            print "GUI.play(): Kein Bild von Kamera oder Bild-Konvertierungsproblem! Eventuell Laeuft die Anwendung noch!?"
    
    # Button-Callback-Funktionen
    def training_set_clicked(self):
        l.log('Training-Set: %s' % self.training_set_button.isChecked())
        if self.training_set_button.isChecked():
            self.training_set_button.setText("Anhalten")
            self.video.save_face = True
            self.video.face_id = self.id_text.text()
        else: # not button.isChecked()
            self.training_set_button.setText("Training-Set")
            self.video.save_face = False
        
    def who_i_clicked(self):
        if self.who_am_i_button.isChecked():
            self.who_am_i_button.setText("Anhalten")
            self.video.recognize_face = True
            self.video.face_id = self.id_text.text()
        else: # not button.isChecked()
            self.who_am_i_button.setText("Who I am")
            self.video.recognize_face = False
            self.video.stop = True

            