# -*- coding: utf-8 -*-
'''
Modul um GUI Eingaben korrekt an Controller-Objekte weiter zu geben.
'''
from fdetection import FaceDetector as fd
import frecognize as fr

class Controller(object):
    """Steuert Facedetector und Facerecognizer Objekte je nach Eingaben in der GUI."""

    def __init__(self):
        """Instanziiert immer ein Facedetector- und ein FaceRecognizer-Objekt."""
        # Facedetekor-Objekt
        self.detect = fd()
        self.fr = fr.FaceRecognizer()
        
    def frame_to_face(self, frame, face_id, save_face, recognize_face):
        """Verarbeitet Informationen der gedrueckten Buttons"""
        self.frame, self.face = self.detect.detectFace(frame)
        if self.face is not None:
            if save_face:
                self.detect.acceptNewFace(self.face, face_id)
            if recognize_face:
                i = self.fr.predict(self.face)
                print "Expects:", face_id,
                print "It predicts the id:", i
        return self.frame
    