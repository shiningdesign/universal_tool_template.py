'''
LNTextEdit v4.4
Text widget with support for line numbers
http://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/

mod: by ying - http://shining-lucy.com/wiki
v4.4 (2021.09.17):
  * add support for file path, file name drag and drop
v4.3 (2020.02.14): 
  * add monoFont function
v4.2
  * fix lineWrap cmd typo
v4.1
 * fix qt5 qpallete code in qtgui
v4.0
 * python 3 support
 * pyside, pyside2, pyqt4, pyqt5 support
v3.2
 * re/set/getFontSize and font size add zoom in out and scoll zoom event
v3.1.2
 * add unicode support url path name
v3.1 
 * add readyOnly function
 * add drag and drop function (multiple files)
 * add highlight toggle
 * add text return function
 * clean and update Qt code
 * remove qvariant and update more code to work for both pyside and pyqt
'''

# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    print("PySide Try")
    qtMode = 0
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        print("PySide2 Try")
        qtMode = 2
    except ImportError:
        try:
            from PyQt4 import QtGui,QtCore
            import PyQt4.QtGui as QtWidgets
            import sip
            qtMode = 1
            print("PyQt4 Try")
        except ImportError:
            from PyQt5 import QtGui,QtCore,QtWidgets
            import sip
            qtMode = 3
            print("PyQt5 Try")
