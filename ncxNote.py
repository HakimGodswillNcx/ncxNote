#--------------------.
#future features list:
#--------------------'
#copy/past Other LABELS content.
#:::::::::::::::::::::::::::::::::::::::::::::::::::
import setproctitle
setproctitle.setproctitle("ncxNote")

import sys

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import os #we start by current directory detect
#any changing to folder names must be fixed from those lines
#THIS is THE ONLY HARDCORED VALUE (if you change any forlder name/s)

script_directory = os.path.dirname(os.path.abspath(__file__))
#output: /home/user_name/dir/to/ncxNote (folder)
notesDirectory=script_directory+"/source/txt/notes.txt"
#output: /home/user_name/dir/to/ncxNote/source/txt/notes.txt

#read notes from file
#noteMsg="""
#"""
txtNotesFile = open(notesDirectory) #DO NOT CHANGE VAR NAMES
noteMsg= txtNotesFile.read()
txtNotesFile.close() #end of folder manipulations ! (here)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#Global vars:
#::::::::::::
boolToSolid=False
boolAllMsgs=True
boolRawText=False

hardCoredOpacity=0.1 #this for preOpacity value for Qpainter (do NOT change)
incDecOpacity=0.9 #solid by default (do NOT change)

boolFullScreen=False #by default (do NOT change)

textColor="white"

moveUp = -10
moveDown = 10
moveLeft = -10
moveRight = 10
downUp = leftRight = 0

moveUpRaw = -10
moveDownRaw = 10
moveLeftRaw = -10
moveRightRaw = 10
downUpRaw = leftRightRaw = 0

heiTxt = widTxt = 500

logzMsg="""logz: program started, no errors.<br>
<br>
"""

helpMsg="""ctrl H = show help only <br>
alt  H = hide/show all msgs_labels. <br>
ctrl F = full screen. <br>
ctrl E = edit Note<br>
ctrl S = save note<br>
ctrl M = show LCDmsg only (old MemoMsg) <br>
ctrl L = show Logz only<br>
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::<br>
ctrl NumPad = moving main label around.<br>
Alt Numpad  = moving raw text editor around<br>
ctrl 0     = toggle solide on<br>
cltrl 5 = center all labels to (0,0)<br>
ctrl / and * for opacity 'increments' <br>
alt + or - = control text editor window size<br>
shift + and - = horizontal text editor size <br>
ctrl + or - = vertical text editor size <br>
::::::::::::::::::::::::::::::::::ubuntu:20::::::::::::::::::<br>
ctrl D = desktop show<br>
start TAB= switch to app window<br>
(custom) ctrl start N = open ncxNote.desktop (read docs how it's done)<br>
<br>
"""

lcdMsg="""LCD screen:<br>
to show custom memory values in a LOOP,<br>
from supposed to be custom function !<br>
<br>
"""

#===================

welcomeMsg= helpMsg #default message on startup ()


