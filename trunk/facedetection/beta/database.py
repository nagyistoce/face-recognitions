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
    def __init__(self, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_', name=''):

        
        self.path = os.path.expanduser(path)
        self.name = name
        self.images = {}
        self.init_folder_structure()

    def get_id_dict(self):
        """Gibt alle IDs als Dictionary mit ID als Key zurueck"""

    # TODO: testen ob das update() funktioniert
    def get_id_infos_dict(self, **known_ids):
        """Gibt Dictionary mit IDs als Key zurueck, known_ids werden hinzugefuegt. 
        
        return -> id_infos_dict {id : ['username', predict_counter], ... }
        
        """
        join = os.path.join
        dic = {}
        lis = sorted([f for f in os.listdir(self.path) 
                      if os.path.isdir(join(self.path,f)) and f.isdigit()])
        for i in lis:
            dic[i] = ['name', 0]
        log.debug('Alle IDs auf Platte: %s', map(int,lis))
        if known_ids:
            dic.update(known_ids)
            log.debug('Das id_infos_dict nach update(known_ids): %s ', dic)
        return dic

    def get_image_name(self, face_id):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        return '%s_%s.png' % (str(face_id), now)
    
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
    
    def init_folder_structure(self):
        """Legt Ordnerstrukur an"""
        self.create_folder(self.path)
    
    def bilder_is_empty(self):
        """Return -> True wenn in keinem der ID-Ordner ein Bild liegt"""
#         self.bild = True   
        log.debug('in bilder_is_empty()')
        join = os.path.join
        lis = ['.jpg', '.JPG', '.png', '.PNG']
        for folder in [f for f in os.listdir(self.path) if os.path.isdir(join(self.path,f))]:
            folder = os.path.join(self.path, folder)
            for dat in os.listdir(folder):
                if dat[-4:] in lis:
                    return False
#                 print 'datei ', dat
#                 if dat_endung.endswith('.jpg') or dat.endswith('.JPG') or dat_endung.endswith('.png') or dat.endswith('.PNG'):
#                     self.bild = False
        return True
    
    def trainings_set_is_empty(self):
        """Return -> True wenn der Wurzelordner KEIN Verzeichnis enthaelt"""
        log.debug('in trainingsset_is_empty()')     
        dirs = [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path,d))]
        is_empty = [] == dirs        
        return is_empty
        #for d in dirs:
            #path = os.path.join(self.path, d)
            #print '%s isdir: %s' % (path, os.path.isdir(path))
            
    def save_face(self, face, face_id):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""     
        assert(isinstance(face, np.ndarray))
        folder = os.path.join(self.path, str(face_id))
        full_path = os.path.join(folder,self.get_image_name(face_id))
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
        for img in [f for f in os.listdir(id_path) if os.path.isfile(join(id_path, f))]:
            img_path = os.path.join(id_path, img)
            try:                
                im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                face_images.append(np.asarray(im, dtype = np.uint8))
                num_imgs +=1
            except IOError as e:
                log.exception("I/O error{0}: {1}".format(e.errno, e.strerror))
            except:
                log.exception("Nichterwarteter Fehler: %s", sys.exc_info()[0])
                raise
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
    ts.bilder_is_empty()
#     ts.trainings_set_is_empty()
    
