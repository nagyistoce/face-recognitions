# -*- coding: utf-8 -*-
"""
Bootstrap Modul zum Starten der Anwendung.

"""
import sys
import os
import errno

from PyQt4 import Qt
from PyQt4 import QtGui

import gui

class FileSystem(object):
    """Legt Ordnrestruktur der Trainings-Sets an"""
    
    def __init__(self):
        self.path = os.path.expanduser('~/Dropbox/FACERECOGNITION/_TRAINING_SETS_')
        self.init_folder_structure()        
        
    def create_folder(self, path, name=''):
        """Legt einen neuen Ordner an."""
        # check ob Ordner bereits existiert
        path = os.path.join(path, name)
        print path
        if not os.path.exists(path):
            print 'lege vz ', path, ' an.'
            try:
                os.makedirs(path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    print 'ignoriere os.error'
        else:
            print "Verzeichnis bereits vorhannden"        
        
    def init_folder_structure(self):
        """Ueberprueft ob Training-Set-Ordnerstruktur existiert und legt diese bei Bedarf neu an"""
        self.create_folder(self.path)

    def add_face(self, id, face):
        """Fuegt ein Gesichtsbild dem entsprechenden Ordner (ID) hinzu"""
        
    def add_id(self, id):
        """Legt eine neue ID (Ordner) an"""
        self.create_folder(self.path, id)
        
        
def main(args):
    """Hauptfenster, Hauptanwendung Initialisierung und Schliessen Signal anbinden""" 
    app = QtGui.QApplication(args)
    win = gui.Gui()
    win.show()
    app.connect(app,                             # Sender-Widget
                Qt.SIGNAL('lastWindowClosed()'), # Signal
                app,                             # Empfaenger
                Qt.SLOT('quit()')                # aktivierter Slot
                )
    # Trainig-Set Dateistruktur anlegen
    fs = FileSystem()
    
    return app.exec_()
    
if __name__ == '__main__':
    # Endlosschleifen aufruf app.exec_ als returnwert
    sys.exit(main(sys.argv))