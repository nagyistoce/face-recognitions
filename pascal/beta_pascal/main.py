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
        self.init_folder_structure()
                         
    def init_folder_structure(self):
        """Ueberprueft ob Training-Set-Ordnerstruktur existiert und legt diese bei Bedarf neu an"""
        
        self.path = os.path.expanduser('/home/mi/ptreb001/Desktop/TEST/')
        print self.path
        # check ob Ordner bereits existiert
        if not os.path.exists(self.path):
            print 'lege vz an'
            try:
                os.makedirs(self.path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    print 'ignoriere os.error'
        else:
            print "Verzeichnis bereits vorhannden"
            
    
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