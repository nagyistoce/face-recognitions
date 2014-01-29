'''
Verwaltung der Persistenten Daten und Programmzustaende.

'''
import os
import errno
import sys
import logging
import time

import cv2, numpy as np
import hashlib
import binascii 

class TrainingSets(object):
    """Verwaltung der TrainingSets (vorab gespeicherte Gesichtsbilder) der Personen und ihrer IDs."""
    
    def __init__(self, path='~/Dropbox/FACERECOGNITION/_TRAINING_SETS_'):
        self.path = os.path.expanduser(path)
        self.counter = 0
        self.images = {}
        print 'Wurzelpfad der TrainingSets: ', self.path
        # Logging
        self.log = time.strftime('%Y-%m-%d_%H-%M', time.gmtime()) + '.log'
#         logging.basicConfig(filename=self.log,level=logging.INFO)
        logging.basicConfig(filename=os.path.join(self.path,self.log), level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('START ------------------------------------------')
        print self.log
        self.init_folder_structure()
    
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
        image_name = self.get_image_name(face_id, face)
        cv2.imwrite(os.path.join(folder, image_name), face)
        self.counter += 1
    
    def get_image_name(self, face_id, face):
        """Gibt den Bildnamen fuer ein neu zu speicherndes Gesicht zurueck"""
        assert(isinstance(face, np.ndarray))
        name = '%s_%s.jpg' % (str(face_id), self.get_hash(face.tostring())) #self.counter)
        return name


    def get_faces(self, id_path):
        """Liest alle Bilder einer bestimmten ID ein"""
        id_path = os.path.join(self.path, id_path)
        print 'get_faces()'
        print 'id_path ', id_path
        
        face_images = []
        for img in os.listdir(id_path):
            try:
                im = cv2.imread(os.path.join(id_path, img), cv2.IMREAD_GRAYSCALE)
                hash_before = img.split('_')[1][:-4]
                hash_after = self.get_hash(im.tostring())
                print hash_before, ' vorher'
                print hash_after, ' nachher'
                print '--> ', hash_before == hash_after
                face_images.append(np.asarray(im, dtype = np.uint8))
            except IOError,(errno,strerror):
                print "I/O error{0}: {1}".format(errno, strerror)
            except:
                print "Unexpected error: ", sys.exc_info()[0]
                raise
        print 'Ich habe %s Bilder eingelesen' % len(face_images)
        

    
            
    # warum nicht jeder face_id ne liste von face_images zuordnen?
    def get_all_faces(self, path=None):
        """Einlesen der Gesichtsbilder von Platte mit zuordnung der jeweiligen ID durch 2 Listen."""

        path = self.path if path == None else path
        print 'get_faces()'
        ids = 0
        face_images, face_ids = [], []
        for dirname, dirnames, filenames in os.walk(path):
            print dirname
            print dirnames
            print filenames
            for subdirname in dirnames:
                id_path = os.path.join(dirname, subdirname)
                for face_image in os.listdir(id_path):
                    try:
                        im = cv2.imread(os.path.join(id_path, face_image), cv2.IMREAD_GRAYSCALE)
                        hash = face_image.split('_')[1]
                        print 'hash von diesem bild war beim speichern: ', hash
                        face_images.append(np.asarray(im, dtype = np.uint8))
                        face_ids.append(ids)
                    except IOError,(errno,strerror):
                        print "I/O error{0}: {1}".format(errno, strerror)
                    except:
                        print "Unexpected error: ", sys.exc_info()[0]
                        raise
                ids = ids +1 # was passiert wenn auf platte nur id (0, 2) vorhanden sind
        return [face_images, face_ids]
    
        
    def get_hash(self, string):
        """Gibt md5 Hashwert des Objekts als String zurueck"""
        m = hashlib.md5()
        m.update(string)
        digest = binascii.hexlify(m.hexdigest())
        print digest
        return digest


        
