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

    Das Dictionary id_infos_dict hat als Schluessel die ID und zugehoerige Informationen als Liste in den Values
    id_infos_dict {'id':['username', counter_predicted], ... }
    values-Liste enthaelt: 
    - Benutzername
    - Counter wie oft diese ID predict wurde im aktuellen Suchvorgang
    
    """

    def __init__(self):
        """Instanziiert immer ein Facedetector- und ein FaceRecognizer-Objekt."""
        self.t_sets = db.TrainingSets()
        # dictionary mit Informationen zu den Personen
        known_ids = {'0' : 'Julia',
                     '1' : 'Deniz',
                     '2' : 'Pascal'
                     }
        # {id : ['username', predict_counter], ... }
        self.id_infos_dict = self.t_sets.get_id_infos_dict(known_ids)
        # Facedetekor-Objekt
        self.detect = fd()                
        self.fr = fr.FaceRecognizer()
        try:
            [face_images, face_ids] = self.t_sets.get_all_faces()
        except:
            log.exception("Es konnten keine Bilder geladen werden")
            raise
        if len(face_images) != 0:
            self.fr.trainFisherFaces(face_ids, face_images)
        else:
            log.info("Training Set ist leer oder Bilder können nicht geladen werden")
        self.trigger_rec = False
        self.trigger_save = False

        self.observer = []
        self.predict = []
    
    # Observer Pattern        
    def get_predict(self):
        """Gibt ID der Erkannten Person zurueck"""
        return self.predict
    def register_observer(self, obj):
        """Wird zum registrieren eines Observers verwendet"""
        log.debug('registriere %s an Controller', obj)
        self.observer.append(obj)
    def notify_observer(self):
        """Ruft update() aller zu benachritigen Objekte auf"""
        for obj in self.observer:
            obj.update()
            
    def get_percentage(self, total, part):
        """Berrechnung des Prozentualen Anteils von part an total."""
        percent = 0.0
        try:
            percent = 100 * part/float(total)
        except ZeroDivisionError:
            log.info('Es wurde in diesem Durchlauf KEIN Gesicht Erkannt!\nEventuell den Schwellwert ueberpruefen. total = %s', total)
        except:
            log.exception('Unerwarteter Fehler beim Berrechnen des Prozentanteils.')
        return percent
    
    def print_stat(self):
        """Erkennungs-Statistik-Ausgabe auf Konsole"""
#         print 'das hier ', [n[1] for n in self.id_infos_dict.values()]
        
#         total = sum([n[1] for n in self.id_infos_dict.values()])
        print self.id_infos_dict

        total = sum([ele['counter'] for ele in self.id_infos_dict.values()])
        s = ['\n----------------------------------------------']
        for k, v in sorted(self.id_infos_dict.items()):  
#             count = v[1]
            count = v['counter']
            percentage = self.get_percentage(total, count)
            s.append('Predicts: ID: %s    %sx => %s%%' % (k, count, percentage))
        s.append('total: %s' %total)
        s.append('----------------------------------------------\n')
        log.info('\n'.join(s))

    # Diese Methode schlank halten, da sie pro Frame aufgerufen wird!        
    def frame_to_face(self, frame, face_id, face_name, save_face, recognize_face):
        """Verarbeitet pro Frame die Informationen der gedrueckten Buttons und gibt bearbeiteten Frame zurueck."""
        self.frame, self.face = self.detect.detectFace(frame)
        if self.face is not None:
            if save_face:
                # Training-Set erstellung
                self.trigger_save = True
                self.detect.acceptNewFace(self.face, face_id, face_name)
            elif self.trigger_save:
                # Nur einmal nach Beenden der Training-Set Aufnahme
                self.trigger_save = False
                log.info('Beende Training-Set...')
                log.info('Trainiere Fisher Faces mit neue Gesichter...')
                [face_images, face_ids]=self.t_sets.get_all_faces()
                if len(face_images)!=0:
                    self.fr.trainFisherFaces(face_ids, face_images)
                # TODO: Lernen der neu aufgenommenen Bilder hier starten
            elif recognize_face:                
                self.trigger_rec = True
                # Facedetection
                predicted_face = self.fr.predict(self.face)
                if predicted_face >= 0:
                    self.predict = [predicted_face]
                    try:
                        self.id_infos_dict[str(predicted_face)]['counter'] += 1
#                         self.id_infos_dict[str(predicted_face)][1] += 1
                    except:
                        log.exception('Fehler beim Erhoehen des predict-Zaehlers der ID: %s', str(predicted_face))
                    self.notify_observer()
            elif self.trigger_rec: 
                # nur einmal bei Beenden der Gesichtserkennung
                log.info('Beende Gesichtserkennung...')
                self.trigger_rec = False
                self.print_stat()
                # Leeren der gemerkten predicts, damit bei nochmaligem Start die liste Leer ist
                for k, v in self.id_infos_dict.items():
                    v[1] = 0
        return self.frame
    