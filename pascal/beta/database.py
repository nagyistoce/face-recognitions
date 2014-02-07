# -*- coding: utf-8 -*-
"""
Modul zur Verwaltung der Persistenten Daten.
Die Klasse TrainingSets stelt Werkzeug-Methoden bereit, sie ist kein Singleton und kann ueberall wo sie benoetigt wird neu instanziiert werden.

"""
import os
import errno
import sys
import datetime
import logging as log

import cv2, numpy as np

class TrainingSets(object):
    """Klasse die IO-Methoden bereit stellt fuer die Training-Sets.
    Sie haelt selbst keine Daten und dient nur als Werkzeug.
     
    """
    def __init__(self, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_'):
        self.path = os.path.expanduser(path)
        self.extensions = ['.jpg', '.JPG', '.png', '.PNG']
        self.images = {}
        self.init_folder_structure()

    def get_id_and_names(self):
        """Liest ID und Namen aus den gespeicherten Bildern heraus. 
        Nur verwenden wenn alle Bilder einheitlich mit ID_Name_ beginnen!
        Siehe get_image_name().
        
        return -> [('id', 'name1'), ('id2', 'name2'), ... ]
        
        """
        try:
            for dir in self.get_id_dirs():
                pics = [f for f in os.listdir(dir) if f[-4:] in self.extensions]                
                print 'nur bilder von %s dir:\n%s' % (dir, pics)
        except:
            log.exception('Training-Set-Pfad nicht vorhanden')
            
    def get_id_infos_dict(self, known_ids=None):
        """Gibt Dictionary mit IDs als Key zurueck, known_ids werden hinzugefuegt. 

        return -> id_infos_dict {id = {'username'='Pascal', 'count_predict'=0}, ... }
        
        """
        join = os.path.join
        dic = {}
        lis = sorted([f for f in os.listdir(self.path) 
                      if os.path.isdir(join(self.path,f)) and f.isdigit()])
        for i in lis:
#             dic[i] = ['name', 0]
            dic[i] = {'name' : 'user', 'counter' : 0}
        log.debug('Alle IDs von Platte: gelesen %s', map(int,lis))
        log.debug('das dict vor update merge %s', dic)
        # Uebergebene (ID,Name) Tuple in info_dict setzen
        if known_ids:
            try:                
                for tup in known_ids:
                    td = {'name':tup[1], 'count_predict':0}
                    dic[tup[0]] = td
                log.debug('Das id_infos_dict nach update(known_ids): %s ', dic)
            except:
                log.exception('Fehler beim hinzufugen bekannter IDs zum info_dictionary.')
        return dic

    def get_image_name(self, face_id, face_name):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck.
        
        return -> ID_Name_Datum_Uhrzeit.png
        
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        # Anfang muss ID_Name_ sein da dies in get_id_and_names() erwartet wird
        return '%s_%s_%s.png' % (str(face_id), face_name, now)
    
    def create_folder(self, path, face_id=''):
        """Legt einen neuen Ordner im Dateisystem an: path/name."""
        # check ob Ordner bereits existiert
        path = os.path.join(path, str(face_id))
        if not os.path.exists(path):
            log.info('%s wird angelegt...', path)
            try:
                os.makedirs(path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    log.debug('ignoriere bekanntes os.error errno.EEXIST: %s', e)
            except:
                log.exception('Unerwarteter Fehler beim Anlegen von %s', path)
    
    def init_folder_structure(self):
        """Legt Ordnerstrukur an"""
        self.create_folder(self.path)
    
    def get_id_dirs(self):
        """Gibt Verzeichnispfade aller aktuell vorhandenen IDs zurueck
        return -> ['path/toid1', 'path/toid2', ...]
        """
        dirs = []
        join = os.path.join
        try:
            for folder in [f for f in os.listdir(self.path) if os.path.isdir(join(self.path,f))]:
                dirs.append(join(self.path, folder))
#                 log.debug('alle id dirs %s', dirs)
        except:
            log.exception('Fehler beim Auslesen der ID-Verzeichnis-Pfade')
        return dirs
        
    def bilder_is_empty(self):
        """Return -> True wenn alle Ordner KEIN Bild enthalten"""
        log.debug('in bilder_is_empty()')
        join = os.path.join
        
        if self.trainings_set_is_empty()==False:
            for folder in [f for f in os.listdir(self.path) if os.path.isdir(join(self.path,f))]:
                folder = join(self.path, folder)
                for dat in os.listdir(folder):
                    if dat[-4:] in self.extensions:
                        return False
        return True
    
    def trainings_set_is_empty(self):
        """Return -> True wenn der Wurzelordner KEIN Verzeichnis enthaelt"""
        log.debug('in trainingsset_is_empty()')     
        try:
            print 'die dirs ', self.get_id_dirs()
#             dirs = [d for d in self.get_id_dirs() if os.path.isdir(os.path.join(self.path,d))]
            dirs = [d for d in self.get_id_dirs() if os.path.isdir(d)]
        except:
            log.exception('Fehler beim pruefen ob das Training-Set Wurzelverzeichnis leer ist.')
            raise
        is_empty = [] == dirs        
        return is_empty
            
    def save_face(self, face, face_id, face_name):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""     
        assert(isinstance(face, np.ndarray))
        folder = os.path.join(self.path, str(face_id))
        full_path = os.path.join(folder,self.get_image_name(face_id, face_name))
        if not os.path.exists(folder):
            self.create_folder(self.path, face_id)
        try:
            cv2.imwrite(full_path, face)

        except (IOError, Exception):
            log.exception("Fehler beim Abspeichern des Bildes: %s", full_path)
                
    def get_faces(self, id_path, face_images):
        """Liest alle Bilder einer bestimmten ID ein"""
        face_id = id_path.split(os.sep)[-1]
        num_imgs = 0
        join = os.path.join
        images = [f for f in os.listdir(id_path) 
             if os.path.isfile(join(id_path, f)) and f[-4:] in self.extensions
             ]
        for img in images:
            img_path = os.path.join(id_path, img)
            try:                         
                im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                face_images.append(np.asarray(im, dtype = np.uint8))
                num_imgs +=1
            except IOError as e:
                log.exception("I/O error{0}: {1}".format(e.errno, e.strerror))
            except TypeError as e:
                log.exception('Fehler beim einlesen der Datei %s.\n'
                              'Eventuell ist die Datei defekt.', img_path)     
            except:
                log.exception("Nicht erwarteter Fehler beim einlesen der Datei "
                            "%s", img_path)
        log.info('ID %s: %s Bilder eingelesen', face_id, num_imgs)
        return face_images, num_imgs
            
    def get_all_faces(self):
        """Einlesen der Gesichtsbilder von Platte mit zuordnung der jeweiligen ID durch 2 Listen."""
        face_images, face_ids = [], []
        for dirname, dirnames, filenames in os.walk(self.path):
            for subdirname in sorted(dirnames):
                if subdirname.isdigit():
                    face_id = int(subdirname)
                    id_path = os.path.join(dirname, str(face_id))
                    face_images, number = self.get_faces(id_path, face_images)
                    face_ids.extend([face_id] * number)
                else:
                    log.info('Ueberspringe den Ordner: %s da er keine gueltige ID darstellt.', subdirname)
        return face_images, face_ids
    
if __name__ == '__main__':
    log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    ts = TrainingSets()
    ts.get_id_and_names()
#     print 'ts empty ',ts.trainings_set_is_empty()
#     print 'bidler empty ', ts.bilder_is_empty()
# #     ts.trainings_set_is_empty()
    
