import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial, time
from tkinter import messagebox

class graficaOscoliscopio:
    def __init__(self,limx,tam,tiempoEntreMuestras,com,veloclidadCom,vDivision):
        self.limx = limx
        self.tam = tam
        self.tiempoEntreMuestras = tiempoEntreMuestras
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [],[]
        self.ln, = plt.plot([], [])
        self.comSerial = serial.Serial(com,veloclidadCom,timeout=0.5)
        self.vDivision = vDivision
        self.banderaErrorGrafica = 0
# -----------------------------------------------------------------
    def init(self):
        self.ax.set_xticks(np.arange(0, self.limx, 1))
        self.ax.set_yticks(np.arange(0, 5 + 1 , 1))
        #self.ax.set_yticks(np.arange(0, 5/self.vDivision + 1 , int((5/self.vDivision)/10) ))
        plt.xlabel('Tiempo (s/Div)')
        plt.ylabel('Tensión (V/Div)')
        #plt.legend(['Canal A'])
        plt.grid(True)
        plt.suptitle('Osciloscopio')
        return self.ln,
# -----------------------------------------------------------------
    def update(self,frame):
        try:
            dato = (float(self.comSerial.readline().decode())*0.0048)/self.vDivision
        except:
            dato = 0
            self.banderaErrorGrafica = self.banderaErrorGrafica + 1
            if self.banderaErrorGrafica == 10:
                messagebox.showerror("Error", "Ha ocurrido un error inesperado, por favor reinicie su puerto")
        #dato = np.sin(frame)
        self.ydata.append(dato)
        self.xdata.append(frame)
        self.ln.set_data(self.xdata,self.ydata)

        return self.ln,
# -----------------------------------------------------------------
    def graficarAnimacion(self):
        self.comSerial.flushInput()
        self.comSerial.flushOutput()

        time.sleep(float(self.tiempoEntreMuestras)/1000)
        ani = FuncAnimation(self.fig,self.update, frames=np.linspace(0, self.limx, self.tam),init_func= self.init, blit=True, interval= int(self.tiempoEntreMuestras),repeat=False  )
        plt.show()
        self.comSerial.close()
    def cerrarSerial(self):
        self.comSerial.close()



archivoParametros = open("parametros.txt","r")
parametros = []

parametros.append(int(archivoParametros.readline()))
parametros.append(int(archivoParametros.readline()))
parametros.append(archivoParametros.readline().rstrip('\n'))
parametros.append(archivoParametros.readline().rstrip('\n'))
parametros.append(int(archivoParametros.readline()))
parametros.append(float(archivoParametros.readline()))
prueba = graficaOscoliscopio(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5])
prueba.graficarAnimacion()
prueba.cerrarSerial()


