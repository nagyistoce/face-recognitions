'''
Created on 16.01.2014

@author: ptreb001
'''
from PyQt4 import QtCore
from PyQt4 import Qt
from PyQt4 import QtGui
# from PyQt4 import QtOpenGL
import sys

class ToggleWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.setCentralWidget(self)
        self.adjustSize()
        
def main(args):
    app = QtGui.QApplication(args)
    widget = QtGui.QWidget()    
    boxLayout = QtGui.QVBoxLayout()    
    widget.setLayout(boxLayout)
    labels = [QtGui.QLabel("Nach %i kommt %i" % (i, i+1), None) for i in range(10)]
    
    for label in labels:    
        boxLayout.addWidget(label)
    widget.show()
    return app.exec_()

if __name__ == '__main__':
    # huebsch gemacht endlosschleifen aufruf app.exec_ als returnwert
    sys.exit(main(sys.argv))