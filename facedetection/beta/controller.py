'''
Created on 31.01.2014

@author: jjoch001
'''
from fdetection import FaceDetector as fd
import frecognize as fr

class Controller(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
                # Facedetekor-Objekt
        self.detect = fd()
    def frame_to_face(self, frame, face_id, save_face, recognize_face):
        self.frame, self.face = self.detect.detectFace(frame)
        if self.face is not None:
            if save_face:
                self.detect.acceptNewFace(self.face, face_id)
                   
            if recognize_face:
                self.fr = fr.FaceRecognizer()
                i = self.fr.predict(self.face)
                print "Expects:", face_id
                print "It predicts the id:", i
        return self.frame
    