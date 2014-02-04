# -*- coding: utf-8 -*-
"""
Modul um GUI Eingaben korrekt zu verarbeiten und entsprechende Prozeduren anzustossen.

"""
from fdetection import FaceDetector as fd
import frecognize as fr
import log as l

class Controller(object):
    """Steuert Facedetector und Facerecognizer Objekte je nach Eingaben in der GUI."""

    def __init__(self):
        """Instanziiert immer ein Facedetector- und ein FaceRecognizer-Objekt."""
        # Facedetekor-Objekt
        self.detect = fd()
        self.fr = fr.FaceRecognizer()
        self.trigger_rec = False
        self.trigger_save = False
    
    def get_percentage(self, sum, part):
        """Berrechnung des Prozentualen Anteils"""
        return 100 * part/float(sum)
    
    # TODO: ggf raus vor abgabe
    def print_stat(self):
        """Erkennungs-Statistik-Ausgabe auf Konsole"""
        s = ['\n----------------------------------------------']
        for k, v in self.fr.ts.ids.items():            
            s.append('Predicts: ID: %s    %sx => ' % (k, len(v[1])), )
        s.append('----------------------------------------------\n')
        l.log('\n'.join(s))
        
    def frame_to_face(self, frame, face_id, save_face, recognize_face):
        """Verarbeitet pro Frame die Informationen der gedrueckten Buttons und gibt bearbeiteten Frame."""
        self.frame, self.face = self.detect.detectFace(frame)
        
        if self.face is not None:
            if save_face:
                self.trigger_save = True
                # Training-Set erstellung
                self.detect.acceptNewFace(self.face, face_id)
            elif self.trigger_save: # Nur einmal nach Beenden der Training-Set Aufnahme
                self.trigger_save = False
                l.log('Habe Training-Set beendet!!!!!!!!!')
                # TODO: Lernen der neu aufgenommenen Bilder hier starten
            if recognize_face:
                self.trigger_rec = True
                # Facedetection
                predicted = self.fr.predict(self.face)
                self.fr.ts.ids[str(predicted)][1].append(predicted)
                print "\nExpects:", face_id
                print "It predicts the id:",  predicted
            elif self.trigger_rec: # nur einmal bei Beenden der Gesichtserkennung
                self.trigger_rec = False
                self.print_stat()
                # Leeren der gemerkten predicts, damit bei nochmaligem Start die liste Leer ist
                for k, v in self.fr.ts.ids.items():
                    v[1] = []
        return self.frame
    