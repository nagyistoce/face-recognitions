# -*- coding: utf-8 -*-
'''
Created on 27.01.2014

@author: jjoch001
'''
import database as m
import numpy as np
import numpy.linalg as la

import logging as log

class FaceRecognizer(object):
    '''
    classdocs
    '''


    def __init__(self, num_comp = 0):
        '''
        Constructor
        '''
        self.possible_ids = {}
        self.projections = []
        self.num_comp = 0
        self.W = []
        self.mu = None
        self.threshold = np.finfo('float').max
    
    def trainFisherFaces(self, face_ids, face_images):
        #self.face_ids = np.asarray(face_ids, dtype=np.int32)
        #face_images = np.asarray(face_images, dtype=np.uint8)
        self.face_ids = face_ids
        # Matrix von Bildern werden in eine Zeile gespeichert
        face_images = self.face_images_as_rows(face_images)
        #Berechne Eigenvektoren eig_vec_pca und Mittelwert mean mit PCA, Nummer von Komponenten muss num_comp = n-c sein
        [eig_vec_pca, self.mu] = self.pca(face_images, (face_images.shape[0]-len(np.unique(self.face_ids))))
        #Berechne Eigenvektoren eig_vec_lda mit LDA
        eig_vec_lda = self.lda(self.project(face_images,eig_vec_pca.T, self.mu), self.face_ids, self.num_comp)
        #Tranformations Matrix W, der ein Image Sample in ein (c-1) Dimensionen Space projeziert wird berechnet
        self.W = np.dot(eig_vec_pca, eig_vec_lda)
        #Jedes Bild wird projeziert und die Projektion wird zu eine Liste Projectionen hinzugefügt
        for fi in face_images:
            self.projections.append(self.project(fi.reshape(1,-1),self.W,self.mu))
        
    #der am nähesten Nachbar, wird berechnet, 
    #in dem die kurzeste Distanz aus die Projektionen,basiert auf den euklidischen Distanz, berechnet wird
    def predict(self,unknown_face):
        """Bekommt das zu testende vorbearbeitete Gesichtsbild und gleicht es mit der Datenbank ab.
        return -> face_id
        Die ID der Person der dieses Gesichtsbild am aehnlichsten ist.
        
        """
        #TODO: Initial Wert von min_dist verfeinern

        #min_dist = np.finfo('float').max
        #min_dist = 113.728304447
        #min_class = -1

        min_dist = 15. #np.finfo('float').max
        min_dist = 10.1 #np.finfo('float').max
        face_id = -1

        #Unbekannter Gesicht wird in unser Projectionsmatrix projeziert
        unknown_face = self.project(unknown_face.reshape(1,-1), self.W, self.mu)
        for p in range(len(self.projections)):
            d = self.euclidean_distance(self.projections[p], unknown_face)
            if d < min_dist:
                #print 'mindist: %s ID: %s' % (min_dist, min_class)
                min_dist = d
                face_id = self.face_ids[p]
                log.debug('min_dist: %s id: %s ' % (min_dist, face_id))
        if min_dist > 10:
            min_dist = -1
        return face_id
    
    #y = W^T(X-u) schauen ob W.T korrekt ist. 
    #Vorher: nur W aber jedes self.W musste als self.W.T als parameter geben
    def project(self, face, W, u = None):
        if u is None:
            return np.dot(face,W.T)
        return np.dot(face-u,W.T)
    
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
        #Errechne der Mittelwert von alle Klassen und ihre Samples(Images)
        mean = face_images.mean(axis=0)
        face_images = face_images - mean
        [eigenvectors, eigenvalues, var] = la.svd(face_images.T, full_matrices = False)
        #Sortiere von eigenwerte abhängig die eigenwerte und eigenvektoren absteigend 
        sort_eigen = np.argsort(-eigenvalues)
        eigenvectors = eigenvectors[:,sort_eigen]
        #eigenvalues = eigenvalues[sort_eigen].copy()
        #Schneide Eigenvektoren ab Anzahl von Komponenten ab, wollen nur non-null comp haben
        #eigenvalues = eigenvalues[:num_comp].copy()
        eigenvectors = eigenvectors[:,:num_comp].copy()
        return eigenvectors, mean
    #Lineare Discriminant Analysis
    def lda(self, face_images, face_ids, num_comp = 0):
        #Die verschieden Klassen an sich
        c = np.unique(face_ids)
        [n,d] = face_images.shape
        if num_comp<=0 or num_comp>(len(c)-1):
            num_comp = len(c)-1
        #Mittelwert aus alle Klassen
        total_mean = face_images.mean(axis=0)
        sb = np.zeros((d,d), dtype = np.float32)
        sw = np.zeros((d,d), dtype = np.float32)
        #print 'lda:', c, face_images.shape, len(face_ids)
        for i in c:
            #Images (Samples) einer Klasse
            face_i = face_images[np.where(face_ids==i)[0],:]
            #Mittelwert einer Klasse
            mean_i = face_i.mean(axis=0)
            #Zwischen-Klassen Verteilung
            sb += n * np.dot((mean_i-total_mean).T, (mean_i-total_mean))
            #Innerhalb-Klassen Verteilung
            sw += np.dot((face_i-mean_i).T,(face_i-mean_i))
        #np.svd kann nicht verwendet werden weil sw und sw nicht umbedingt symmetrische matrixen ergeben 
        [eigenvalues, eigenvectors] = la.eig(la.inv(sw)*sb)
        #Sortiere von eigenwerte abhängig die eigenwerte und eigenvektoren absteigend 
        sort_eigen = np.argsort(-eigenvalues.real)
        eigenvectors = eigenvectors[:,sort_eigen]
        #eigenvalues= eigenvalues[sort_eigen]
        #Schneide Eigenvektoren ab Anzahl von Komponenten ab, wollen nur non-null comp haben
        #eigenvalues = np.array(eigenvalues[:num_comp].real, dtype=np.float32, copy = True)
        eigenvectors = np.array(eigenvectors[:,num_comp].real, dtype=np.float32, copy = True)
        return eigenvectors
    #Euklidischen Distanz zweier Projektion Matrizen
    def euclidean_distance(self,p,q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sqrt(np.sum(np.power((p-q),2)))
    def cosine_distance(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return 1-(np.dot(p,q)/(la.norm(p)*la.norm(q)))
        #return 1-np.dot(p.T,q) / (np.sqrt(np.dot(p,p.T)*np.dot(q,q.T)))
# if __name__ == "__main__":
#     ts = m.TrainingSets()
#     [face_images, face_ids] = ts.get_all_faces()
# #     uf = face_images[94]
# #     i_f = face_ids[94]
# #     face_images[:] = face_images[:94]+face_images[94:]
# #     face_ids[:] = face_ids[:94]+face_ids[95:]
#     fr = FaceRecognizer(face_images[:-1], face_ids[:-1])
#     i = fr.predict(face_images[-1])
#     print "Expected ID:", face_ids[-1],"It predicts the id:", i