#CLASS customWindow(QMainWindow)
#===============================
class CustomWindow(QMainWindow):
    def paintEvent(self, event=None):
        global hardCoredOpacity
        painter = QPainter(self)
        painter.setOpacity(hardCoredOpacity)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black))   
        painter.drawRect(self.rect())

    def hideAllMsgs(self): #hide and show ALL msgs:
        global boolAllMsgs, lcdMsg, noteMsg
        global helpMsg, logzMsg, boolHelpOnly

        if boolAllMsgs==False:
            boolAllMsgs=True
            coloredMemoMsg='<font color="yellow">'+lcdMsg+'</font>'
            prefixWrapMsgs = "<font color='white' style='white-space: pre-wrap;'>"
            coloredNoteMsg=prefixWrapMsgs+noteMsg+"<br>"+"</font>"
            coloredLogzMsg='<font color="red">'+logzMsg+'</font>'
            allMsgs=coloredNoteMsg+coloredMemoMsg+coloredLogzMsg
            mainLabel.setText(allMsgs)
        elif boolAllMsgs==True:
            boolAllMsgs=False
            noMsgs= " "
            mainLabel.setText(noMsgs)

    def showHelpOnly(self):
        global helpMsg
        coloredHelpMsg='<font color="green">'+helpMsg+'</font>'
        mainLabel.setText(coloredHelpMsg)
        mainLabel.move(0, 0)
    def showNoteOnly(self):
        global NoteMsg
        coloredNoteMsg="<font color='red' style='white-space: pre-wrap;'>"+noteMsg+"</font>"
        mainLabel.setText(coloredNoteMsg)
        mainLabel.move(0, 0)
    def showLogzOnly(self):
        global logzMsg
        coloredlogzMsg='<font color="red">'+logzMsg+'</font>'
        mainLabel.setText(coloredlogzMsg)
        mainLabel.move(0, 0)
    def showMemoOnly(self):
        global lcdMsg
        coloredMemoMsg='<font color="yellow">'+lcdMsg+'</font>'
        mainLabel.setText(coloredMemoMsg)
        mainLabel.move(0, 0)

    def modeFullScreen(self):
        global boolFullScreen
        if boolFullScreen==False:
            boolFullScreen=True
            window.showFullScreen()
        elif boolFullScreen==True:
            boolFullScreen=False
            window.showNormal()

    def moveLabelRight(self):
        global moveRight, leftRight
        leftRight+=moveRight
        mainLabel.move(leftRight, downUp)
    def moveLabelUP(self):
        global moveUp, downUp
        downUp+=moveUp
        mainLabel.move(leftRight, downUp)
    def moveLabelLeft(self):
        global moveLeft, leftRight
        leftRight+=moveLeft
        mainLabel.move(leftRight, downUp)
    def moveLabelDown(self):
        global moveDown, downUp
        downUp+=moveDown
        mainLabel.move(leftRight, downUp)

    def moveRawRight(self):
        global moveRightRaw, leftRightRaw
        leftRightRaw+=moveRightRaw
        rawTextLabel.move(leftRightRaw, downUpRaw)
    def moveRawUp(self):
        global moveUpRaw, downUpRaw
        downUpRaw+=moveUpRaw
        rawTextLabel.move(leftRightRaw, downUpRaw)
    def moveRawLeft(self):
        global moveLeftRaw, leftRightRaw
        leftRightRaw+=moveLeftRaw
        rawTextLabel.move(leftRightRaw, downUpRaw)
    def moveRawDown(self):
        global moveDownRaw, downUpRaw
        downUpRaw+=moveDownRaw
        rawTextLabel.move(leftRightRaw, downUpRaw)

    def switchSolid(self):
        global boolToSolid
        global incDecOpacity
        if boolToSolid==False:
            boolToSolid=True
            opaSolid=incDecOpacity+1.0
            if opaSolid>=1.0:
                opaSolid=0.9
            opaSolidStr = str(opaSolid)
            opaSolidColor = "background: rgba(0, 0, 0, "+opaSolidStr+");"
            mainLabel.setStyleSheet(opaSolidColor + "color:white;")
        elif boolToSolid==True:
            boolToSolid=False
            incDecOpaStr = str(incDecOpacity)
            incDecOpaColor = "background: rgba(0, 0, 0, "+incDecOpaStr+");"
            mainLabel.setStyleSheet(incDecOpaColor + "color:white;")
    def incOpacity(self):
        global incDecOpacity
        if incDecOpacity<=0.9:
            incDecOpacity += 0.1
            incDecOpaStr = str(incDecOpacity)
            incDecOpaColor = "background: rgba(0, 0, 0, "+incDecOpaStr+");"
            mainLabel.setStyleSheet(incDecOpaColor + "color:white;")
    def decOpacity(self):
        global incDecOpacity
        if incDecOpacity>=0.1:
            incDecOpacity -= 0.1
            incDecOpaStr = str(incDecOpacity)
            incDecOpaColor = "background: rgba(0, 0, 0, "+incDecOpaStr+");"
            mainLabel.setStyleSheet(incDecOpaColor + "color:white;")
    def noteRawText(self):
        global noteMsg, boolRawText, downUp, leftRight, downUpRaw, leftRightRaw
        if boolRawText == False:
            boolRawText=True
            rawTextLabel.setPlainText(noteMsg)
            rawTextLabel.move(leftRightRaw,downUpRaw)
            rawTextLabel.show()
        elif boolRawText==True:
            boolRawText=False
            rawTextLabel.hide()
    def incSizeTxT(self):
        global heiTxt, widTxt
        heiTxt+=9
        widTxt+=9
        rawTextLabel.resize(heiTxt,widTxt)
    def decSizeTxT(self):
        global heiTxt, widTxt
        heiTxt-=9
        widTxt-=9
        rawTextLabel.resize(heiTxt,widTxt)
    def decSizeTxTvert(self):
        global heiTxt, widTxt
        heiTxt-=9
        rawTextLabel.resize(heiTxt,widTxt)
    def incSizeTxTvert(self):
        global heiTxt, widTxt
        heiTxt+=9
        rawTextLabel.resize(heiTxt,widTxt)
    def decSizeTxThori(self):
        global heiTxt, widTxt
        widTxt-=9
        rawTextLabel.resize(heiTxt,widTxt)
    def incSizeTxThori(self):
        global heiTxt, widTxt
        widTxt+=9
        rawTextLabel.resize(heiTxt,widTxt)
    def saveRawNote(self):
        global noteMsg
        noteMsg = rawTextLabel.toPlainText()
        #write to file
        txtNotesFile = open(notesDirectory,"w+")
        txtNotesFile.write(noteMsg)
        txtNotesFile.close()
    def zeroPose(self):
        global downUp, leftRight,downUpRaw, leftRightRaw
        downUpRaw = leftRightRaw = 0
        downUp = leftRight = 0
        mainLabel.move(0,0)
        rawTextLabel.move(0,0)




