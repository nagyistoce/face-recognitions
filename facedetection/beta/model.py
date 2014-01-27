'''
Created on 24.01.2014

@author: ptreb001
'''
import os
import errno
import sys

from PyQt4 import QtGui
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
    
    def get_image_name(self, id):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        return '%s_%s.jpg' % (str(id), self.counter)
    
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

    def add_face(self, face, id):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""     
        folder = os.path.join(self.path, str(id))
        
        if not os.path.exists(folder):
            self.create_folder(self.path, id)
        print 'Okay, ID existiert'
        cv2.imwrite(os.path.join(folder,self.get_image_name(id)), face)
        #assert(isinstance(face, QtGui.QPixmap))
        #face.save(os.path.join(self.path, self.get_image_name()))
        self.counter += 1
    
    def get_faces(self):
        ids = 0
        face_images,face_ids = [],[]
        for dirname, dirnames,filenames in os.walk(self.path):
            for subdirname in dirnames:
                id_path = os.path.join(dirname, subdirname)
                for face_image in os.listdir(id_path):
                    try:
                        im = cv2.imread(os.path.join(id_path,face_image), cv2.IMREAD_GRAYSCALE)
                        face_images.append(np.asarray(im,dtype = np.uint8))
                        face_ids.append(ids)
                    except IOError,(errno,strerror):
                        print "I/O error{0}: {1}".format(errno,strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                ids = ids +1
        return [face_images,face_ids]
            
            
        
