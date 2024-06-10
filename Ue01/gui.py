# import all the widgets
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QFrame, QMessageBox

# only needed for command line arguments
import sys

# we define our own window type to build a custom UI
class MyWindow(QMainWindow):

    def quit_app(self): 
        # closing the last (and only) window ends the application 
        self.close()

    def show_dialog(self):
        # open a simple dialog window to say hello
        QMessageBox.question(self, "Some message...", "Hello World!", QMessageBox.Ok)

    def everything(self):
        QMessageBox.question(self, "Some message...", "42", QMessageBox.Ok)

    def __init__(self, parent): 
        # call parent constructor
        super().__init__(parent)

        # a bit of housekeeping...
        
        # set a frame object (empty container) that fills the whole window
        self.frame = QFrame(self)
        # make this the content of the main window 
        self.setCentralWidget(self.frame)
        # create a layout object
        self.my_layout = QVBoxLayout(self.frame)
        # tell the frame (just created) to use this layout 
        self.frame.setLayout(self.my_layout)
        
        # make a button!
        
        # create a button, remember in a member variable
        self.btn_dialog = QPushButton("show dialog")
        # connect button to method of self object 
        self.btn_dialog.clicked.connect(self.show_dialog) 
        # add the button to the UI via the layout object 
        self.my_layout.addWidget(self.btn_dialog)

        # button 42
        self.btn_dialog = QPushButton("show the answer to life, the universe, and everything")
        self.btn_dialog.clicked.connect(self.everything) 
        self.my_layout.addWidget(self.btn_dialog)

        # same procedure again...
        self.btn_quit = QPushButton("quit")
        self.btn_quit.clicked.connect(self.quit_app) 
        self.my_layout.addWidget(self.btn_quit)

# our main program starts here, Python-style
if __name__ == "__main__":

    # create an application object (needs cmd-line arguments)
    app: QApplication = QApplication(sys.argv)

    # Create the main window.
    main_window: MyWindow = MyWindow(None) 
    main_window.show()

    # Start the event loop.
    # Ends only after closing the main window 
    app.exec_()