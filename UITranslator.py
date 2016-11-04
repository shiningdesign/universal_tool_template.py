'''
UITranslator v1.0

based on Univeral Tool Template based v006.1
update: 2016.07.22
by ying

usage in maya: 
import UITranslator
UITranslator.main()

usage in commandline:
python UITranslator.py

'''
deskMode = 0
qtMode = 0 # 0: PySide; 1 : PyQt
try:
    import maya.OpenMayaUI as mui
except ImportError:
    deskMode = 1

# ==== for PyQt4 ====
#from PyQt4 import QtGui,QtCore
#import sip

# ==== for pyside ====
#from PySide import QtGui,QtCore
#import shiboken

# ==== auto Qt load ====
try:
    from PySide import QtGui,QtCore
    import shiboken
    qtMode = 0
except ImportError:
    from PyQt4 import QtGui,QtCore
    import sip
    qtMode = 1
    
from functools import partial
import sys

import LNTextEdit # for text edit code
import json # for file operation code
import os # for language code

# note: if you want to create a window with menu, then use QMainWindow Class
class UITranslator(QtGui.QMainWindow):
#class UITranslator(QtGui.QDialog):
    def __init__(self, parent=None, mode=0):
        QtGui.QMainWindow.__init__(self, parent)
        #QtGui.QDialog.__init__(self, parent)
        
        self.version="1.0"
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        
        self.fileType='.UITranslator_EXT'
        # mode: example for receive extra user input as parameter
        self.mode = 0
        if mode in [0,1]:
            self.mode = mode # mode validator
        
        self.location = ""
        if getattr(sys, 'frozen', False):
            # frozen - cx_freeze
            self.location = sys.executable
        else:
            # unfrozen
            self.location = os.path.realpath(__file__) # location: ref: sys.modules[__name__].__file__
            
        self.setupStyle()
        self.setupMenu() # only if you use QMainWindows Class
        self.setupWin()
        self.setupUI()
        self.Establish_Connections()
        self.loadData()
        self.loadLang()
        
    def setupStyle(self):
        # global app style setting for desktop
        if deskMode == 1:
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
            
    def setupMenu(self):
        self.quickMenu(['file_menu;&File','setting_menu;&Setting','help_menu;&Help'])
        cur_menu = self.uiList['setting_menu']
        self.quickMenuAction('setParaA_atn','Set Parameter &A','A example of tip notice.','setParaA.png', cur_menu)
        cur_menu.addSeparator()
        # for file menu
        cur_menu = self.uiList['file_menu']
        self.quickMenuAction('newLang_atn','&Add New Language','Add a new translation.','newLang.png', cur_menu)
        
        # for info review
        cur_menu = self.uiList['help_menu']
        self.quickMenuAction('helpDeskMode_atnNone','Desk Mode - {}'.format(deskMode),'Desktop Running Mode - 0: Maya Mode; 1: Desktop Mode.','', cur_menu)
        self.quickMenuAction('helpQtMode_atnNone','PyQt4 Mode - {}'.format(qtMode),'Qt Library - 0: PySide; 1: PyQt4.','', cur_menu)
        cur_menu.addSeparator()
        self.uiList['helpGuide_msg'] = "How to Use:\n1. Put source info in\n2. Click Process button\n3. Check result output\n4. Save memory info into a file."
        self.quickMenuAction('helpGuide_atnMsg','Usage Guide','How to Usge Guide.','helpGuide.png', cur_menu)
        
    def setupWin(self):
        self.setWindowTitle("UITranslator" + " - v" + self.version) 
        self.setGeometry(300, 300, 300, 300)
        # win icon setup
        path = os.path.join(os.path.dirname(self.location),'icons','UITranslator.png')
        self.setWindowIcon(QtGui.QIcon(path))
        # initial win drag position
        self.drag_position=QtGui.QCursor.pos()
        #self.resize(250,250)
        # - for frameless or always on top option
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # it will keep ui always on top of desktop, but to set this in Maya, dont set Maya as its parent
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # it will hide ui border frame, but in Maya, use QDialog instead as QMainWindow will disappear
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint) # best for Maya case with QDialog without parent, for always top frameless ui
        # - for transparent and non-regular shape ui
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # use it if you set main ui to transparent and want to use alpha png as irregular shape window
        #self.setStyleSheet("background-color: rgba(0, 0, 0,0);") # black color better white color for get better look of semi trans edge, like pre-mutiply
        
    def setupUI(self):
        #==============================
        
        # main_layout for QMainWindow
        main_widget = QtGui.QWidget()
        self.setCentralWidget(main_widget)        
        main_layout = self.quickLayout('vbox') # grid for auto fill window size
        main_widget.setLayout(main_layout)
        '''
        # main_layout for QDialog
        main_layout = self.quickLayout('vbox')
        self.setLayout(main_layout)
        '''
        
        #------------------------------
        # ui element creation part
        info_split = self.quickSplitUI( "info_split", self.quickUI(["dict_table;QTableWidget","source_txtEdit;LNTextEdit","result_txtEdit;LNTextEdit"]), "v" )
        fileBtn_layout = self.quickUI(["filePath_input;QLineEdit", "fileLoad_btn;QPushButton;Load", "fileLang_choice;QComboBox", "fileExport_btn;QPushButton;Export"],"fileBtn_QHBoxLayout")
        self.quickUI( [info_split, "process_btn;QPushButton;Process and Update Memory From UI", fileBtn_layout], main_layout)
        self.uiList["source_txtEdit"].setWrap(0)
        self.uiList["result_txtEdit"].setWrap(0)
        
        '''
        self.uiList['secret_btn'] = QtGui.QPushButton(self) # invisible but functional button
        self.uiList['secret_btn'].setText("")
        self.uiList['secret_btn'].setGeometry(0, 0, 50, 20)
        self.uiList['secret_btn'].setStyleSheet("QPushButton{background-color: rgba(0, 0, 0,0);} QPushButton:pressed{background-color: rgba(0, 0, 0,0); border: 0px;} QPushButton:hover{background-color: rgba(0, 0, 0,0); border: 0px;}")
        #:hover:pressed:focus:hover:disabled
        '''

    def Establish_Connections(self):
        # loop button and menu action to link to functions
        for ui_name in self.uiList.keys():
            if ui_name.endswith('_btn'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("clicked()"), getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            if ui_name.endswith('_atn'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("triggered()"), getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            if ui_name.endswith('_atnMsg') or ui_name.endswith('_btnMsg'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("triggered()"), getattr(self, ui_name[:-7]+"_message", partial(self.default_message,ui_name)))
        QtCore.QObject.connect(self.uiList["dict_table"].horizontalHeader(), QtCore.SIGNAL("sectionDoubleClicked(int)"), self.changeTableHeader)
        
    #############################################
    # UI Response functions
    ##############################################
    #-- ui actions
    def loadData(self):
        print("Load data")
        self.memoData['fileList']={}
    #~~~~~~~~~~~~~~~
    # custom ui function
    def newLang_action(self):
        if len(self.memoData['fileList'].keys()) == 0:
            print("You need have UI name structure loaded in order to create a new language.")
        else:
            text, ok = QtGui.QInputDialog.getText(self, 'New Translation Creation', 'Enter language file name (eg. lang_cn):')
            if ok:
                if text in self.memoData['fileList'].keys():
                    print("This Language already in the table.")
                else:
                    self.uiList['dict_table'].insertColumn(self.uiList['dict_table'].columnCount())
                    index = self.uiList['dict_table'].columnCount() - 1
                    self.uiList['dict_table'].setHorizontalHeaderItem(index, QtGui.QTableWidgetItem(text) )
    def changeTableHeader(self, index):
        table = self.uiList["dict_table"]
        oldHeader = str(table.horizontalHeaderItem(index).text())
        text, ok = QtGui.QInputDialog.getText(self, 'Change header label for column %d' % index,'Header:',QtGui.QLineEdit.Normal, oldHeader)
        if ok:
            if text in self.memoData['fileList'].keys():
                print("This Language already in the table.")
            else:
                table.setHorizontalHeaderItem(index, QtGui.QTableWidgetItem(text) )
    
    #~~~~~~~~~~~~~~
    # default ui function
    def process_action(self): # (optional)
        print("Process ....")
        self.source_ui_to_memory()
        print("Update Result")
        self.memory_to_result_ui()
        
    def default_action(self, ui_name):
        print("No action defined for this button: "+ui_name)
    def default_message(self, ui_name):
        msgName = ui_name[:-7]+"_msg"
        msg_txt = msgName + " is not defined in uiList."
        if msgName in self.uiList:
            msg_txt = self.uiList[msgName]
        tmpMsg = QtGui.QMessageBox()
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg_txt)
        tmpMsg.addButton("OK",QtGui.QMessageBox.YesRole)
        tmpMsg.exec_()
    
    #=======================================
    #- UI and RAM content update functions (optional)
    #=======================================
    def memory_to_source_ui(self):
        # update ui once memory gets update
        txt='\n'.join([row for row in self.memoData['fileList']])
        self.uiList['source_txtEdit'].setText(txt)
        # table
        table = self.uiList['dict_table']
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)
        
        headers = ["UI Name"]
        table.insertColumn(table.columnCount())
        for key in self.memoData['fileList']:
            headers.append(key)
            table.insertColumn(table.columnCount())
        table.setHorizontalHeaderLabels(headers)
        
        ui_name_ok = 0
        translate = 1
        for file in self.memoData['fileList']:
            for row, ui_name in enumerate(self.memoData['fileList'][file]):
                #create ui list
                if ui_name_ok == 0:
                    ui_item = QtGui.QTableWidgetItem(ui_name)
                    table.insertRow(table.rowCount())
                    table.setItem(row, 0, ui_item)
                translate_item = QtGui.QTableWidgetItem(self.memoData['fileList'][file][ui_name])
                table.setItem(row, translate, translate_item)
            ui_name_ok = 1
            translate +=1
    
    def memory_to_result_ui(self):
        # update result ui based on memory data
        txt='\n'.join([('Updated: '+row) for row in self.memoData['fileList']])
        self.uiList['result_txtEdit'].setText(txt)
    
    def source_ui_to_memory(self):
        # 1: get source content
        # 2: update memory
        table = self.uiList['dict_table']
        rowCnt = table.rowCount()
        colCnt = table.columnCount()
        
        if colCnt < 2:
            print("You need at least 2 column to make the valid ui-to-language data.")
        else:
            headers = [ str(table.horizontalHeaderItem(i).text()) for i in range(1,colCnt) ]
            for index, each_file in enumerate(headers):
                self.memoData['fileList'][each_file]={}
                col = index + 1
                for row in range(rowCnt):
                    ui_name = str(table.item(row,0).text())
                    if not table.item(row,col):
                        ui_txt = ""
                    else:
                        ui_txt = unicode(table.item(row,col).text())
                    self.memoData['fileList'][each_file][ui_name] = ui_txt
            print("Memory: update finished.")
            # update export combo box
            self.uiList['fileLang_choice'].clear()
            self.uiList['fileLang_choice'].addItems(self.memoData['fileList'].keys())
        # 3. process memory data and update result ui
        self.memory_to_result_ui()
        print("Process: process memory finished.")
        
    #=======================================
    #- File Operation functions (optional)
    #=======================================
    def fileExport_action(self):
        file=str(self.uiList['filePath_input'].text()).strip()
        # open file dialog if no text input for file path
        if file == "":
            file = QtGui.QFileDialog.getSaveFileName(self, "Save File","","RAW data (*.json);;Format Txt(*{});;AllFiles(*.*)".format(self.fileType))
            if isinstance(file, (list, tuple)): # for deal with pyside case
                file = file[0]
            else:
                file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            self.uiList['filePath_input'].setText(file)
            if file.endswith(self.fileType): # formated txt file
                lang = str( self.uiList['fileLang_choice'].currentText() )
                self.writeFormatFile(self.process_rawData_to_formatData(self.memoData['fileList'][lang]), file) 
            else:
                lang = str( self.uiList['fileLang_choice'].currentText() )
                self.writeRawFile(self.memoData['fileList'][lang], file) # raw json file
            self.uiList['result_txtEdit'].setText("File: '"+file+"' creation finished.")
    
    def fileLoad_action(self):
        file=str(self.uiList['filePath_input'].text()).strip()
        # open file dialog if no text input for file path
        if file == "":
            file = QtGui.QFileDialog.getOpenFileName(self, "Open File","","RAW data (*.json);;Format Txt(*{});;AllFiles(*.*)".format(self.fileType))
            if isinstance(file, (list, tuple)): # for deal with pyside case
                file = file[0]
            else:
                file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            fileName=os.path.splitext( os.path.basename(file) )[0]
            self.uiList['filePath_input'].setText(file)
            if file.endswith(self.fileType): # formated txt file loading
                self.memoData['fileList'][fileName] = self.process_formatData_to_rawData( self.readFormatFile(file) )
            else: 
                self.memoData['fileList'][fileName] = self.readRawFile(file) # raw json file loading
            self.memory_to_source_ui()
            self.uiList['result_txtEdit'].setText("File: '"+file+"' loading finished.")
        # update export combo box
        self.uiList['fileLang_choice'].clear()
        self.uiList['fileLang_choice'].addItems(self.memoData['fileList'].keys())
    
    def process_formatData_to_rawData(self, file_txt):
        # 1: prepare clean data from file Data
        file_data=[] # to implement here
        return file_data
    def process_rawData_to_formatData(self, memo_data):
        # 1: prepare memory data from file Data
        file_txt = '' # to implement here
        return file_txt
        
    #############################################
    # json and text data functions
    ##############################################
    def readRawFile(self,file):
        with open(file) as f:
            data = json.load(f)
        return data
    def writeRawFile(self, data, file):
        with open(file, 'w') as f:
            json.dump(data, f)
            
    # format data functions
    def readFormatFile(self, file):
        txt = ''
        with open(file) as f:
            txt = f.read()
        return txt
    def writeFormatFile(self, txt, file):    
        with open(file, 'w') as f:
            f.write(txt)
    #############################################
    # UI and Mouse Interaction functions
    ##############################################
    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.close()
    def mouseMoveEvent(self, event):
        if (event.buttons() == QtCore.Qt.LeftButton):
            self.move(event.globalPos().x() - self.drag_position.x(),
                event.globalPos().y() - self.drag_position.y())
        event.accept()
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.drag_position = event.globalPos() - self.pos()
        event.accept()
    #############################################
    # UI language functions
    ##############################################
    def loadLang(self):
        self.quickMenu(['language_menu;&Language'])
        cur_menu = self.uiList['language_menu']
        self.quickMenuAction('langDefault_atnLang', 'Default','','langDefault.png', cur_menu)
        cur_menu.addSeparator()
        QtCore.QObject.connect( self.uiList['langDefault_atnLang'], QtCore.SIGNAL("triggered()"), partial(self.setLang, 'default') )
        # store default language
        self.memoData['lang']={}
        self.memoData['lang']['default']={}
        for ui_name in self.uiList:
            ui_element = self.uiList[ui_name]
            if type(ui_element) in [ QtGui.QLabel, QtGui.QPushButton, QtGui.QAction, QtGui.QCheckBox ]:
                # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                self.memoData['lang']['default'][ui_name] = str(ui_element.text())
            elif type(ui_element) in [ QtGui.QGroupBox, QtGui.QMenu ]:
                # uiType: QMenu, QGroupBox
                self.memoData['lang']['default'][ui_name] = str(ui_element.title())
            elif type(ui_element) in [ QtGui.QTabWidget]:
                # uiType: QTabWidget
                tabCnt = ui_element.count()
                tabNameList = []
                for i in range(tabCnt):
                    tabNameList.append(str(ui_element.tabText(i)))
                self.memoData['lang']['default'][ui_name]=';'.join(tabNameList)
            elif type(ui_element) == str:
                # uiType: string for msg
                self.memoData['lang']['default'][ui_name] = self.uiList[ui_name]
        
        # try load other language
        lang_path = os.path.dirname(self.location) # better in packed than(os.path.abspath(__file__))
        baseName = os.path.splitext( os.path.basename(self.location) )[0]
        for fileName in os.listdir(lang_path):
            if fileName.startswith(baseName+"_lang_"):
                langName = fileName.replace(baseName+"_lang_","").split('.')[0].replace(" ","")
                self.memoData['lang'][ langName ] = self.readRawFile( os.path.join(lang_path,fileName) )
                self.quickMenuAction(langName+'_atnLang', langName.upper(),'',langName + '.png', cur_menu)
                QtCore.QObject.connect( self.uiList[langName+'_atnLang'], QtCore.SIGNAL("triggered()"), partial(self.setLang, langName) )
        # if no language file detected, add export default language option
        if len(self.memoData['lang']) == 1:
            self.quickMenuAction('langExport_atnLang', 'Export Default Language','','langExport.png', cur_menu)
            QtCore.QObject.connect( self.uiList['langExport_atnLang'], QtCore.SIGNAL("triggered()"), self.exportLang )
    def setLang(self, langName):
        uiList_lang_read = self.memoData['lang'][langName]
        for ui_name in uiList_lang_read:
            ui_element = self.uiList[ui_name]
            if type(ui_element) in [ QtGui.QLabel, QtGui.QPushButton, QtGui.QAction, QtGui.QCheckBox ]:
                # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                if uiList_lang_read[ui_name] != "":
                    ui_element.setText(uiList_lang_read[ui_name])
            elif type(ui_element) in [ QtGui.QGroupBox, QtGui.QMenu ]:
                # uiType: QMenu, QGroupBox
                if uiList_lang_read[ui_name] != "":
                    ui_element.setTitle(uiList_lang_read[ui_name])
            elif type(ui_element) in [ QtGui.QTabWidget]:
                # uiType: QTabWidget
                tabCnt = ui_element.count()
                if uiList_lang_read[ui_name] != "":
                    tabNameList = uiList_lang_read[ui_name].split(';')
                    if len(tabNameList) == tabCnt:
                        for i in range(tabCnt):
                            if tabNameList[i] != "":
                                ui_element.setTabText(i,tabNameList[i])
            elif type(ui_element) == str:
                # uiType: string for msg
                if uiList_lang_read[ui_name] != "":
                    self.uiList[ui_name] = uiList_lang_read[ui_name]
    def exportLang(self):
        file = QtGui.QFileDialog.getSaveFileName(self, "Export Default UI Language File","","RAW data (*.json);;AllFiles(*.*)")
        if isinstance(file, (list, tuple)): # for deal with pyside case
            file = file[0]
        else:
            file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            self.writeRawFile( self.memoData['lang']['default'], file )
            self.quickMsg("Languge File created: '"+file)
    #############################################
    # quick ui function for speed up programming
    ##############################################
    def quickMenu(self, ui_names):
        if isinstance(self, QtGui.QMainWindow):
            menubar = self.menuBar()
            for each_ui in ui_names:
                createOpt = each_ui.split(';')
                if len(createOpt) > 1:
                    uiName = createOpt[0]
                    uiLabel = createOpt[1]
                    self.uiList[uiName] = QtGui.QMenu(uiLabel)
                    menubar.addMenu(self.uiList[uiName])
        else:
            print("Warning (QuickMenu): Only QMainWindow can have menu bar.")
        
    def quickMenuAction(self, objName, title, tip, icon, menuObj):
        self.uiList[objName] = QtGui.QAction(QtGui.QIcon(icon), title, self)        
        self.uiList[objName].setStatusTip(tip)
        menuObj.addAction(self.uiList[objName])

    def quickUI(self, ui_names, parentLayout="", opt=""):
        # quick ui for hbox, vbox, grid, form layout
        # example: vbox, hbox, grid
        # quickUI(['mod_check;QCheckBox;Good One?','mod_space;QSpaceItem;(20,20,0,0)','modAct_btn;QPushButton;Build Module','mod_input;QLineEdit'],"baseProc_QHBoxLayout")
        # example: form
        # quickUI(['mod_check@Label A;QCheckBox','mod_input@Name B;QLineEdit','mod_choice@Type C;QComboBox;(AAA,BBB)'],"baseProc_QFormLayout")
        tmp_ui_list = []
        tmp_ui_label = [] # for form layout
        form_type = 0 # for form layout
        
        if not isinstance(ui_names, list):
            print("Error (QuickUI):  require string list as ui creation input")
            return
        for each_ui in ui_names:
            # create if it is string
            if not isinstance(each_ui, str):
                if isinstance(each_ui, QtGui.QWidget) or isinstance(each_ui, QtGui.QLayout) or isinstance(each_ui, QtGui.QSpacerItem):
                    tmp_ui_list.append(each_ui)
                    tmp_ui_label.append("")
                else:
                    print("Warning (QuickUI): Currently only support string ui creation or qwidget and qlayout object insertion.")
            else:
                # get Qt elements option
                createOpt = each_ui.split(';')
                uiNameLabel = createOpt[0].split('@')
                uiName = uiNameLabel[0]
                uiLabel = uiNameLabel[1] if len(uiNameLabel) > 1 else ""
                if len(uiNameLabel) > 1:
                    form_type = 1 
                uiType = createOpt[1] if len(createOpt) > 1 else ""
                uiArgs = createOpt[2] if len(createOpt) > 2 else ""
                
                # create qt elemeent
                if uiType == "":
                    print uiType
                    print("Warning (QuickUI): uiType is empty, current ui is not created.")
                else:
                    ui_create_state = 0
                    if not uiType[0] == 'Q':
                        # if 3rd ui, it create like UI_Class.UI_Class()
                        self.uiList[uiName] = getattr(eval(uiType), uiType)()
                        tmp_ui_list.append(self.uiList[uiName])
                        ui_create_state = 1
                    else:
                        if uiArgs == "":
                            self.uiList[uiName] = getattr(QtGui, uiType)()
                            tmp_ui_list.append(self.uiList[uiName])
                            ui_create_state = 1
                        else:
                            arg_list = uiArgs.replace('(','').replace(')','').split(',')
                            if not ( uiArgs.startswith("(") and uiArgs.endswith(")") ):
                                self.uiList[uiName] = getattr(QtGui, uiType)(uiArgs)
                                tmp_ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            else:
                                if uiType == 'QComboBox':
                                    self.uiList[uiName] = QtGui.QComboBox()
                                    self.uiList[uiName].addItems(arg_list)
                                    tmp_ui_list.append(self.uiList[uiName])
                                    ui_create_state = 1
                                elif uiType == 'QSpacerItem':
                                    policyList = ( QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Ignored)
                                    # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
                                    # factors in fighting for space: horizontalStretch
                                    # extra space: setContentsMargins and setSpacing
                                    # ref: http://www.cnblogs.com/alleyonline/p/4903337.html
                                    arg_list = [ int(x) for x in arg_list ]
                                    self.uiList[uiName] = QtGui.QSpacerItem(arg_list[0],arg_list[1], policyList[arg_list[2]], policyList[arg_list[3]] )
                                    tmp_ui_list.append(self.uiList[uiName])
                                    ui_create_state = 1
                                else:
                                    print("Warning (QuickUI): This Object type : "+uiType+" is not implemented in quickUI function.")
                    # if ui create ok, create its label
                    if ui_create_state == 1:
                        if not uiLabel == "":
                            uiLabel = QtGui.QLabel(uiLabel) # create label widget if label not empty
                            self.uiList[uiName+'_label'] = uiLabel
                        tmp_ui_label.append(uiLabel)
                    ui_create_state = 0
        
        if parentLayout == "":
            # - has no layout input, then
            if form_type == 1:
                return (tmp_ui_list, tmp_ui_label)
            else:
                return tmp_ui_list
        else:
            # - has layout input, then
            # create parentLayout if not a layout object there
            if isinstance(parentLayout, str):
                layout_type = parentLayout.split('_')[-1]
                type_txt = "vbox"
                if layout_type == "QHBoxLayout":
                    type_txt = "hbox"
                elif layout_type == "QFormLayout":
                    type_txt = "form"
                elif layout_type == "QGridLayout":
                    type_txt = "grid"
                parentLayout = self.quickLayout(type_txt, parentLayout)
            # layout ready, add widgets
            if isinstance(parentLayout, QtGui.QBoxLayout):
                for each_ui in tmp_ui_list:
                    if isinstance(each_ui, QtGui.QWidget):
                        parentLayout.addWidget(each_ui)
                    elif isinstance(each_ui, QtGui.QSpacerItem):
                        parentLayout.addItem(each_ui)
                    elif isinstance(each_ui, QtGui.QLayout):
                        parentLayout.addLayout(each_ui)
            elif isinstance(parentLayout, QtGui.QGridLayout):
                # one row/colume operation only
                insertRow = parentLayout.rowCount()
                insertCol = parentLayout.columnCount()
                for i in range(len(tmp_ui_list)):
                    each_ui = tmp_ui_list[i]
                    x = insertRow if opt=="h" else i
                    y = i if opt=="h" else insertCol
                    if isinstance(each_ui, QtGui.QWidget):
                        parentLayout.addWidget(each_ui,x,y)
                    elif isinstance(each_ui, QtGui.QSpacerItem):
                        parentLayout.addItem(each_ui,x,y)
                    elif isinstance(each_ui, QtGui.QLayout):
                        parentLayout.addLayout(each_ui,x,y)
            elif isinstance(parentLayout, QtGui.QFormLayout):
                for i in range(len(tmp_ui_list)):
                    each_ui = tmp_ui_list[i]
                    if isinstance(each_ui, QtGui.QWidget) or isinstance(each_ui, QtGui.QLayout):
                        parentLayout.addRow(tmp_ui_label[i], each_ui)
            else:
                print("Warning (QuickUI): Currently quickUI only support vbox, hbox, form and grid layout.")
            
            return parentLayout
            
    def quickLayout(self, type, ui_name=""):
        the_layout = QtGui.QVBoxLayout()
        if type == "form":
            the_layout = QtGui.QFormLayout()
            the_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
            the_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)    
        elif type == "grid":
            the_layout = QtGui.QGridLayout()
        elif type == "hbox":
            the_layout = QtGui.QHBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        else:        
            the_layout = QtGui.QVBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        if ui_name != "":
            self.uiList[ui_name] = the_layout
        return the_layout
        
    def quickSplitUI(self, name, part_list, type):
        split_type = QtCore.Qt.Horizontal
        if type == 'v':
            split_type = QtCore.Qt.Vertical
        self.uiList[name]=QtGui.QSplitter(split_type)
        
        for each_part in part_list:
            if isinstance(each_part, QtGui.QWidget):
                self.uiList[name].addWidget(each_part)
            else:
                tmp_holder = QtGui.QWidget()
                tmp_holder.setLayout(each_part)
                self.uiList[name].addWidget(tmp_holder)
        return self.uiList[name]
        
    def quickTabUI(self, name, tab_list, tab_names):
        self.uiList[name]=QtGui.QTabWidget()
        self.uiList[name].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
        for i in range( len(tab_list) ):
            each_tab = tab_list[i]
            each_name = tab_names[i]
            if isinstance(each_tab, QtGui.QWidget):
                self.uiList[name].addTab(each_tab, each_name)
            else:
                tmp_holder = QtGui.QWidget()
                tmp_holder.setLayout(each_tab)
                self.uiList[name].addTab(tmp_holder, each_name)
        return self.uiList[name]
        
    def quickMsg(self, msg):
        tmpMsg = QtGui.QMessageBox() # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg)
        tmpMsg.addButton("OK",QtGui.QMessageBox.YesRole)
        tmpMsg.exec_()
    def quickMsgAsk(self, msg):
        txt, ok = QtGui.QInputDialog.getText(self, "Input", msg)
        return (str(txt), ok)
#############################################
# window instance creation
##############################################
# If you want to be able to Keep only one copy of windows ui, use code below
single_UITranslator = None   
def main():
    parentWin = None
    app = None
    if deskMode == 0:
        if qtMode == 0:
            # ==== for pyside ====
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)
        elif qtMode == 1:
            # ==== for PyQt====
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
    if deskMode == 1:
        app = QtGui.QApplication(sys.argv)
    
    # single UI window code, so no more duplicate window instance when run this function
    global single_UITranslator
    if single_UITranslator is None:
        single_UITranslator = UITranslator(parentWin) # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_UITranslator.show()
    
    if deskMode == 1:
        sys.exit(app.exec_())
    
    # example: show ui stored
    print(single_UITranslator.uiList.keys())
    return single_UITranslator
    
# If you want to be able to load multiple windows of the same ui, use code below
'''
def main():
    parentWin = None
    if deskMode == 0:
        if qtMode == 0:
            # ==== for pyside ====
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)
        elif qtMode == 1:
            # ==== for PyQt====
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
            
    ui = UITranslator(parentWin) # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    ui.show()
    # example: show ui stored
    print(ui.uiList.keys())
    return ui
'''
if __name__ == "__main__":
    main()