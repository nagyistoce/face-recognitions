# -*- coding: utf-8 -*-
'''
Created on 27.01.2014

@author: jjoch001
'''
import database as m
import numpy as np
import numpy.linalg as la
import cv2
import pprint as pp
class FaceRecognizer(object):
    '''
    classdocs
    '''


    def __init__(self, face_images, face_ids, num_comp = 0):
        '''
        Constructor
        '''
        #self.ts = m.TrainingSets()
        self.projections = []
        self.num_comp = 0
        self.W = []
        self.mu = None
        #if face_images is None and face_ids is None:
            #[face_images, face_ids] = self.ts.get_all_faces()
        self.trainFisherFaces(face_ids, face_images)
    
    def trainFisherFaces(self, face_ids, face_images):
        self.face_ids = np.asarray(face_ids, dtype=np.int32)
        face_images = np.asarray(face_images, dtype=np.uint8)
        face_images = self.face_images_as_rows(face_images)
        n = face_images.shape[0]
        c = len(np.unique(self.face_ids))
        [eigenvectors_pca, self.mu] = self.pca(face_images, (n-c))
        eigenvectors_lda = self.lda(self.project(face_images,eigenvectors_pca, self.mu), self.face_ids, self.num_comp)
        self.W = np.dot(eigenvectors_pca, eigenvectors_lda)
        for fi in face_images:
            self.projections.append(self.project(fi.reshape(1,-1),self.W.T,self.mu))
        
    #der am nähesten Nachbar basiert auf den euklidischen Distanz wird berechnet
    def predict(self,unknown_face):
        min_dist = np.finfo('float').max
        min_class = -1
        unknown_face=self.project(unknown_face.reshape(1,-1), self.W.T, self.mu)
        for p in range(len(self.projections)):
            d = self.euclidean_distance(self.projections[p], unknown_face)
            if d < min_dist:
                min_dist = d
                min_class = self.face_ids[p]
        return min_class
    
    #y = W^T(X-u)
    def project(self, face, W, u = None):
        if u is None:
            return np.dot(face,W)
        return np.dot(face-u,W)
    
    #Jede Reihe is ein flache image matrix
    def face_images_as_rows(self,face_images):
        if len(face_images) == 0:
            return np.asarray([])
        data_matrix = np.empty((0,face_images[0].size), dtype=face_images[0].dtype)
        for fi in face_images:
            data_matrix= np.append(data_matrix, fi.reshape(1,-1),axis = 0)
        return np.asmatrix(data_matrix)
    #Principal Component Analysis
    def pca(self, face_images,num_comp = 0):
        n = face_images.shape[0]
        if num_comp<=0 or num_comp > n:
            num_comp = n
        mean = face_images.mean(axis=0)
        face_images = face_images - mean
        [eigenvectors, eigenvalues, v] = la.svd(face_images.T, full_matrices = False)
        #Sortiere eigenwerte und eigenvektoren absteigend von eigenwerte abhängig
        sort_eigen = np.argsort(-eigenvalues)
        eigenvectors = eigenvectors[:,sort_eigen]
        #eigenvalues = eigenvalues[sort_eigen].copy()
        #eigenvalues = eigenvalues[:num_comp].copy()
        #Schneide Eigenvektoren ab Anzahl von Komponenten ab
        eigenvectors = eigenvectors[:,:num_comp].copy()
        return eigenvectors, mean
    #Lineare Discriminant Analysis
    def lda(self, face_images, face_ids, num_comp = 0):
        c = np.unique(face_ids)
        [n,d] = face_images.shape
        if num_comp<=0 or num_comp>(len(c)-1):
            num_comp = len(c)-1
        total_mean = face_images.mean(axis=0)
        sb = np.zeros((d,d), dtype = np.float32)
        sw = np.zeros((d,d), dtype = np.float32)
        print 'lda:', c, face_images.shape, face_ids.shape
        for i in c:
            face_i = face_images[np.where(face_ids==i)[0],:]
            mean_i = face_i.mean(axis=0)
            sb += n * np.dot((mean_i-total_mean).T, (mean_i-total_mean))
            sw += np.dot((face_i-mean_i).T,(face_i-mean_i))
        [eigenvalues, eigenvectors] = la.eig(la.inv(sw)*sb)
        sort_eigen = np.argsort(-eigenvalues.real)
        eigenvectors = eigenvectors[:,sort_eigen]
        eigenvalues= eigenvalues[sort_eigen]
        eigenvalues = np.array(eigenvalues[:num_comp].real, dtype=np.float32, copy = True)
        eigenvectors = np.array(eigenvectors[:,num_comp].real, dtype=np.float32, copy = True)
        return eigenvectors
    
    def euclidean_distance(self,p,q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sqrt(np.sum(np.power((p-q),2)))
    
if __name__ == "__main__":
    ts = m.TrainingSets()
    [face_images, face_ids] = ts.get_all_faces()
    uf = face_images[94]
#     i_f = face_ids[94]
#     face_images[:] = face_images[:94]+face_images[94:]
#     face_ids[:] = face_ids[:94]+face_ids[95:]
    fr = FaceRecognizer(face_images[:-1], face_ids[:-1])
    i = fr.predict(face_images[-1])
    print "Expected ID:", face_ids[-1],"It predicts the id:", i