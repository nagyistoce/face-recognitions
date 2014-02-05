# -*- coding: utf-8 -*-
"""
Modul um GUI Eingaben korrekt zu verarbeiten und entsprechende Prozeduren anzustossen.

"""
import logging as log
try:
    import cPickle as pickle
except ImportError:
    import pickle    
from fdetection import FaceDetector as fd
import frecognize as fr
import database as db

class Controller(object):
    """Steuert Facedetector und Facerecognizer Objekte je nach Eingaben in der GUI.
    Das Dictionary id_dict hat als Schluessel die ID und zugehoerige Informationen als Liste in den Values
    
    id_dict {'id':['username', counter_predicted], ... }
    values-Liste enthaelt: 
    - Benutzername
    - Counter wie oft diese ID predicted wurde im aktuellen Suchvorgang
    
    """

    def __init__(self):
        """Instanziiert immer ein Facedetector- und ein FaceRecognizer-Objekt."""
        # Facedetekor-Objekt
        self.detect = fd()
        self.fr = fr.FaceRecognizer()
        self.t_sets = db.TrainingSets()
        self.trigger_rec = False
        self.trigger_save = False
        # dictionary d{'id':[#_imgs, [predict, predict, ...], 'username', ...]}
        # ids enthaelt Informationen zu den IDs: Anzahl eingelesener Bilder, liste mit allen Predicts bei facedetection-Vorgang
        self.id_dict = self.t_sets.get_id_dict()
        
    def get_percentage(self, total, part):
        """Berrechnung des Prozentualen Anteils von part an total."""
        try:
            percent = 100 * part/float(total)
        except ZeroDivisionError, e:
            log.debug('Durch Null geteilt. Wenn kein Gesicht erkannt wurde kann es passieren. total = %s', total)
        except:
            log.exception('Unerwarteter Fehler beim Berrechnen des Prozentanteils.')
        return percent
    
    def print_stat(self):
        """Erkennungs-Statistik-Ausgabe auf Konsole"""
        total = sum([n[1] for n in self.id_dict.values()])
        s = ['\n----------------------------------------------']
        for k, v in sorted(self.id_dict.items()):  
            count = v[1]
            #percentage = 100 * count/float(total)
            s.append('Predicts: ID: %s    %sx => %s%%' % (k, count, self.get_percentage(total, count)))
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
                print 'it predicts: %s' % predicted
                if predicted > 0:
                    self.id_dict[str(predicted)][1] += 1
            elif self.trigger_rec: # nur einmal bei Beenden der Gesichtserkennung
                log.info('Beende Gesichtserkennung...')
                self.trigger_rec = False
                self.print_stat()
                # Leeren der gemerkten predicts, damit bei nochmaligem Start die liste Leer ist
                for k, v in self.id_dict.items():
                    v[1] = 0
        return self.frame
    