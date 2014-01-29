'''
Created on 24.01.2014

@author: ptreb001
'''
import os
import errno
import sys

import cv2, numpy as np

class TrainingSets(object):
    """Ein Trainings-Set d.h. eine Person mit ihren Gesichtern und ID."""
    
    def __init__(self, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_', name=''):
        self.path = os.path.expanduser(path)
        self.counter = 0
        self.name = name
        self.images = {}
        print ' path den ich bekomme ', self.path
        # TOD0: automatisch Ordnerstruktur anlegen falls sie noch nicht existiert
        self.init_folder_structure()
    
    def get_image_name(self, face_id):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        #.png damit die pixel values sich nicht ändern
        return '%s_%s.png' % (str(face_id), self.counter)
    
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
        else:
            print path, ' bereits vorhannden'        
    
    # todo raus
    def init_folder_structure(self):
        """Legt Ordnerstrukur an"""
        self.create_folder(self.path)

    def save_face(self, face, face_id):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""     
        assert(isinstance(face, np.ndarray))
        folder = os.path.join(self.path, str(face_id))
        
        if not os.path.exists(folder):
            self.create_folder(self.path, face_id)
        cv2.imwrite(os.path.join(folder,self.get_image_name(face_id)), face)
        self.counter += 1

    def get_faces(self, id_path):
        """Liest alle Bilder einer bestimmten ID ein"""
        id_path = os.path.join(self.path, id_path)
        face_images = []
        for img in os.listdir(id_path):
            try:
                img_path = os.path.join(id_path, img)
                im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                face_images.append(np.asarray(im, dtype = np.uint8))
            except IOError,(errno,strerror):
                print "I/O error{0}: {1}".format(errno, strerror)
            except:
                print "Unexpected error: ", sys.exc_info()[0]
                raise
        print 'Ich habe %s Bilder eingelesen' % len(face_images)
        return face_images, len(face_images)
            
    def get_all_faces(self):
        """Einlesen der Gesichtsbilder von Platte mit zuordnung der jeweiligen ID durch 2 Listen."""
        face_images, face_ids = [], []
        for dirname, dirnames, filenames in os.walk(self.path):
            for subdirname in dirnames:
                if subdirname != 'ID':
                    id_path = os.path.join(dirname, subdirname)
                    images, number = self.get_faces(id_path)
                    face_images.extend(images)
                    face_ids.extend([int(subdirname)] * number)
        return [face_images, face_ids]
    
#     def get_faces(self):
#         ids = 0
#         face_images,face_ids = [],[]
#         for dirname, dirnames,filenames in os.walk(self.path):
#             for subdirname in dirnames:
#                 id_path = os.path.join(dirname, subdirname)
#                 for face_image in os.listdir(id_path):
#                     try:
#                         im = cv2.imread(os.path.join(id_path,face_image), cv2.IMREAD_GRAYSCALE)
#                         face_images.append(np.asarray(im,dtype = np.uint8))
#                         face_ids.append(ids)
#                     except IOError,(errno,strerror):
#                         print "I/O error{0}: {1}".format(errno,strerror)
#                     except:
#                         print "Unexpected error:", sys.exc_info()[0]
#                         raise
#                 ids = ids +1
#         return [face_images,face_ids]
            
            
        
