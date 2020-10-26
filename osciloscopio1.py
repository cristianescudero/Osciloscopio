import sys, serial, os
from PyQt5.QtWidgets import QApplication,QMainWindow, QDesktopWidget,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

# ------------------------------------------------------------------------------------------------------------------------------------------
class ventanaOsciloscopio(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("osciloscopio1.ui", self)
        self.vDivision=0
        self.sDivision=0
        self.verificacionComSerial = 0
        self.tiempoEntreMuestras = 10 #tiempoEnms
        self.fn_alinearVentanaIzquierda()
        self.setWindowTitle(' Osciloscopio')
        self.labelvDivision.setText(str(self.vDivision))
        self.labelsDivision.setText(str(self.sDivision))
        self.labelLogo.setPixmap(QPixmap('logo.png'))
# ------------------------------------------------------------------------------------------------------------------------------------------
        self.botonIniciarSerial.clicked.connect(self.fn_iniciarSerial)
        self.botonIniciarGrafica.clicked.connect(self.fn_IniciarGrafica)
        self.slidervDvision.valueChanged.connect(self.fn_slidervDivision)
        self.slidersDvision.valueChanged.connect(self.fn_slidersDivision)
# ------------------------------------------------------------------------------------------------------------------------------------------
    def fn_alinearVentanaIzquierda(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveBottomRight(cp)
        self.move(qr.topLeft())
# ------------------------------------------------------------------------------------------------------------------------------------------
    def fn_iniciarSerial(self):
        try:
            self.comSerial = serial.Serial(self.nombrePuertoSerial.text(), 9600)
            self.comSerial.close()
            QMessageBox.about(self, " ", "La comunicación serial funciona correctamente")
            self.verificacionComSerial = 1
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Existe un error, verifique la conexión y los parámetros de la comunicación serial')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.verificacionComSerial = 2
# ------------------------------------------------------------------------------------------------------------------------------------------
    def fn_IniciarGrafica(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        if self.sDivision == 0 or self.vDivision == 0:
            msg.setInformativeText('V/División y S/División deben ser diferentes de cero')
            msg.setWindowTitle("Error")
            msg.exec_()
        elif self.verificacionComSerial == 0:
            msg.setInformativeText('No se ha verificado la comunicación serial')
            msg.setWindowTitle("Error")
            msg.exec_()
        elif self.verificacionComSerial == 2:
            msg.setInformativeText('Existe un error, verifique la conexión y los parámetros de la comunicación serial')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            archivo = open("parametros.txt","w")
            archivo.write("10\n") #limite eje x
            archivo.write(str(int(10*self.sDivision/(self.tiempoEntreMuestras/1000)))+'\n') #numero de muestras
            archivo.write(str(self.tiempoEntreMuestras)+'\n')  #tiempo entre muestras para generar la gráfica
            archivo.write(str(self.comSerial.port)+'\n') #com
            archivo.write(str(self.comSerial.baudrate)+'\n') #velocidad com
            archivo.write(str(self.vDivision))
            archivo.close()
            os.system('python pruebaGraficaConObjeto.py')
# ------------------------------------------------------------------------------------------------------------------------------------------
    def fn_slidervDivision(self,value):
        self.vDivision = value/10
        self.labelvDivision.setText(str(self.vDivision))
# ------------------------------------------------------------------------------------------------------------------------------------------
    def fn_slidersDivision(self,value):
        self.sDivision = value
        self.labelsDivision.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    guiOsciloscopio = ventanaOsciloscopio()
    guiOsciloscopio.show()
    sys.exit(app.exec_())
