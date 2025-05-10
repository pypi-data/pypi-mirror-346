import sys
import numpy as np
import pyabf
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QFileDialog, QMessageBox, QHBoxLayout, QSlider
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

class ABFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABF Promedio por Selección")
        self.setGeometry(100, 100, 800, 600)
        self.abf = None

        # Layout principal: horizontal
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Layout para el gráfico (izquierda)
        self.graph_layout = QVBoxLayout()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)

        # Layout para los controles (derecha)
        self.controls_layout = QVBoxLayout()

        self.btn_cargar = QPushButton("Cargar archivo ABF")
        self.btn_cargar.clicked.connect(self.cargar_abf)
        self.controls_layout.addWidget(self.btn_cargar)

        self.combo_sweep = QComboBox()
        self.combo_sweep.currentIndexChanged.connect(self.actualizar_grafico)
        self.controls_layout.addWidget(self.combo_sweep)

        self.combo_canal = QComboBox()
        self.combo_canal.currentIndexChanged.connect(self.actualizar_grafico)
        self.controls_layout.addWidget(self.combo_canal)

        self.label_promedio = QLabel("Promedio: ---")
        self.controls_layout.addWidget(self.label_promedio)

        # Botones de zoom (más pequeños)
        self.btn_zoom_x_in = QPushButton("Zoom X +")
        self.btn_zoom_x_out = QPushButton("Zoom X -")
        self.btn_zoom_y_in = QPushButton("Zoom Y +")
        self.btn_zoom_y_out = QPushButton("Zoom Y -")
        self.btn_reset_zoom = QPushButton("Reset Zoom")

        # Ajustar tamaño
        for btn in [self.btn_zoom_x_in, self.btn_zoom_x_out, self.btn_zoom_y_in, self.btn_zoom_y_out, self.btn_reset_zoom]:
            btn.setFixedWidth(100)

        # Conectar funciones
        self.btn_zoom_x_in.clicked.connect(lambda: self.zoom('x', 'in'))
        self.btn_zoom_x_out.clicked.connect(lambda: self.zoom('x', 'out'))
        self.btn_zoom_y_in.clicked.connect(lambda: self.zoom('y', 'in'))
        self.btn_zoom_y_out.clicked.connect(lambda: self.zoom('y', 'out'))
        self.btn_reset_zoom.clicked.connect(self.reset_zoom)

        # Añadir botones al layout
        self.controls_layout.addWidget(self.btn_zoom_x_in)
        self.controls_layout.addWidget(self.btn_zoom_x_out)
        self.controls_layout.addWidget(self.btn_zoom_y_in)
        self.controls_layout.addWidget(self.btn_zoom_y_out)
        self.controls_layout.addWidget(self.btn_reset_zoom)
        self.controls_layout.addStretch()  # empuja los controles hacia arriba

        # Añadir layouts al layout principal
        self.main_layout.addLayout(self.graph_layout, 4)
        self.main_layout.addLayout(self.controls_layout, 1)

        # Slider para el grosor de la línea
        self.slider_grosor = QSlider(Qt.Horizontal)
        self.slider_grosor.setMinimum(0)
        self.slider_grosor.setMaximum(150)  # porque usaremos pasos de 0.1
        self.slider_grosor.setValue(75)    # valor inicial = 1.5
        self.slider_grosor.setSingleStep(1)
        self.slider_grosor.setTickInterval(1)
        self.slider_grosor.setTickPosition(QSlider.TicksBelow)
        self.slider_grosor.valueChanged.connect(self.actualizar_grafico)

        self.controls_layout.addWidget(QLabel("Espesor de línea"))
        self.controls_layout.addWidget(self.slider_grosor)

        self.span = None
        self.tiempo = None
        self.senal = None

    def cargar_abf(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo ABF", "", "Archivos ABF (*.abf)")
        if not archivo:
            return
        self.abf = pyabf.ABF(archivo)

        # Desconectar señales temporalmente
        self.combo_sweep.blockSignals(True)
        self.combo_canal.blockSignals(True)

        self.combo_sweep.clear()
        self.combo_canal.clear()

        self.combo_sweep.addItems([f"Sweep {i}" for i in range(self.abf.sweepCount)])
        self.combo_canal.addItems([f"Canal {i}" for i in range(self.abf.channelCount)])

        # Asegurar selección válida
        self.combo_sweep.setCurrentIndex(0)
        self.combo_canal.setCurrentIndex(0)

        # Reconectar señales
        self.combo_sweep.blockSignals(False)
        self.combo_canal.blockSignals(False)

        self.actualizar_grafico()

    def zoom(self, axis, inout='in', factor=0.2):
        if not self.ax:
            return

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        if axis == 'x':
            center = sum(xlim) / 2
            width = (xlim[1] - xlim[0])
            if inout == 'in':
                width *= (1 - factor)
            else:
                width *= (1 + factor)
            self.ax.set_xlim(center - width/2, center + width/2)

        elif axis == 'y':
            center = sum(ylim) / 2
            height = (ylim[1] - ylim[0])
            if inout == 'in':
                height *= (1 - factor)
            else:
                height *= (1 + factor)
            self.ax.set_ylim(center - height/2, center + height/2)

        self.canvas.draw()
    def reset_zoom(self):
        self.ax.relim()
        self.ax.autoscale()
        self.canvas.draw()

    def actualizar_grafico(self):
        if not self.abf:
            return

        sweep = self.combo_sweep.currentIndex()
        canal = self.combo_canal.currentIndex()

        # Prevenir errores si los combos aún no tienen selección válida
        if sweep < 0 or canal < 0:
            return

        try:
            self.abf.setSweep(sweep, channel=canal)
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"No se pudo establecer sweep/canal:\n{e}")
            return

        self.tiempo = self.abf.sweepX
        self.senal = self.abf.sweepY

        # Determinar si hay límites ya definidos (por zoom anterior)
        has_limits = self.ax.has_data()

        if has_limits:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

        self.ax.clear()
        grosor = self.slider_grosor.value() / 100.0
        self.ax.plot(self.tiempo, self.senal, linewidth=grosor)
        self.ax.set_title(f"Sweep {sweep}, Canal {canal}")
        self.label_promedio.setText("Promedio: ---")

        # Si ya había límites, restaurarlos. Si no, hacer autoscale.
        if has_limits:
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)
        else:
            self.ax.relim()
            self.ax.autoscale()

        if self.span:
            self.span.disconnect_events()
        self.span = SpanSelector(
            self.ax, self.onselect, 'horizontal', useblit=True,
            props=dict(alpha=0.5, facecolor='red'), interactive=True
        )

        self.canvas.draw()


    def onselect(self, xmin, xmax):
        if self.tiempo is None or self.senal is None:
            return
        idx_min = np.searchsorted(self.tiempo, xmin)
        idx_max = np.searchsorted(self.tiempo, xmax)
        if idx_max > idx_min:
            promedio = np.mean(self.senal[idx_min:idx_max])
            self.label_promedio.setText(f"Promedio: {promedio:.3f}")
        else:
            QMessageBox.warning(self, "Selección inválida", "Selecciona un intervalo válido.")


def main():
    app = QApplication(sys.argv)
    ventana = ABFViewer()
    ventana.show()
    sys.exit(app.exec_())