import os
class LNTextEdit(QtWidgets.QFrame):
 
    class NumberBar(QtWidgets.QWidget):
 
        def __init__(self, edit):
            QtWidgets.QWidget.__init__(self, edit)
            
            self.edit = edit
            self.adjustWidth(1)
            
        def paintEvent(self, event):
            self.edit.numberbarPaint(self, event)
            QtWidgets.QWidget.paintEvent(self, event)
 
        def adjustWidth(self, count):
            width = self.fontMetrics().width(unicode(count))
            if self.width() != width:
                self.setFixedWidth(width)
 
        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                # It would be nice to do
                # self.update(0, rect.y(), self.width(), rect.height())
                # But we can't because it will not remove the bold on the
                # current line if word wrap is enabled and a new block is
                # selected.
                self.update()
                
    class PlainTextEdit(QtWidgets.QPlainTextEdit):
        def __init__(self, *args):
            QtWidgets.QPlainTextEdit.__init__(self, *args)
            self.setFrameStyle(QtWidgets.QFrame.NoFrame)
            self.zoomWheelEnabled = 0
            self.highlight()
            #self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
            self.cursorPositionChanged.connect(self.highlight)
        
        def dragEnterEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

        def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

        def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                mod = self.quickModKeyAsk()
                if mod == 1: # ctrl
                    txt = "\n".join( [ os.path.basename(unicode(url.path())[1:]) for url in urls] ) # remove 1st / char
                    self.insertPlainText( txt ) 
                elif mod == 6: # ctrl +shift
                    txt = "\n".join([os.path.dirname(unicode(urls[0].path())[1:])]+ [ os.path.basename(unicode(url.path())[1:]) for url in urls] ) # remove 1st / char
                    self.insertPlainText( txt ) 
                else:
                    txt = "\n".join( [unicode(url.path())[1:] for url in urls] ) # remove 1st / char
                    self.insertPlainText( txt ) 
        def zoom_in(self):
            font = self.document().defaultFont()
            size = font.pointSize()
            if size < 28:
                size += 2
                font.setPointSize(size)
            self.setFont(font)
        def zoom_out(self):
            font = self.document().defaultFont()
            size = font.pointSize()
            if size > 6:
                size -= 2
                font.setPointSize(size)
            self.setFont(font)
        def wheelEvent(self, event, forward=True):
            if event.modifiers() == QtCore.Qt.ControlModifier:
                if self.zoomWheelEnabled == 1:
                    if event.delta() == 120:
                        self.zoom_in()
                    elif event.delta() == -120:
                        self.zoom_out()
                event.ignore()
            QtWidgets.QPlainTextEdit.wheelEvent(self, event)
            
        def highlight(self):
            hi_selection = QtWidgets.QTextEdit.ExtraSelection()
 
            hi_selection.format.setBackground(self.palette().alternateBase())
            hi_selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, 1) #QtCore.QVariant(True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
 
            self.setExtraSelections([hi_selection])
 
        def numberbarPaint(self, number_bar, event):
            font_metrics = self.fontMetrics()
            current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1
 
            block = self.firstVisibleBlock()
            line_count = block.blockNumber()
            painter = QtGui.QPainter(number_bar)
            painter.fillRect(event.rect(), self.palette().base())
 
            # Iterate over all visible text blocks in the document.
            while block.isValid():
                line_count += 1
                block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
 
                # Check if the position of the block is out side of the visible
                # area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break
 
                # We want the line number for the selected line to be bold.
                if line_count == current_line:
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
                else:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)
 
                # Draw the line number right justified at the position of the line.
                paint_rect = QtCore.QRect(0, block_top, number_bar.width(), font_metrics.height())
                painter.drawText(paint_rect, QtCore.Qt.AlignRight, unicode(line_count))
 
                block = block.next()
 
            painter.end()
        def quickModKeyAsk(self):
            modifiers = QtWidgets.QApplication.queryKeyboardModifiers()
            clickMode = 0 # basic mode
            if modifiers == QtCore.Qt.ControlModifier:
                clickMode = 1 # ctrl
            elif modifiers == QtCore.Qt.ShiftModifier:
                clickMode = 2 # shift
            elif modifiers == QtCore.Qt.AltModifier:
                clickMode = 3 # alt
            elif modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier | QtCore.Qt.AltModifier:
                clickMode = 4 # ctrl+shift+alt
            elif modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier:
                clickMode = 5 # ctrl+alt
            elif modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                clickMode = 6 # ctrl+shift
            elif modifiers == QtCore.Qt.AltModifier | QtCore.Qt.ShiftModifier:
                clickMode = 7 # alt+shift
            return clickMode
    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)
 
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
 
        self.edit = self.PlainTextEdit()
        self.number_bar = self.NumberBar(self.edit)
 
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0,0,0,0) # setMargin
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
 
        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)
    
    def text(self):
        return unicode(self.edit.toPlainText())
    def clear(self):
        self.setText('')
    def getText(self):
        return unicode(self.edit.toPlainText())
    def setText(self, text):
        self.edit.setPlainText(text)
    def insertText(self, text):
        self.edit.insertPlainText(text)
    def addText(self, text):
        self.edit.setPlainText(self.edit.toPlainText()+text)
    def insertPlainText(self, text):
        self.insertText(text)
    def isModified(self):
        return self.edit.document().isModified() 
    def setModified(self, modified):
        self.edit.document().setModified(modified)
    
    def setLineWrapMode(self, mode):
        self.setWrap(mode)
    def setWrap(self, state):
        if state == 0:
            self.edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        else:
            self.edit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
    def setReadOnly(self, state):
        self.edit.setReadOnly(state)
    def setReadOnlyStyle(self, state):
        if state == 1:
            mainWindowBgColor = QtGui.QPalette().color(QtGui.QPalette.Window)
            self.setStyleSheet('QPlainTextEdit[readOnly="true"] { background-color: %s;} QFrame {border: 0px}' % mainWindowBgColor.name() )
            self.setHighlight(0)
        else:
            self.setStyleSheet('')
            self.setHighlight(1)
    def setFontSize(self, value):
        font = self.edit.document().defaultFont()
        if value > 6 and value < 28:
            font.setPointSize(value)
            self.edit.setFont(font)
    def getFontSize(self):
        font = self.edit.document().defaultFont()
        size = font.pointSize()
        return size
    def resetFontSize(self):
        font = self.edit.document().defaultFont()
        font.setPointSize(8)
        self.edit.setFont(font)
    def monoFont(self, state):
        if state == 1:
            self.edit.setStyleSheet('QPlainTextEdit {font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;}')
        else:
            self.edit.setStyleSheet('')
    def setZoom(self,mode):
        if mode == 0:
            self.edit.zoomWheelEnabled = 0
        else:
            self.edit.zoomWheelEnabled = 1
    def setHighlight(self, state):
        txtEdit = self.edit
        if state == 0:
            txtEdit.cursorPositionChanged.disconnect()
            txtEdit.setExtraSelections([])
        else:
            txtEdit.cursorPositionChanged.connect(txtEdit.highlight)
