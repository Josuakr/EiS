import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QKeySequence, QWheelEvent
from PyQt5.QtCore import Qt

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
        self.current_shape = None
        self.drawing_mode = None
        self.shift_pressed = False
        self.color1 = 'blue'
        self.color2 = 'black'

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_factor = 1.0
        self.drawing_area_width = 1600  # Width of the drawing area
        self.drawing_area_height = 1200  # Height of the drawing area

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.zoom_factor, self.zoom_factor)
        painter.translate(self.offset_x, self.offset_y)

        painter.setBrush(QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        painter.drawRect(0, 0, self.drawing_area_width, self.drawing_area_height)

        for shape in self.drawing.shapes:
            painter.setBrush(QBrush(shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(shape.border_color, 2))
            if isinstance(shape, Rectangle):
                painter.drawRect(int(shape.x), int(shape.y), int(shape.width), int(shape.height))
            elif isinstance(shape, Circle):
                painter.drawEllipse(int(shape.center_x - shape.radius), int(shape.center_y - shape.radius), int(shape.radius * 2), int(shape.radius * 2))

        if self.current_shape:
            painter.setBrush(QBrush(self.current_shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(self.current_shape.border_color, 2))
            if isinstance(self.current_shape, Rectangle):
                painter.drawRect(int(self.current_shape.x), int(self.current_shape.y), int(self.current_shape.width), int(self.current_shape.height))
            elif isinstance(self.current_shape, Circle):
                painter.drawEllipse(int(self.current_shape.center_x - self.current_shape.radius), int(self.current_shape.center_y - self.current_shape.radius), int(self.current_shape.radius * 2), int(self.current_shape.radius * 2))

    def mousePressEvent(self, event):
        if self.drawing_mode == 'rectangle':
            self.current_shape = Rectangle(event.x() / self.zoom_factor - self.offset_x, event.y() / self.zoom_factor - self.offset_y, 0, 0, QColor(self.color1), QColor(self.color2))
        elif self.drawing_mode == 'circle':
            self.current_shape = Circle(event.x() / self.zoom_factor - self.offset_x, event.y() / self.zoom_factor - self.offset_y, 0, QColor(self.color1), QColor(self.color2))
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing_mode == 'rectangle' and self.current_shape:
            self.current_shape.width = (event.x() / self.zoom_factor - self.offset_x) - self.current_shape.x
            self.current_shape.height = (event.y() / self.zoom_factor - self.offset_y) - self.current_shape.y
            self.update()
        elif self.drawing_mode == 'circle' and self.current_shape:
            dx = (event.x() / self.zoom_factor - self.offset_x) - self.current_shape.center_x
            dy = (event.y() / self.zoom_factor - self.offset_y) - self.current_shape.center_y
            self.current_shape.radius = (dx ** 2 + dy ** 2) ** 0.5
            self.update()

    def mouseReleaseEvent(self, event):
        if self.current_shape:
            self.drawing.add_shape(self.current_shape)
            self.current_shape = None
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            delta = event.angleDelta()
            if delta.y() > 0:
                self.scrollUp()
            elif delta.y() < 0:
                self.scrollDown()
            if delta.x() > 0:
                self.scrollLeft()
            elif delta.x() < 0:
                self.scrollRight()

    def scrollUp(self):
        self.offset_y += 20 / self.zoom_factor
        self.update()

    def scrollDown(self):
        self.offset_y -= 20 / self.zoom_factor
        self.update()

    def scrollLeft(self):
        self.offset_x += 20 / self.zoom_factor
        self.update()

    def scrollRight(self):
        self.offset_x -= 20 / self.zoom_factor
        self.update()

    def zoomIn(self):
        old_center_x = self.width() / 2 / self.zoom_factor - self.offset_x
        old_center_y = self.height() / 2 / self.zoom_factor - self.offset_y
        self.zoom_factor *= 1.1
        new_center_x = self.width() / 2 / self.zoom_factor - self.offset_x
        new_center_y = self.height() / 2 / self.zoom_factor - self.offset_y
        self.offset_x += new_center_x - old_center_x
        self.offset_y += new_center_y - old_center_y
        self.update()

    def zoomOut(self):
        old_center_x = self.width() / 2 / self.zoom_factor - self.offset_x
        old_center_y = self.height() / 2 / self.zoom_factor - self.offset_y
        self.zoom_factor /= 1.1
        new_center_x = self.width() / 2 / self.zoom_factor - self.offset_x
        new_center_y = self.height() / 2 / self.zoom_factor - self.offset_y
        self.offset_x += new_center_x - old_center_x
        self.offset_y += new_center_y - old_center_y
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kill Me')
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

        # Tastenkombinationen
        self.createShortcuts()

    def createMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('Program')
        exitAction = QAction('Quit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('File')
        exitAction = QAction('New', self)
        # exitAction.triggered.connect(self.save)
        fileMenu.addAction(exitAction)
        exitAction = QAction('Open', self)
        # exitAction.triggered.connect(self.save)
        fileMenu.addAction(exitAction)
        fileMenu.addSeparator()
        exitAction = QAction('Save', self)
        # exitAction.triggered.connect(self.save)
        fileMenu.addAction(exitAction)
        exitAction = QAction('Save as...', self)
        # exitAction.triggered.connect(self.save)
        fileMenu.addAction(exitAction)
        exitAction = QAction('Discard', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)

        fileMenu = menubar.addMenu('Edit')
        exitAction = QAction('Discard', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)

        fileMenu = menubar.addMenu('Image')
        exitAction = QAction('No images found.', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Layer')
        exitAction = QAction('No layers available.', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Type')
        exitAction = QAction("I don't got no type", self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        exitAction = QAction("Bad bitches is the only thing that I like", self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Select')
        exitAction = QAction('No selection available.', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Filter')
        exitAction = QAction('#NoFilter', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('3D')
        exitAction = QAction('Imagine I could do that lol', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('View')
        exitAction = QAction('Look at the screen', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Window')
        exitAction = QAction('???', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)
        
        fileMenu = menubar.addMenu('Help')
        exitAction = QAction('There is no help.', self)
        # exitAction.triggered.connect(self.discard)
        fileMenu.addAction(exitAction)

    def createToolbar(self):
        toolbar = self.addToolBar('Toolbar')

        rectAction = QAction('Rechteck', self)
        rectAction.triggered.connect(self.setRectangleMode)
        toolbar.addAction(rectAction)

        circleAction = QAction('Kreis', self)
        circleAction.triggered.connect(self.setCircleMode)
        toolbar.addAction(circleAction)

        # testScene1Action = QAction('Testszene 1', self)
        # testScene1Action.triggered.connect(self.testScene1)
        # toolbar.addAction(testScene1Action)

        # testScene2Action = QAction('Testszene 2', self)
        # testScene2Action.triggered.connect(self.testScene2)
        # toolbar.addAction(testScene2Action)

        zoomInAction = QAction('Zoom In', self)
        zoomInAction.triggered.connect(self.drawingWidget.zoomIn)
        toolbar.addAction(zoomInAction)

        zoomOutAction = QAction('Zoom Out', self)
        zoomOutAction.triggered.connect(self.drawingWidget.zoomOut)
        toolbar.addAction(zoomOutAction)

        color1PickerAction = QAction('FÜllung', self)
        color1PickerAction.triggered.connect(self.openColorPicker1)
        toolbar.addAction(color1PickerAction)
        
        color2PickerAction = QAction('Rand', self)
        color2PickerAction.triggered.connect(self.openColorPicker2)
        toolbar.addAction(color2PickerAction)

    def openColorPicker1(self):
        color1 = QColorDialog.getColor()
        if color1.isValid():
            # print("Selected color:", color1.name())
            self.drawingWidget.color1 = color1
    
    def openColorPicker2(self):
        color2 = QColorDialog.getColor()
        if color2.isValid():
            # print("Selected color:", color2.name())
            self.drawingWidget.color2 = color2

    def createPrimitiveInputs(self):
        # Eingabeelemente für die einfachere Variante
        pass

    def createShortcuts(self):
        zoomInShortcut = QAction('Zoom In', self)
        zoomInShortcut.setShortcut(QKeySequence("Ctrl++"))
        zoomInShortcut.triggered.connect(self.drawingWidget.zoomIn)
        self.addAction(zoomInShortcut)

        zoomOutShortcut = QAction('Zoom Out', self)
        zoomOutShortcut.setShortcut(QKeySequence("Ctrl+-"))
        zoomOutShortcut.triggered.connect(self.drawingWidget.zoomOut)
        self.addAction(zoomOutShortcut)

    def setRectangleMode(self):
        self.drawingWidget.drawing_mode = 'rectangle'

    def setCircleMode(self):
        self.drawingWidget.drawing_mode = 'circle'

    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.drawing.add_shape(Rectangle(100, 100, 200, 150, QColor('red'), QColor('black')))
        self.drawingWidget.drawing.add_shape(Circle(400, 300, 100, QColor('green'), QColor('black')))
        self.drawingWidget.update()

    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.drawing.add_shape(Rectangle(50, 50, 100, 200, QColor('blue'), QColor('black')))
        self.drawingWidget.drawing.add_shape(Rectangle(200, 200, 150, 100, QColor('yellow'), QColor('black')))
        self.drawingWidget.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
