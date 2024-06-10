// get all the AWT/SWING components we need
import java.awt.BorderLayout 
import java.awt.Dimension
import java.awt.GridLayout
import javax.swing.JFrame
import javax.swing.JPanel
import javax.swing.JButton
import javax.swing.WindowConstants 
import javax.swing.JOptionPane

object SwingHellowWorld extends App { // a fancy way of creating an application 
    // some member functions, for later use
    def showSomeDialog(): Unit = {
        JOptionPane.showMessageDialog(null, "Hello World!"); 
    }
    def showAnswer(): Unit = {
        JOptionPane.showMessageDialog(null, "42!"); 
    }
    def doQuit(): Unit = { 
        mainWindow.setVisible(false) 
        mainWindow.dispose()
    }

    // member variables to remember all the components we need
    // first, two new buttons
    var buttonDialog = new JButton("show dialog") 
    var buttonAnswer = new JButton("show the answer to life, the universe, and everything") 
    var buttonQuit = new JButton("quit")
    // then, a panel, where the buttons are put into 
    var panel = new JPanel()
    // and a layout, for the panel to arrange the buttons
    var layout = new GridLayout(2,1) 
    panel.setLayout(layout)

    // we now add the buttons to the panel
    panel.add(buttonDialog)
    panel.add(buttonAnswer)
    panel.add(buttonQuit)
    
    // we connect member functions as events to be called to the buttons
    buttonDialog.addActionListener(e => showSomeDialog()) 
    buttonAnswer.addActionListener(e => showAnswer()) 
    buttonQuit.addActionListener(e => doQuit())
    
    // now we create the main window (simple window via type "JFrame")
    var mainWindow = new JFrame("Scala & Swing Example")
    // it also needs a layout
    mainWindow.getContentPane.add(panel, BorderLayout.CENTER)
    // when it is closed, the whole app should quit 
    mainWindow.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE) 
    // set some default size, why not VGA?
    mainWindow.setSize(new Dimension(640, 480)) 
    // center the new window on the screen 
    mainWindow.setLocationRelativeTo(null)
    //  show the window 
    mainWindow.setVisible(true)
    
}