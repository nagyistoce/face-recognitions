# -*- coding: utf-8 -*-
"""
Modul um GUI Eingaben korrekt zu verarbeiten und entsprechende Prozeduren anzustossen.

"""
import logging as log

from fdetection import FaceDetector as fd
import frecognize as fr

class Controller(object):
    """Steuert Facedetector und Facerecognizer Objekte je nach Eingaben in der GUI."""

    def __init__(self):
        """Instanziiert immer ein Facedetector- und ein FaceRecognizer-Objekt."""
        # Facedetekor-Objekt
        self.detect = fd()
        self.fr = fr.FaceRecognizer()
        self.trigger_rec = False
        self.trigger_save = False
    
    def get_percentage(self, total, part):
        """Berrechnung des Prozentualen Anteils von part an total."""
        return 100 * part/float(total)
    
    # TODO: ggf raus vor abgabe
    def print_stat(self):
        """Erkennungs-Statistik-Ausgabe auf Konsole"""
        total = sum([len(v[1]) for v in self.fr.ts.ids.values()])
        s = ['\n----------------------------------------------']
        for k, v in self.fr.ts.ids.items():  
            length = len(v[1])
            #percentage = 100 * length/float(total)
            s.append('Predicts: ID: %s    %sx => %s%%' % (k, length, self.get_percentage(total, length)))
        s.append('total: %s' %total)
        s.append('----------------------------------------------\n')
        log.info('\n'.join(s))
        
    def frame_to_face(self, frame, face_id, save_face, recognize_face):
        """Verarbeitet pro Frame die Informationen der gedrueckten Buttons und gibt bearbeiteten Frame zurueck."""
        self.frame, self.face = self.detect.detectFace(frame)
        if self.face is not None:
            if save_face:
                # Training-Set erstellung
                self.trigger_save = True
                self.detect.acceptNewFace(self.face, face_id)
            elif self.trigger_save: # Nur einmal nach Beenden der Training-Set Aufnahme
                self.trigger_save = False
                log.info('Habe Training-Set beendet!')
                # TODO: Lernen der neu aufgenommenen Bilder hier starten
            elif recognize_face:
                self.trigger_rec = True
                # Facedetection
                predicted = self.fr.predict(self.face)                
                self.fr.ts.ids[str(predicted)][1].append(predicted)
#                 print "Expects: %s It predicts the id: %s" % (face_id, predicted)
            elif self.trigger_rec: # nur einmal bei Beenden der Gesichtserkennung
                log.info('Beende Gesichtserkennung...')
                self.trigger_rec = False
                self.print_stat()
                # Leeren der gemerkten predicts, damit bei nochmaligem Start die liste Leer ist
                for k, v in self.fr.ts.ids.items():
                    v[1] = []
        return self.frame
    