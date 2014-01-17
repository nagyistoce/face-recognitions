from PyQt4 import QtCore
from PyQt4 import Qt
from PyQt4 import QtGui
# from PyQt4 import QtOpenGL
import sys


class ToggleWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.texts = ["Hallo Welt", "Hello World", "Guude"]
        self.createWidgets()
        
    def createWidgets(self):
        boxLayout = QtGui.QHBoxLayout()
        self.setLayout(boxLayout)
        self.toggleButton = QtGui.QPushButton("Tausche")
        boxLayout.addWidget(self.toggleButton)
        self.textLabel = QtGui.QLabel(self.texts[0])
        boxLayout.addWidget(self.textLabel)
##        self.textLabel.setAlignment(
##            Qt.AlignHCenter | Qt.AlignVCenter)
        self.textLabel.setMargin(10)
        Qt.QObject.connect(self.toggleButton,Qt.SIGNAL('clicked()'),
                        self.toggle)

    def toggle(self):
        index = self.texts.index(self.textLabel.text())
        index = (index + 1) % len(self.texts)
        self.textLabel.setText(self.texts[index])

class ToggleComplete(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        boxLayout = QtGui.QVBoxLayout()
        self.setLayout(boxLayout)
        self.toggleWidget = ToggleWidget(self)
        boxLayout.addWidget(self.toggleWidget)
        self.quit = QtGui.QPushButton("Ende", self)
        boxLayout.addWidget(self.quit)
        palette = QtGui.QPalette()
        palette.setColor(self.quit.foregroundRole(),Qt.QColor("red"))
        self.quit.setPalette(palette)
        Qt.QObject.connect(self.quit,
                           Qt.SIGNAL('clicked()'),
                           Qt.qApp,
                           Qt.SLOT('quit()'))

class ToggleWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.toggleComplete = ToggleComplete(self)
        self.setCentralWidget(self.toggleComplete)
        self.adjustSize()


def main(args):
    app=QtGui.QApplication(args)
    win=ToggleWindow()
    win.show()
    app.connect(app, # Widget das Signal aussendet
                Qt.SIGNAL('lastWindowClosed()'), # Standard-Signal aus Qt
                app, # empfaenger Widget
                Qt.SLOT('quit()') # zu aktivierender slot des Empfaengers
                )
    return app.exec_()

if __name__ == '__main__':
    # huebsch gemacht endlosschleifen aufruf app.exec_ als returnwert
    sys.exit(main(sys.argv))
