'''
Created on 24.01.2014

@author: ptreb001
'''
import os
import errno

from PyQt4 import QtGui

class TrainingSet(object):
    """Ein Trainings-Set d.h. eine Person mit ihren Gesichtern und ID."""
    
    def __init__(self, id, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_', name=''):      
        self.ID = id
        self.path = os.path.expanduser(os.path.join(path,str(id)))
        self.counter = 0
        self.name = name
        self.images = {}
        print ' path ', self.path
        # TOD0: automatisch Ordnerstruktur anlegen falls sie noch nicht existiert
        self.init_folder_structure()
    
    def get_image_name(self):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        return '%s_%s.jpg' % (self.ID, self.counter)
    
    def create_folder(self, path, name=''):
        """Legt einen neuen Ordner im Dateisystem an: path/name."""
        # check ob Ordner bereits existiert
        path = os.path.join(path, name)
        print path
        if not os.path.exists(path):
            print 'path ', 'wird angelegt...'
            try:
                os.makedirs(path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    print 'ignoriere os.error'
        else:
            print path, ' bereits vorhannden'        
        
    def init_folder_structure(self):
        """Legt Ordnerstrukur an"""
        self.create_folder(self.path)

    def add_face(self, face):                
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (self.ID) hinzu"""
        folder = os.path.join(self.path)
        print folder, ' folder checken'
        
        if os.path.exists(folder):
            print 'Okay, ID existiert'
            print type(face)
            assert(isinstance(face, QtGui.QPixmap))
            face.save(os.path.join(self.path, self.get_image_name()))
            self.counter += 1
        else:
            print 'Fehler '
        
