'''
Created on 24.01.2014

@author: ptreb001
'''
import os
import errno

from PyQt4 import QtGui
import cv2

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
        
            
            
            
        