#============================================================ END of CLASS.

#settings variables init
#:::::::::::::::::::::::
hintFrameless = Qt.FramelessWindowHint #fullscreen
hintAlwaysOnTop = Qt.WindowStaysOnTopHint #windowed always on top
customWindowFlag=hintAlwaysOnTop #framed/framless = windowed/fullscreen

solidBackground=Qt.WA_NoSystemBackground
opacityBackground=Qt.WA_TranslucentBackground

#======================================================
#PROGRAM STARTS
#::::::::::::::
app = QApplication(sys.argv)
# Create the main window
window = CustomWindow()

#framed/framless = windowed/fullscreen
window.setWindowFlags(customWindowFlag)

#SOLID (switch)
window.setAttribute(solidBackground, True)
#opacity (switch)
window.setAttribute(opacityBackground, True)


# Create the Widget (MAIN opacity WINDOW/WIDGET)
mainWidget=QWidget(window)
mainWidget.setGeometry(QRect(0, 0, 55555, 55555))

# Create the Label (main)
mainLabel = QLabel(mainWidget)
mainLabel.setGeometry(QRect(0, 0, 55555, 55555))
mainLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
mainLabel.setStyleSheet("color:"+textColor+";")
mainLabel.setText(welcomeMsg)
mainLabel.setFont(QFont('Comic Sans MS', 22))
mainLabel.move(leftRight, downUp)
#===========================================QPlainTextEdit
# Create the copy/past (EFFECT)
rawTextLabel = QPlainTextEdit(mainWidget)
rawTextLabel.setGeometry(QRect(0, 0, heiTxt,widTxt))
rawTextLabel.setBackgroundVisible(True)
rawTextLabel.move(leftRightRaw, downUpRaw)
rawTextLabel.setFont(QFont('Ubuntu', 15))
rawTextLabel.setStyleSheet('background-color:#0080FF80;color:white;');
rawTextLabel.hide()
#=========================================================

# Run the application
window.setGeometry(QRect(0, 0, 333, 333))
window.show()
#window.showFullScreen()

#if conditions (SHORTCUTS)
#:::::::::::::::::::::::::
window.hideAllabels = QShortcut(QKeySequence('alt+h'), window)
window.hideAllabels.activated.connect(window.hideAllMsgs)
window.showHelp = QShortcut(QKeySequence('ctrl+h'), window)
window.showHelp.activated.connect(window.showHelpOnly)

