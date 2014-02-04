# -*- coding: utf-8 -*-
'''
Created on 24.01.2014

@author: ptreb001
'''
import os
import errno
import sys
import datetime

import cv2, numpy as np
import logging as log

class TrainingSets(object):
    """Ein Trainings-Set d.h. eine Person mit ihren Gesichtern und ID."""
    
    def __init__(self, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_', name=''):
        # dictionary d{'id':[#_imgs, [predict, predict, ...], 'username', ...]}
        # ids enthaelt Informationen zu den IDs: Anzahl eingelesener Bilder, liste mit allen Predicts bei facedetection-Vorgang
        self.ids = {} 
        self.path = os.path.expanduser(path)
        self.name = name
        self.images = {}
        # TOD0: automatisch Ordnerstruktur anlegen falls sie noch nicht existiert
        self.init_folder_structure()
    
    def get_image_name(self, face_id):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        return '%s_%s.png' % (str(face_id), now)
    
    def create_folder(self, path, face_id=''):
        """Legt einen neuen Ordner im Dateisystem an: path/name."""
        # check ob Ordner bereits existiert
        path = os.path.join(path, str(face_id))
        if not os.path.exists(path):
            print path , 'wird angelegt...'
            try:
                os.makedirs(path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    print 'ignoriere os.error'
    
    # TODO: aufraeumen, einzeiler Funktion raus
    def init_folder_structure(self):
        """Legt Ordnerstrukur an"""
        self.create_folder(self.path)

    def save_face(self, face, face_id):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""     
        assert(isinstance(face, np.ndarray))
        folder = os.path.join(self.path, str(face_id))
        
        if not os.path.exists(folder):
            self.create_folder(self.path, face_id)
        try:
            cv2.imwrite(os.path.join(folder,self.get_image_name(face_id)), face)
        except IOError as detail:
            print "Fehler beim Abspeichern des Bildes", detail
            
            
                
    def get_faces(self, id_path, face_images):
        """Liest alle Bilder einer bestimmten ID ein"""
        id = id_path.split(os.sep)[-1]
        num_imgs = 0
        for img in os.listdir(id_path):
            try:
                img_path = os.path.join(id_path, img)
                im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                face_images.append(np.asarray(im, dtype = np.uint8))
                num_imgs +=1
            except IOError,(errno,strerror):
                print "I/O error{0}: {1}".format(errno, strerror)
            except:
                print "Unexpected error: ", sys.exc_info()[0]
                raise
        log.info('ID: %s %s Bilder eingelesen', id, num_imgs)
        self.ids[str(id)] = [num_imgs, []]
        return face_images, num_imgs
            
    def get_all_faces(self):
        """Einlesen der Gesichtsbilder von Platte mit zuordnung der jeweiligen ID durch 2 Listen."""
        face_images, face_ids = [], []
        for dirname, dirnames, filenames in os.walk(self.path):
            for subdirname in sorted(dirnames):
                if subdirname != 'ID':
                    id_path = os.path.join(dirname, subdirname)
                    face_images, number = self.get_faces(id_path, face_images)
                    face_ids.extend([int(subdirname)] * number)
        return face_images, face_ids
    
if __name__ == '__main__':
    ts = TrainingSets()
    
