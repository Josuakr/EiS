import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QColorDialog, QSpinBox, QWidgetAction
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QKeySequence, QWheelEvent, QPolygon
from PyQt5.QtCore import Qt, QPoint

class Shape:
    def __init__(self, fill_color, border_color, border_width):
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

class Rectangle(Shape):
    def __init__(self, x, y, width, height, fill_color, border_color, border_width):
        super().__init__(fill_color, border_color, border_width)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Circle(Shape):
    def __init__(self, center_x, center_y, radius, fill_color, border_color, border_width):
        super().__init__(fill_color, border_color, border_width)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Star(Shape):
    def __init__(self, x, y, points, inner_radius, outer_radius, fill_color, border_color, border_width):
        super().__init__(fill_color, border_color, border_width)
        self.x = x
        self.y = y
        self.points = points
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

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
        self.color1Cache = None
        self.color2 = 'black'
        self.hollowDrawing = False
        self.starPointCount = 8
        self.experimental = 2
        self.border_width = 2  # Initialize border_width

    def updateStarPointCount(self, value):
        self.starPointCount = value
        print(f'Star Point Count updated to: {value}')

    def updateBorderWidth(self, value):
        self.border_width = value
        print(f'Border width updated to: {value}')
        self.update()

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_factor = 1.0
        self.drawing_area_width = 1600  
        self.drawing_area_height = 1200  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.zoom_factor, self.zoom_factor)
        painter.translate(self.offset_x, self.offset_y)

        painter.setBrush(QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        painter.drawRect(0, 0, self.drawing_area_width, self.drawing_area_height)

        for shape in self.drawing.shapes:
            painter.setBrush(QBrush(shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(shape.border_color, shape.border_width))
            if isinstance(shape, Rectangle):
                painter.drawRect(int(shape.x), int(shape.y), int(shape.width), int(shape.height))
            elif isinstance(shape, Circle):
                painter.drawEllipse(int(shape.center_x - shape.radius), int(shape.center_y - shape.radius), int(shape.radius * 2), int(shape.radius * 2))
            elif isinstance(shape, Star):
                self.drawStar(painter, shape)

        if self.current_shape:
            painter.setBrush(QBrush(self.current_shape.fill_color, Qt.SolidPattern))
            painter.setPen(QPen(self.current_shape.border_color, self.current_shape.border_width))
            if isinstance(self.current_shape, Rectangle):
                painter.drawRect(int(self.current_shape.x), int(self.current_shape.y), int(self.current_shape.width), int(self.current_shape.height))
            elif isinstance(self.current_shape, Circle):
                painter.drawEllipse(int(self.current_shape.center_x - self.current_shape.radius), int(self.current_shape.center_y - self.current_shape.radius), int(self.current_shape.radius * 2), int(self.current_shape.radius * 2))
            elif isinstance(self.current_shape, Star):
                self.drawStar(painter, self.current_shape)

    def drawStar(self, painter, star):
        points = []
        angle = self.experimental * math.pi / star.points
        for i in range(star.points * 2):
            r = star.outer_radius if i % 2 == 0 else star.inner_radius
            theta = i * angle / 2
            x = star.x + r * math.cos(theta)
            y = star.y + r * math.sin(theta)
            points.append(QPoint(int(x), int(y)))

        star_polygon = QPolygon(points)
        painter.drawPolygon(star_polygon)

    def mousePressEvent(self, event):
        if self.hollowDrawing:
            self.color1Cache = self.color1
            self.color1 = 'transparent'
        if self.drawing_mode == 'rectangle':
            self.current_shape = Rectangle(event.x() / self.zoom_factor - self.offset_x, event.y() / self.zoom_factor - self.offset_y, 0, 0, QColor(self.color1), QColor(self.color2), self.border_width)
        elif self.drawing_mode == 'circle':
            self.current_shape = Circle(event.x() / self.zoom_factor - self.offset_x, event.y() / self.zoom_factor - self.offset_y, 0, QColor(self.color1), QColor(self.color2), self.border_width)
        elif self.drawing_mode == 'star':
            self.current_shape = Star(event.x() / self.zoom_factor - self.offset_x, event.y() / self.zoom_factor - self.offset_y, self.starPointCount, 0, 0, QColor(self.color1), QColor(self.color2), self.border_width)
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing_mode == 'rectangle' and self.current_shape:
            self.current_shape.width = (event.x() / self.zoom_factor - self.offset_x) - self.current_shape.x
            self.current_shape.height = (event.y() / self.zoom_factor - self.offset_y) - self.current_shape.y
            self.update()
        elif self.drawing_mode == 'circle' and self.current_shape:
            dx = (event.x() / self.zoom_factor - self.offset_x) - self.current_shape.center_x
            dy = (event.y() / self.zoom_factor - self.offset_x) - self.current_shape.center_y
            self.current_shape.radius = (dx ** 2 + dy ** 2) ** 0.5
            self.update()
        elif self.drawing_mode == 'star' and self.current_shape:
            dx = (event.x() / self.zoom_factor - self.offset_x) - self.current_shape.x
            dy = (event.y() / self.zoom_factor - self.offset_y) - self.current_shape.y
            self.current_shape.outer_radius = (dx ** 2 + dy ** 2) ** 0.5
            self.current_shape.inner_radius = self.current_shape.outer_radius / 2 
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
        new_center_x = self.width() / 2 /self.zoom_factor - self.offset_x
        new_center_y = self.height() / 2 / self.zoom_factor - self.offset_y
        self.offset_x += new_center_x - old_center_x
        self.offset_y += new_center_y - old_center_y
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MS Pain')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Drawing area
        self.drawingWidget = DrawingWidget()
        self.layout.addWidget(self.drawingWidget)

        # Menu and Toolbar
        self.createMenu()
        self.createToolbar()

        # Keyboard Shortcuts
        self.createShortcuts()

    def createMenu(self):
        # Menu bar
        menubar = self.menuBar()

        # Program Menu
        programMenu = menubar.addMenu('Program')
        exitAction = QAction('End (my life)', self)
        exitAction.triggered.connect(self.close)
        programMenu.addAction(exitAction)
        
        # File Menu
        fileMenu = menubar.addMenu('File')
        newAction = QAction('New', self)
        fileMenu.addAction(newAction)
        openAction = QAction('Open', self)
        fileMenu.addAction(openAction)
        openRecentAction = QAction('Open recent...', self)
        fileMenu.addAction(openRecentAction)
        testScenesMenu = fileMenu.addMenu('Test Scenes')
        testScene1Action = QAction('Testscene 1', self)
        testScene1Action.triggered.connect(self.testScene1)
        testScenesMenu.addAction(testScene1Action)
        testScene2Action = QAction('Testscene 2', self)
        testScene2Action.triggered.connect(self.testScene2)
        testScenesMenu.addAction(testScene2Action)
        fileMenu.addSeparator()
        saveAction = QAction('Save', self)
        fileMenu.addAction(saveAction)
        saveAsAction = QAction('Save as...', self)
        fileMenu.addAction(saveAsAction)
        discardAction = QAction('Discard', self)
        fileMenu.addAction(discardAction)
        
        # Edit Menu
        editMenu = menubar.addMenu('Edit')
        discardAction = QAction('Discard', self)
        editMenu.addAction(discardAction)

        # Image Menu
        imageMenu = menubar.addMenu('Image')
        noImagesAction = QAction('No images found.', self)
        imageMenu.addAction(noImagesAction)
        
        # Layer Menu
        layerMenu = menubar.addMenu('Layer')
        noLayersAction = QAction('No layers available.', self)
        layerMenu.addAction(noLayersAction)
        
        # Type Menu
        typeMenu = menubar.addMenu('Type')
        noTypeAction = QAction("I don't got no type", self)
        typeMenu.addAction(noTypeAction)
        badBitchesAction = QAction("Bad bitches is the only thing that I like", self)
        typeMenu.addAction(badBitchesAction)
        
        # Select Menu
        selectMenu = menubar.addMenu('Select')
        noSelectionAction = QAction('No selection available.', self)
        selectMenu.addAction(noSelectionAction)
        
        # Filter Menu
        filterMenu = menubar.addMenu('Filter')
        noFilterAction = QAction('#NoFilter', self)
        filterMenu.addAction(noFilterAction)
        
        # 3D Menu
        threeDMenu = menubar.addMenu('3D')
        no3DAction = QAction('Imagine I could do that lol', self)
        threeDMenu.addAction(no3DAction)
        
        # View Menu
        viewMenu = menubar.addMenu('View')
        lookAtScreenAction = QAction('Look at the screen', self)
        viewMenu.addAction(lookAtScreenAction)
        
        # Window Menu
        windowMenu = menubar.addMenu('Window')
        windowAction = QAction('???', self)
        windowMenu.addAction(windowAction)
        
        # Help Menu
        helpMenu = menubar.addMenu('Help')
        noHelpAction = QAction('There is no help.', self)
        helpMenu.addAction(noHelpAction)

    def createToolbar(self):
        # Toolbar
        toolbar = self.addToolBar('Toolbar')

        # Actions
        rectAction = QAction('Rectangle', self)
        rectAction.triggered.connect(self.setRectangleMode)
        toolbar.addAction(rectAction)

        circleAction = QAction('Circle', self)
        circleAction.triggered.connect(self.setCircleMode)
        toolbar.addAction(circleAction)

        starAction = QAction('Star', self)
        starAction.triggered.connect(self.setStarMode)
        toolbar.addAction(starAction)

        self.spinBox = QSpinBox()
        self.spinBox.setRange(0, 100)  # Set range for spin box
        self.spinBox.setValue(10)     # Set default value
        self.spinBox.valueChanged.connect(self.drawingWidget.updateStarPointCount)  # Connect to updateStarPointCount

        # Create a QWidgetAction and set the QSpinBox as its default widget
        spinBoxAction = QWidgetAction(self)
        spinBoxAction.setDefaultWidget(self.spinBox)
        toolbar.addAction(spinBoxAction)

        zoomInAction = QAction('Zoom In', self)
        zoomInAction.triggered.connect(self.drawingWidget.zoomIn)
        toolbar.addAction(zoomInAction)

        zoomOutAction = QAction('Zoom Out', self)
        zoomOutAction.triggered.connect(self.drawingWidget.zoomOut)
        toolbar.addAction(zoomOutAction)

        color1PickerAction = QAction('Fill', self)
        color1PickerAction.triggered.connect(self.openColorPicker1)
        toolbar.addAction(color1PickerAction)
        
        color2PickerAction = QAction('Border', self)
        color2PickerAction.triggered.connect(self.openColorPicker2)
        toolbar.addAction(color2PickerAction)
        # Spin Box for border width
        self.spinBox = QSpinBox()
        self.spinBox.setRange(0, 100)  # Set range for spin box
        self.spinBox.setValue(2)     # Set default value
        self.spinBox.valueChanged.connect(self.drawingWidget.updateBorderWidth)  # Connect to updateBorderWidth

        # Create a QWidgetAction and set the QSpinBox as its default widget
        spinBoxAction = QWidgetAction(self)
        spinBoxAction.setDefaultWidget(self.spinBox)
        toolbar.addAction(spinBoxAction)

        hollow = QAction('Hollow', self, checkable=True)
        hollow.triggered.connect(self.isHollow)
        toolbar.addAction(hollow)

    def openColorPicker1(self):
        color1 = QColorDialog.getColor()
        if color1.isValid():
            self.drawingWidget.color1 = color1
    
    def openColorPicker2(self):
        color2 = QColorDialog.getColor()
        if color2.isValid():
            self.drawingWidget.color2 = color2

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

    def setStarMode(self):
        self.drawingWidget.drawing_mode = 'star'

    def testScene1(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.drawing.add_shape(Rectangle(100, 100, 100, 50, QColor('transparent'), QColor('blue'), 2))
        self.drawingWidget.drawing.add_shape(Circle(300, 300, 30, QColor('transparent'), QColor('purple'), 7))
        self.drawingWidget.drawing.add_shape(Star(500, 200, 8, 50, 100, QColor('transparent'), QColor('yellow'), 4))
        self.drawingWidget.drawing.add_shape(Star(100, 500, 5, 50, 100, QColor('transparent'), QColor('black'), 10))
        self.drawingWidget.update()

    def testScene2(self):
        self.drawingWidget.drawing = Drawing()
        self.drawingWidget.drawing.add_shape(Rectangle(200, 200, 100, 100, QColor('light blue'), QColor('light green'), 2))
        self.drawingWidget.drawing.add_shape(Circle(500, 400, 50, QColor('light yellow'), QColor('red'), 2))
        self.drawingWidget.drawing.add_shape(Star(100, 500, 5, 50, 100, QColor('lavender'), QColor('black'), 4))
        self.drawingWidget.drawing.add_shape(Rectangle(100, 100, 50, 50, QColor('pink'), QColor('light blue'), 5))
        self.drawingWidget.update()

    def isHollow(self):
        if self.drawingWidget.hollowDrawing:
            self.drawingWidget.hollowDrawing = False
            self.drawingWidget.color1 = self.drawingWidget.color1Cache
        else:
            self.drawingWidget.hollowDrawing = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