window.showNote = QShortcut(QKeySequence('ctrl+n'), window)
window.showNote.activated.connect(window.showNoteOnly)
window.showLogz = QShortcut(QKeySequence('ctrl+l'), window)
window.showLogz.activated.connect(window.showLogzOnly)
window.showMemo = QShortcut(QKeySequence('ctrl+m'), window)
window.showMemo.activated.connect(window.showMemoOnly)

#moveLabelAround
window.moveTextRight = QShortcut(QKeySequence('ctrl+6'), window)
window.moveTextRight.activated.connect(window.moveLabelRight)
window.moveTextUP = QShortcut(QKeySequence('ctrl+8'), window)
window.moveTextUP.activated.connect(window.moveLabelUP)
window.moveTextLeft = QShortcut(QKeySequence('ctrl+4'), window)
window.moveTextLeft.activated.connect(window.moveLabelLeft)
window.moveTextDown = QShortcut(QKeySequence('ctrl+2'), window)
window.moveTextDown.activated.connect(window.moveLabelDown)

#move RAw TEXT arround (navigation) moveRawDown
window.moveRawTextRight = QShortcut(QKeySequence('alt+6'), window)
window.moveRawTextRight.activated.connect(window.moveRawRight)
window.moveRawTextUp = QShortcut(QKeySequence('alt+8'), window)
window.moveRawTextUp.activated.connect(window.moveRawUp)
window.moveRawTextLeft = QShortcut(QKeySequence('alt+4'), window)
window.moveRawTextLeft.activated.connect(window.moveRawLeft)
window.moveRawTextDown = QShortcut(QKeySequence('alt+2'), window)
window.moveRawTextDown.activated.connect(window.moveRawDown)

#switchSolid
window.switchToSolid = QShortcut(QKeySequence('ctrl+0'), window)
window.switchToSolid.activated.connect(window.switchSolid)
#showFullScreen
window.fullScreenMode = QShortcut(QKeySequence('ctrl+f'), window)
window.fullScreenMode.activated.connect(window.modeFullScreen)

#noteRawText
window.switchToRaw = QShortcut(QKeySequence('ctrl+e'), window)
window.switchToRaw.activated.connect(window.noteRawText)
#saveRawNote
window.saveRawText = QShortcut(QKeySequence('ctrl+s'), window)
window.saveRawText.activated.connect(window.saveRawNote)
#zeroPose
window.zeroPoseLabel = QShortcut(QKeySequence('ctrl+5'), window)
window.zeroPoseLabel.activated.connect(window.zeroPose)
#incOpacity
window.incOpaLabel = QShortcut(QKeySequence('ctrl+*'), window)
window.incOpaLabel.activated.connect(window.incOpacity)
#decOpacity
window.decOpaLabel = QShortcut(QKeySequence('ctrl+/'), window)
window.decOpaLabel.activated.connect(window.decOpacity)
#incSizeTxT
window.incSizeTxTLabel = QShortcut(QKeySequence("Alt++"), window)
window.incSizeTxTLabel.activated.connect(window.incSizeTxT)
#decSizeTxT
window.decSizeTxTLabel = QShortcut(QKeySequence('alt+-'), window)
window.decSizeTxTLabel.activated.connect(window.decSizeTxT)

#incSizeTxThori
window.incSizeTxThoriLabel = QShortcut(QKeySequence('ctrl++'), window)
window.incSizeTxThoriLabel.activated.connect(window.incSizeTxThori)
#decSizeTxThori
window.decSizeTxThoriLabel = QShortcut(QKeySequence('ctrl+-'), window)
window.decSizeTxThoriLabel.activated.connect(window.decSizeTxThori)
#decSizeTxTvert
window.decSizeTxTvertLabel = QShortcut(QKeySequence('shift+-'), window)
window.decSizeTxTvertLabel.activated.connect(window.decSizeTxTvert)
#incSizeTxTvert
window.incSizeTxTvertLabel = QShortcut(QKeySequence('shift++'), window)
window.incSizeTxTvertLabel.activated.connect(window.incSizeTxTvert)


#=================END OF PROGRAM.
window.switchSolid() #here is a_SOLID_color_BG-BY_DEFAULT.
#::::::::::::::::::::::::::::::::::::::::::::::::
#keep app opened until exit! (necessary) THE END.
sys.exit(app.exec_())
