import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vektororientiertes Zeichenprogramm')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Zeichenbereich
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)
        
        # Menü und Toolbar
        self.createMenu()
        self.createToolbar()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('Datei')
        
        exitAction = QAction('Beenden', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')
        
        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.addRectangle)
        toolbar.addAction(rectAction)
        
        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.addCircle)
        toolbar.addAction(circleAction)
        
    def addRectangle(self):
        self.drawingWidget.addRectangle()

    def addCircle(self):
        self.drawingWidget.addCircle()

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        
    def addRectangle(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.shapes.append(('rect', QRectF(100, 100, 200, 150), color))
            self.update()

    def addCircle(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.shapes.append(('circle', QRectF(300, 200, 150, 150), color))
            self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for shape, rect, color in self.shapes:
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            if shape == 'rect':
                painter.drawRect(rect)
            elif shape == 'circle':
                painter.drawEllipse(rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

class Shape:
    def __init__(self, fill_color, border_color):
        self.fill_color = fill_color
        self.border_color = border_color

class Rectangle(Shape):
    def __init__(self, x, y, width, height, fill_color, border_color):
        super().__init__(fill_color, border_color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Circle(Shape):
    def __init__(self, center_x, center_y, radius, fill_color, border_color):
        super().__init__(fill_color, border_color)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Drawing:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.drawing = Drawing()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.drawing.shapes:
            painter.setBrush(QBrush(shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(shape.border_color, 2))
            if isinstance(shape, Rectangle):
                painter.drawRect(shape.x, shape.y, shape.width, shape.height)
            elif isinstance(shape, Circle):
                painter.drawEllipse(shape.center_x - shape.radius, shape.center_y - shape.radius, shape.radius * 2, shape.radius * 2)

    def addRectangle(self):
        fill_color = QColorDialog.getColor()
        border_color = QColorDialog.getColor()
        if fill_color.isValid() and border_color.isValid():
            rect = Rectangle(100, 100, 200, 150, fill_color, border_color)
            self.drawing.add_shape(rect)
            self.update()

    def addCircle(self):
        fill_color = QColorDialog.getColor()
        border_color = QColorDialog.getColor()
        if fill_color.isValid() and border_color.isValid():
            circle = Circle(300, 200, 75, fill_color, border_color)
            self.drawing.add_shape(circle)
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vektororientiertes Zeichenprogramm')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Zeichenbereich
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)
        
        # Menü und Toolbar
        self.createMenu()
        self.createToolbar()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('Datei')
        
        exitAction = QAction('Beenden', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')
        
        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.addRectangle)
        toolbar.addAction(rectAction)
        
        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.addCircle)
        toolbar.addAction(circleAction)
        
        testScene1Action = QAction('Testszene 1', self)
        testScene1Action.triggered.connect(self.testScene1)
        toolbar.addAction(testScene1Action)
        
        testScene2Action = QAction('Testszene 2', self)
        testScene2Action.triggered.connect(self.testScene2)
        toolbar.addAction(testScene2Action)
        
    def addRectangle(self):
        self.drawingWidget.addRectangle()

    def addCircle(self):
        self.drawingWidget.addCircle()
        
    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addCircle()
        self.drawingWidget.update()
        
    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addRectangle()
        self.drawingWidget.update()

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.drawing = Drawing()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_factor = 1.0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.zoom_factor, self.zoom_factor)
        painter.translate(self.offset_x, self.offset_y)
        for shape in self.drawing.shapes:
            painter.setBrush(QBrush(shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(shape.border_color, 2))
            if isinstance(shape, Rectangle):
                painter.drawRect(shape.x, shape.y, shape.width, shape.height)
            elif isinstance(shape, Circle):
                painter.drawEllipse(shape.center_x - shape.radius, shape.center_y - shape.radius, shape.radius * 2, shape.radius * 2)

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.offset_x += delta.x() / self.zoom_factor
        self.offset_y += delta.y() / self.zoom_factor
        self.last_mouse_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vektororientiertes Zeichenprogramm')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Zeichenbereich
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)
        
        # Menü und Toolbar
        self.createMenu()
        self.createToolbar()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('Datei')
        
        exitAction = QAction('Beenden', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')
        
        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.addRectangle)
        toolbar.addAction(rectAction)
        
        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.addCircle)
        toolbar.addAction(circleAction)
        
        testScene1Action = QAction('Testszene 1', self)
        testScene1Action.triggered.connect(self.testScene1)
        toolbar.addAction(testScene1Action)
        
        testScene2Action = QAction('Testszene 2', self)
        testScene2Action.triggered.connect(self.testScene2)
        toolbar.addAction(testScene2Action)
        
        zoomInAction = QAction('Zoom In', self)
        zoomInAction.triggered.connect(self.zoomIn)
        toolbar.addAction(zoomInAction)
        
        zoomOutAction = QAction('Zoom Out', self)
        zoomOutAction.triggered.connect(self.zoomOut)
        toolbar.addAction(zoomOutAction)
        
    def addRectangle(self):
        self.drawingWidget.addRectangle()

    def addCircle(self):
        self.drawingWidget.addCircle()
        
    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addCircle()
        self.drawingWidget.update()
        
    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addRectangle()
        self.drawingWidget.update()
        
    def zoomIn(self):
        self.drawingWidget.zoom_factor *= 1.1
        self.drawingWidget.update()
        
    def zoomOut(self):
        self.drawingWidget.zoom_factor /= 1.1
        self.drawingWidget.update()

from PyQt5.QtWidgets import QDoubleSpinBox, QLabel, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vektororientiertes Zeichenprogramm')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Zeichenbereich
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)
        
        # Menü und Toolbar
        self.createMenu()
        self.createToolbar()
        
        # Eingabeelemente für neue Primitive
        self.createPrimitiveInputs()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('Datei')
        
        exitAction = QAction('Beenden', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')
        
        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.addRectangle)
        toolbar.addAction(rectAction)
        
        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.addCircle)
        toolbar.addAction(circleAction)
        
        testScene1Action = QAction('Testszene 1', self)
        testScene1Action.triggered.connect(self.testScene1)
        toolbar.addAction(testScene1Action)
        
        testScene2Action = QAction('Testszene 2', self)
        testScene2Action.triggered.connect(self.testScene2)
        toolbar.addAction(testScene2Action)
        
        zoomInAction = QAction('Zoom In', self)
        zoomInAction.triggered.connect(self.zoomIn)
        toolbar.addAction(zoomInAction)
        
        zoomOutAction = QAction('Zoom Out', self)
        zoomOutAction.triggered.connect(self.zoomOut)
        toolbar.addAction(zoomOutAction)
        
    def createPrimitiveInputs(self):
        primitiveLayout = QHBoxLayout()
        
        self.xInput = QDoubleSpinBox()
        self.xInput.setRange(0, 800)
        self.xInput.setPrefix('X: ')
        
        self.yInput = QDoubleSpinBox()
        self.yInput.setRange(0, 600)
        self.yInput.setPrefix('Y: ')
        
        self.widthInput = QDoubleSpinBox()
        self.widthInput.setRange(0, 800)
        self.widthInput.setPrefix('Breite: ')
        
        self.heightInput = QDoubleSpinBox()
        self.heightInput.setRange(0, 600)
        self.heightInput.setPrefix('Höhe: ')
        
        primitiveLayout.addWidget(QLabel('Neues Primitiv: '))
        primitiveLayout.addWidget(self.xInput)
        primitiveLayout.addWidget(self.yInput)
        primitiveLayout.addWidget(self.widthInput)
        primitiveLayout.addWidget(self.heightInput)
        
        addButton = QPushButton('Hinzufügen')
        addButton.clicked.connect(self.addPrimitive)
        primitiveLayout.addWidget(addButton)
        
        self.layout.addLayout(primitiveLayout)
        
    def addPrimitive(self):
        x = self.xInput.value()
        y = self.yInput.value()
        width = self.widthInput.value()
        height = self.heightInput.value()
        
        fill_color = QColorDialog.getColor()
        border_color = QColorDialog.getColor()
        
        if fill_color.isValid() and border_color.isValid():
            rect = Rectangle(x, y, width, height, fill_color, border_color)
            self.drawingWidget.drawing.add_shape(rect)
            self.drawingWidget.update()
        
    def addRectangle(self):
        self.addPrimitive()

    def addCircle(self):
        # Similar implementation for circle
        pass
        
    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addCircle()
        self.drawingWidget.update()
        
    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addRectangle()
        self.drawingWidget.update()
        
    def zoomIn(self):
        self.drawingWidget.zoom_factor *= 1.1
        self.drawingWidget.update()
        
    def zoomOut(self):
        self.drawingWidget.zoom_factor /= 1.1
        self.drawingWidget.update()

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.drawing = Drawing()
        self.initUI()
        self.current_shape = None
        self.drawing_mode = None
        
    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_factor = 1.0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.zoom_factor, self.zoom_factor)
        painter.translate(self.offset_x, self.offset_y)
        for shape in self.drawing.shapes:
            painter.setBrush(QBrush(shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(shape.border_color, 2))
            if isinstance(shape, Rectangle):
                painter.drawRect(shape.x, shape.y, shape.width, shape.height)
            elif isinstance(shape, Circle):
                painter.drawEllipse(shape.center_x - shape.radius, shape.center_y - shape.radius, shape.radius * 2, shape.radius * 2)
                
        if self.current_shape:
            painter.setBrush(QBrush(self.current_shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(self.current_shape.border_color, 2))
            if isinstance(self.current_shape, Rectangle):
                painter.drawRect(self.current_shape.x, self.current_shape.y, self.current_shape.width, self.current_shape.height)
            elif isinstance(self.current_shape, Circle):
                painter.drawEllipse(self.current_shape.center_x - self.current_shape.radius, self.current_shape.center_y - self.current_shape.radius, self.current_shape.radius * 2, self.current_shape.radius * 2)
    
    def mousePressEvent(self, event):
        if self.drawing_mode == 'rectangle':
            self.current_shape = Rectangle(event.x(), event.y(), 0, 0, QColor('blue'), QColor('black'))
        elif self.drawing_mode == 'circle':
            self.current_shape = Circle(event.x(), event.y(), 0, QColor('blue'), QColor('black'))
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.drawing_mode == 'rectangle' and self.current_shape:
            self.current_shape.width = event.x() - self.current_shape.x
            self.current_shape.height = event.y() - self.current_shape.y
            self.update()
        elif self.drawing_mode == 'circle' and self.current_shape:
            dx = event.x() - self.current_shape.center_x
            dy = event.y() - self.current_shape.center_y
            self.current_shape.radius = (dx ** 2 + dy ** 2) ** 0.5
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.current_shape:
            self.drawing.add_shape(self.current_shape)
            self.current_shape = None
            self.update()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vektororientiertes Zeichenprogramm')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Zeichenbereich
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)
        
        # Menü und Toolbar
        self.createMenu()
        self.createToolbar()
        
        # Eingabeelemente für neue Primitive
        self.createPrimitiveInputs()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('Datei')
        
        exitAction = QAction('Beenden', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')
        
        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.setRectangleMode)
        toolbar.addAction(rectAction)
        
        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.setCircleMode)
        toolbar.addAction(circleAction)
        
        testScene1Action = QAction('Testszene 1', self)
        testScene1Action.triggered.connect(self.testScene1)
        toolbar.addAction(testScene1Action)
        
        testScene2Action = QAction('Testszene 2', self)
        testScene2Action.triggered.connect(self.testScene2)
        toolbar.addAction(testScene2Action)
        
        zoomInAction = QAction('Zoom In', self)
        zoomInAction.triggered.connect(self.zoomIn)
        toolbar.addAction(zoomInAction)
        
        zoomOutAction = QAction('Zoom Out', self)
        zoomOutAction.triggered.connect(self.zoomOut)
        toolbar.addAction(zoomOutAction)
        
    def createPrimitiveInputs(self):
        # Eingabeelemente für die einfachere Variante
        pass
        
    def setRectangleMode(self):
        self.drawingWidget.drawing_mode = 'rectangle'
        
    def setCircleMode(self):
        self.drawingWidget.drawing_mode = 'circle'
        
    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addCircle()
        self.drawingWidget.update()
        
    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.addRectangle()
        self.drawingWidget.addRectangle()
        self.drawingWidget.update()
        
    def zoomIn(self):
        self.drawingWidget.zoom_factor *= 1.1
        self.drawingWidget.update()
        
    def zoomOut(self):
        self.drawingWidget.zoom_factor /= 1.1
        self.drawingWidget.update()

