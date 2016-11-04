'''
Univeral Tool Template v007
by ying - http://shining-lucy.com/wiki

log:
v007.3: 2016.10.13
  * add functions for convert between Maya built-in UI creation and Qt Widget Object, 
  * Qt use object pointer reference, Maya use object name
v007.2: 2016.09.20
  * fix layout margin clear
  * add quickPolicy
  * add quickInfo for quick notify and feedback, user customizable
v007: 2016.09.09
  * v7.1: fix btnMsg issue
  * rewrite quickUI, backward compatible, and also optimized label creation for form layout, only create label when needed
  * enable you to directly nest quickUI inside quickUI with various return type,
    * eg. self.quickUI([self.quickUI(), self.quickUI()], 'main_vbox')
  * enable you to quickUI with tab, split, groupbox as layout object, same creation string syntax as element
  * a even compact pure text based UI creation and reference function on top of quickUI, called "qui()"
v006.2: 2016.09.01
  * add utf8 support
  * better structure for fast template update
v006.1.2:
  - add hotkey example
  - add self.memoData['data'] for default, since not affect self.memoData['lang']
v006.1:
  - self location and location for load lang
  - window icon support and window intitial drag position
  - quickMsgAsk for user input
  - quickTabUI (no tab name lang out yet)
  - improve lang functions
  - fix qmenu creation for lang function
  - fix file icon template name
v005: 2016.07.30 
- add translation and stype function, better grid layout
v004: 2016.07.28
v003: 2016.07.22

usage in maya: 
import TMP_UniversalToolUI_TND
TMP_UniversalToolUI_TND.main()

usage in commandline:
python TMP_UniversalToolUI_TND.py
'''
tpl_ver = 7.3
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

########################################


import LNTextEdit # for text edit code
import json # for file operation code
import os # for language code

# note: if you want to create a window with menu, then use QMainWindow Class
class TMP_UniversalToolUI_TND(QtGui.QMainWindow):
#class TMP_UniversalToolUI_TND(QtGui.QDialog):
    def __init__(self, parent=None, mode=0):
        QtGui.QMainWindow.__init__(self, parent)
        #QtGui.QDialog.__init__(self, parent)
        
        self.version="0.1"
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        
        self.fileType='.TMP_UniversalToolUI_TND_EXT'
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
        
        #~~~~~~~~~~~~~~~~~~
        # initial data
        #~~~~~~~~~~~~~~~~~~
        self.memoData['data']=[]
        
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
        self.uiList['setParaA_atn'].setShortcut(QtGui.QKeySequence("Ctrl+R"))
        cur_menu.addSeparator()
        # for info review
        cur_menu = self.uiList['help_menu']
        self.quickMenuAction('helpDeskMode_atnNone','Desk Mode - {}'.format(deskMode),'Desktop Running Mode - 0: Maya Mode; 1: Desktop Mode.','', cur_menu)
        self.quickMenuAction('helpQtMode_atnNone','PyQt4 Mode - {}'.format(qtMode),'Qt Library - 0: PySide; 1: PyQt4.','', cur_menu)
        self.quickMenuAction('helpTemplate_atnNone','Universal Tool Teamplate - {}'.format(tpl_ver),'based on Univeral Tool Template v7 by Shining Ying - http://shining-lucy.com','', cur_menu)
        cur_menu.addSeparator()
        self.uiList['helpGuide_msg'] = "How to Use:\n1. Put source info in\n2. Click Process button\n3. Check result output\n4. Save memory info into a file."
        self.quickMenuAction('helpGuide_atnMsg','Usage Guide','How to Usge Guide.','helpGuide.png', cur_menu)
        
    def setupWin(self):
        self.setWindowTitle("TMP_UniversalToolUI_TND" + " - v" + self.version) 
        self.setGeometry(300, 300, 800, 600)
        # win icon setup
        path = os.path.join(os.path.dirname(self.location),'icons','TMP_UniversalToolUI_TND.png')
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
    
    def qui(self, ui_list_string, parentObject_string='', opt=''):
        # pre-defined user short name syntax
        type_dict = {
            'vbox': 'QVBoxLayout','hbox':'QHBoxLayout','grid':'QGridLayout', 'form':'QFormLayout',
            'split': 'QSplitter', 'grp':'QGroupBox', 'tab':'QTabWidget',
            'btn':'QPushButton', 'btnMsg':'QPushButton', 'label':'QLabel', 'input':'QLineEdit', 'check':'QCheckBox', 'choice':'QComboBox',
            'txtEdit': 'LNTextEdit', 'txt': 'QTextEdit',
            'tree': 'QTreeWidget',
            'space': 'QSpacerItem', 
        }
        # get ui_list, creation or existing ui object
        ui_list = [x.strip() for x in ui_list_string.split('|')]
        for i in range(len(ui_list)):
            if ui_list[i] in self.uiList:
                # - exisiting object
                ui_list[i] = self.uiList[ui_list[i]]
            else:
                # - string creation: 
                # get part info
                partInfo = ui_list[i].split(';',1)
                uiName = partInfo[0].split('@')[0]
                uiType = uiName.rsplit('_',1)[-1]
                if uiType in type_dict:
                    uiType = type_dict[uiType]
                # set quickUI string format
                ui_list[i] = partInfo[0]+';'+uiType
                if len(partInfo)==1:
                    # give empty button and label a place holder name
                    if uiType in ('btn', 'btnMsg', 'QPushButton','label', 'QLabel'):
                        ui_list[i] = partInfo[0]+';'+uiType + ';'+uiName 
                elif len(partInfo)==2:
                    ui_list[i]=ui_list[i]+";"+partInfo[1]
        # get parentObject or exisiting object
        parentObject = parentObject_string
        if parentObject in self.uiList:
            parentObject = self.uiList[parentObject]
        # process quickUI
        self.quickUI(ui_list, parentObject, opt)
        
    def setupUI(self):
        #==============================
        
        # main_layout for QMainWindow
        main_widget = QtGui.QWidget()
        self.setCentralWidget(main_widget)        
        main_layout = self.quickLayout('vbox', 'main_layout') # grid for auto fill window size
        main_widget.setLayout(main_layout)
        '''
        # main_layout for QDialog
        main_layout = self.quickLayout('vbox', 'main_layout')
        self.setLayout(main_layout)
        '''
        
        #------------------------------
        # ui element creation part
        # quickUI version from universal tool template v6
        '''
        upper_layout = self.quickUI(["source_txtEdit;LNTextEdit","process_btn;QPushButton;Process and Update"],"upper_QVBoxLayout")
        upper_layout.setContentsMargins(0,0,0,0)
        
        input_split = self.quickSplitUI("input_split", [ upper_layout, self.quickUI(["result_txtEdit;LNTextEdit"])[0] ], "v")
        fileBtn_layout = self.quickUI(["filePath_input;QLineEdit", "fileLoad_btn;QPushButton;Load", "fileExport_btn;QPushButton;Export"],"fileBtn_QHBoxLayout")
        self.quickUI([input_split, fileBtn_layout], main_layout)
        self.uiList["source_txtEdit"].setWrap(0)
        self.uiList["result_txtEdit"].setWrap(0)
        '''

        #------------------------------
        # qui version from template 7
        # no extra variable name, all text based creation and reference

        self.qui('source_txtEdit | process_btn;Process and Update', 'upper_vbox')
        self.qui('upper_vbox | result_txtEdit', 'input_split;v')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('input_split | fileBtn_layout', 'main_layout')
        self.uiList["source_txtEdit"].setWrap(0)
        self.uiList["result_txtEdit"].setWrap(0)        
        
        '''
        self.uiList['secret_btn'] = QtGui.QPushButton(self) # invisible but functional button
        self.uiList['secret_btn'].setText("")
        self.uiList['secret_btn'].setGeometry(0, 0, 50, 20)
        self.uiList['secret_btn'].setStyleSheet("QPushButton{background-color: rgba(0, 0, 0,0);} QPushButton:pressed{background-color: rgba(0, 0, 0,0); border: 0px;} QPushButton:hover{background-color: rgba(0, 0, 0,0); border: 0px;}")
        #:hover:pressed:focus:hover:disabled
        '''
        #------------- end ui creation --------------------
        for name,each in self.uiList.items():
            if isinstance(each, QtGui.QLayout) and name!='main_layout' and not name.endswith('_grp_layout'):
                each.setContentsMargins(0,0,0,0)
        self.quickInfo('Ready')

    def Establish_Connections(self):
        # loop button and menu action to link to functions
        for ui_name in self.uiList.keys():
            if ui_name.endswith('_btn'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("clicked()"), getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_atn'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("triggered()"), getattr(self, ui_name[:-4]+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_btnMsg'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("clicked()"), getattr(self, ui_name[:-7]+"_message", partial(self.default_message,ui_name)))
            elif ui_name.endswith('_atnMsg'):
                QtCore.QObject.connect(self.uiList[ui_name], QtCore.SIGNAL("triggered()"), getattr(self, ui_name[:-7]+"_message", partial(self.default_message,ui_name)))
        # custom connection
    
    #=======================================
    # UI Response functions (custom + prebuilt functions)
    #=======================================
    #-- ui actions
    def loadData(self):
        print("Load data")
    def quickInfo(self, info):
        self.statusBar().showMessage(info)
        
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
        txt='\n'.join([row for row in self.memoData['data']])
        self.uiList['source_txtEdit'].setText(txt)
    
    def memory_to_result_ui(self):
        # update result ui based on memory data
        txt='\n'.join([('>>: '+row) for row in self.memoData['data']])
        self.uiList['result_txtEdit'].setText(txt)
    
    def source_ui_to_memory(self):
        # 1: get source content
        source_txt = unicode(self.uiList['source_txtEdit'].text())
        # 2: update memory
        self.memoData['data'] = [row.strip() for row in source_txt.split('\n')]
        print("Memory: update finished.")
        # 3. process memory data and update result ui
        self.memory_to_result_ui()
        print("Process: process memory finished.")
    
    #=======================================
    #- File Operation functions (optional and custom functions)
    #=======================================
    def fileExport_action(self):
        file=str(self.uiList['filePath_input'].text())
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
                self.writeFormatFile(self.process_rawData_to_formatData(self.memoData['data']), file) 
            else: 
                self.writeRawFile(self.memoData['data'], file) # raw json file
            self.quickInfo("File: '"+file+"' creation finished.")
    
    def fileLoad_action(self):
        file=str(self.uiList['filePath_input'].text())
        # open file dialog if no text input for file path
        if file == "":
            file = QtGui.QFileDialog.getOpenFileName(self, "Open File","","RAW data (*.json);;Format Txt(*{});;AllFiles(*.*)".format(self.fileType))
            if isinstance(file, (list, tuple)): # for deal with pyside case
                file = file[0]
            else:
                file = str(file) # for deal with pyqt case
        # read file if open file dialog not cancelled
        if not file == "":
            self.uiList['filePath_input'].setText(file)
            if file.endswith(self.fileType): # formated txt file loading
                self.memoData['data'] = self.process_formatData_to_rawData( self.readFormatFile(file) )
            else: 
                self.memoData['data'] = self.readRawFile(file) # raw json file loading
            self.memory_to_source_ui()
            self.quickInfo("File: '"+file+"' loading finished.")
    
    def process_formatData_to_rawData(self, file_txt):
        # 1: prepare clean data from file Data
        file_data=[] # to implement here
        return file_data
    def process_rawData_to_formatData(self, memo_data):
        # 1: prepare memory data from file Data
        file_txt = '' # to implement here
        return file_txt
        
    #############################################################
    #############################################################
    # ----------------- CORE TEMPLATE FUNCTIONS -----------------
    #############################################################
    # dont touch code below
    #############################################
    # json and text data functions
    #############################################
    def readRawFile(self,file):
        with open(file) as f:
            data = json.load(f)
        return data
    def writeRawFile(self, data, file):
        with open(file, 'w') as f:
            json.dump(data, f)
            
    # format data functions
    def readFormatFile(self, file):
        with open(file) as f:
            txt = f.read()
        return txt
    def writeFormatFile(self, txt, file):    
        with open(file, 'w') as f:
            f.write(txt)
    #############################################
    # UI and Mouse Interaction functions
    #############################################
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
    #############################################
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
    #############################################
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
    
    def quickUI(self, part_list, parentObject="", insert_opt=""):
        # part_list contains: 
        # -- 1. string (strings for widget/space, layout, container[group, tab, splitter])
        # -- 2. object (widget/space, layout, container[group, tab, splitter])
        # -- 3. object list 
        # -- 4. [object list, label_object list]
        # parentObject contains:
        # -- 1. string (strings for layout, container[group, tab, splitter])
        # -- 2. object (layout, container[group, tab, splitter])
        # insert_opt:
        # -- insert into grid layout, h, v
        # -- insert into tab, titles
        if not isinstance(part_list, (list, tuple)):
            part_list = [part_list]
        # func variable
        ui_list = []
        ui_label_list = []
        form_type = 0 # flag for store whether ui_list need a label widget list for form layout creation
        
        # 1. convert string to object and flatten part_list
        for each_part in part_list:
            # 1.1 string
            if isinstance(each_part, str):
                # - string : get part info
                partInfo = each_part.split(';')
                uiNameLabel = partInfo[0].split('@')
                uiName = uiNameLabel[0]
                uiLabel = ''
                if len(uiNameLabel) > 1:
                    uiLabel = uiNameLabel[1]
                    form_type = 1
                uiType = partInfo[1] if len(partInfo) > 1 else ""
                uiArgs = partInfo[2] if len(partInfo) > 2 else ""
                # - string : valid info
                if uiType == "":
                    print uiType
                    print("Warning (QuickUI): uiType is empty for "+each_part)
                else:
                    # - string : to object creation
                    ui_create_state = 0 # flag to track creation success
                    if not uiType[0] == 'Q':
                        # -- 3rd ui type, create like UI_Class.UI_Class()
                        self.uiList[uiName] = getattr(eval(uiType), uiType)()
                        ui_list.append(self.uiList[uiName])
                        ui_create_state = 1
                    else:
                        # -- Qt ui
                        if uiType in ('QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout'):
                            # --- Qt Layout creation preset func
                            ui_list.append(self.quickLayout(uiType, uiName))
                            ui_create_state = 1
                        elif uiType in ('QSplitter', 'QTabWidget', 'QGroupBox'):
                            # --- Qt container creation
                            if uiType == 'QSplitter':
                                # ---- QSplitter as element
                                split_type = QtCore.Qt.Horizontal
                                if uiArgs == 'v':
                                    split_type = QtCore.Qt.Vertical
                                self.uiList[uiName]=QtGui.QSplitter(split_type)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            elif uiType == 'QTabWidget':
                                # ---- QTabWidget as element, no tab label need for input
                                self.uiList[uiName]=QtGui.QTabWidget()
                                self.uiList[uiName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            elif uiType == 'QGroupBox':
                                # ---- QGroupBox as element, with layout type and optional title
                                arg_list = [x.strip() for x in uiArgs.split(',')]
                                grp_layout = arg_list[0] if arg_list[0]!='' else 'vbox'
                                grp_title = arg_list[1] if len(arg_list)>1 else uiName
                                # create layout and set grp layout
                                grp_layout = self.quickLayout(grp_layout, uiName+"_layout" )
                                self.uiList[uiName] = QtGui.QGroupBox(grp_title)
                                self.uiList[uiName].setLayout(grp_layout)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                        else:
                            # --- Qt widget creation
                            if uiArgs == "":
                                # ---- widget with no uiArgs
                                self.uiList[uiName] = getattr(QtGui, uiType)()
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            else:
                                # ---- widget with uiArgs
                                if not ( uiArgs.startswith("(") and uiArgs.endswith(")") ):
                                    # ----- with string arg
                                    self.uiList[uiName] = getattr(QtGui, uiType)(uiArgs)
                                    ui_list.append(self.uiList[uiName])
                                    ui_create_state = 1
                                else:
                                    # ----- with array arg
                                    arg_list = uiArgs.replace('(','').replace(')','').split(',')
                                    if uiType == 'QComboBox':
                                        self.uiList[uiName] = QtGui.QComboBox()
                                        self.uiList[uiName].addItems(arg_list)
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    elif uiType == 'QSpacerItem':
                                        policyList = ( QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Ignored)
                                        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
                                        # factors in fighting for space: horizontalStretch
                                        # extra space: setContentsMargins and setSpacing
                                        # ref: http://www.cnblogs.com/alleyonline/p/4903337.html
                                        arg_list = [ int(x) for x in arg_list ]
                                        self.uiList[uiName] = QtGui.QSpacerItem(arg_list[0],arg_list[1], policyList[arg_list[2]], policyList[arg_list[3]] )
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    else:
                                        print("Warning (QuickUI): uiType don't support array arg for "+each_part)
                    # - string : Qt widget label for form element creation
                    if ui_create_state == 1:
                        if uiLabel != '':
                            ui_label_list.append((uiName,uiLabel))
                        else:
                            ui_label_list.append('')
                    ui_create_state = 0
            else:
                # 1.2 other part like: object, object list, [object, label object]
                if isinstance(each_part, (QtGui.QWidget, QtGui.QLayout, QtGui.QSpacerItem)):
                    # - object
                    ui_list.append(each_part)
                    ui_label_list.append('')
                elif isinstance(each_part, (tuple, list)):
                    # - object list, [object, label object]
                    if len(each_part) != 0:
                        if isinstance(each_part[0], (tuple, list)) and len(each_part)==2:
                            # -- [object, label object]
                            ui_list.extend(each_part[0])
                            ui_label_list.extend(each_part[1])
                        else:
                            # -- object list
                            ui_list.extend(each_part)
                            ui_label_list.extend(['']*len(each_part))
                
        # 2 parentObject part
        if parentObject == '':
            # - if no parentObject, return object list or [object list, label_object list] 
            if form_type == 1:
                return [ui_list, ui_label_list]
            else:
                return ui_list
        else:
            if isinstance(parentObject, str):
                # - if parentObject, convert string to parentObject
                parentName = ''
                parentType = ''
                parentArgs = ''
                layout_type_list = (
                    'QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout', 'vbox', 'hbox', 'grid', 'form',
                    'QSplitter', 'QTabWidget', 'QGroupBox', 'split', 'tab', 'grp',
                )
                # get options
                parentOpt = parentObject.split(';')
                if len(parentOpt) == 1:
                    # -- only 1 arg case: strict name format, eg. conf_QHBoxLayout, config_hbox
                        parentName = parentOpt[0] # 1 para case: strict name endfix format
                        parentType = parentName.rsplit('_',1)[-1]
                elif len(parentOpt)==2:
                    # -- only 2 arg case: 
                    # a. flexible name format + type eg. conf_layout;QGridLayout, conf_layout;hbox
                    # b. strict name format, + setting eg. conf_QGridLayout;h, config_grid;h
                    parentName = parentOpt[0]
                    if parentOpt[1] in layout_type_list:
                        parentType = parentOpt[1] # a
                    else:
                        parentType = parentName.rsplit('_',1)[-1]
                        parentArgs = parentOpt[1] # b
                elif len(parentOpt)>=3: 
                    # -- 3 arg case: 
                    # flexible name format + type + settings eg. conf_layout;QGridLayout;h
                    parentName = parentOpt[0]
                    parentType = parentOpt[1]
                    parentArgs = parentOpt[2]
                # - validate layout options
                if parentName=='' or (parentType not in layout_type_list):
                    print("Warning (QuickUI): quickUI not support parent layout as "+parentObject)
                    return
                else:
                    # - create layout
                    if parentType in ('QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout', 'vbox', 'hbox', 'grid', 'form'):
                        # -- layout object case
                        parentObject = self.quickLayout(parentType, parentName)
                    elif parentType in ('QSplitter', 'QTabWidget', 'QGroupBox', 'split', 'tab', 'grp'):
                        # --- Qt container creation
                        if parentType in ('QSplitter', 'split'):
                            # ---- QSplitter as element
                            split_type = QtCore.Qt.Horizontal
                            if parentArgs == 'v':
                                split_type = QtCore.Qt.Vertical
                            self.uiList[parentName]=QtGui.QSplitter(split_type)
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QTabWidget', 'tab'):
                            # ---- QTabWidget as element, no tab label need for input
                            self.uiList[parentName]=QtGui.QTabWidget()
                            self.uiList[parentName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QGroupBox', 'grp'):
                            # ---- QGroupBox as element, with layout type and optional title
                            arg_list = [x.strip() for x in parentArgs.split(',')]
                            grp_layout = arg_list[0] if arg_list[0]!='' else 'vbox'
                            grp_title = arg_list[1] if len(arg_list)>1 else parentName
                            # create layout and set grp layout
                            grp_layout = self.quickLayout(grp_layout, parentName+"_layout" )
                            self.uiList[parentName] = QtGui.QGroupBox(grp_title)
                            self.uiList[parentName].setLayout(grp_layout)
                            parentObject = self.uiList[parentName]
            
            # 3. get parentLayout inside parentObject
            parentLayout = ''
            if isinstance(parentObject, QtGui.QLayout):
                parentLayout = parentObject
            elif isinstance(parentObject, QtGui.QGroupBox):
                parentLayout = parentObject.layout()
            # 3.1 insert part_list into parentLayout for layout and groupbox
            if isinstance(parentLayout, QtGui.QBoxLayout):
                for each_ui in ui_list:
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
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    x = insertRow if insert_opt=="h" else i
                    y = i if insert_opt=="h" else insertCol
                    if isinstance(each_ui, QtGui.QWidget):
                        parentLayout.addWidget(each_ui,x,y)
                    elif isinstance(each_ui, QtGui.QSpacerItem):
                        parentLayout.addItem(each_ui,x,y)
                    elif isinstance(each_ui, QtGui.QLayout):
                        parentLayout.addLayout(each_ui,x,y)
            elif isinstance(parentLayout, QtGui.QFormLayout):
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    if isinstance(each_ui, QtGui.QWidget) or isinstance(each_ui, QtGui.QLayout):
                        # create and add label: (uiName, uiLabel)
                        if ui_label_list[i] != '':
                            uiLabelName = ui_label_list[i][0] + "_label"
                            uiLabelText = ui_label_list[i][1]
                            self.uiList[uiLabelName] = QtGui.QLabel(uiLabelText)
                            parentLayout.addRow(self.uiList[uiLabelName], each_ui)
                        else:
                            parentLayout.addRow(each_ui)
            else:
                # 3.2 insert for empty parentLayout for split, and tab
                if isinstance(parentObject, QtGui.QSplitter):
                    for each_ui in ui_list:
                        if isinstance(each_ui, QtGui.QWidget):
                            parentObject.addWidget(each_ui)
                        else:
                            tmp_holder = QtGui.QWidget()
                            tmp_holder.setLayout(each_ui)
                            parentObject.addWidget(tmp_holder)
                elif isinstance(parentObject, QtGui.QTabWidget):
                    tab_names = insert_opt.replace('(','').replace(')','').split(',')
                    for i in range( len(ui_list) ):
                        each_tab = ui_list[i]
                        each_name = 'tab_'+str(i) 
                        if i < len(tab_names):
                            if tab_names[i] != '':
                                each_name = tab_names[i]
                        if isinstance(each_tab, QtGui.QWidget):
                            parentObject.addTab(each_tab, each_name)
                        else:
                            tmp_holder = QtGui.QWidget()
                            tmp_holder.setLayout(each_tab)
                            parentObject.addTab(tmp_holder, each_name)
            return parentObject
            
    def quickLayout(self, type, ui_name=""):
        the_layout = ''
        if type in ("form", "QFormLayout"):
            the_layout = QtGui.QFormLayout()
            the_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
            the_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)    
        elif type in ("grid", "QGridLayout"):
            the_layout = QtGui.QGridLayout()
        elif type in ("hbox", "QHBoxLayout"):
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
        
    def quickGrpUI(self, ui_name, ui_label, ui_layout):
        self.uiList[ui_name] = QtGui.QGroupBox(ui_label)
        if isinstance(ui_layout, QtGui.QLayout):
            self.uiList[ui_name].setLayout(ui_layout)
        elif isinstance(ui_layout, str):
            ui_layout = self.quickLayout(ui_name+"_layout", ui_layout)
            self.uiList[ui_name].setLayout(ui_layout)
        return [self.uiList[ui_name], ui_layout]
    
    def quickPolicy(self, ui_list, w, h):
        if not isinstance(ui_list, (list, tuple)):
            ui_list = [ui_list]
        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
        policyList = ( QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Ignored)
        for each_ui in ui_list:
            if isinstance(each_ui, str):
                each_ui = self.uiList[each_ui]
            each_ui.setSizePolicy(policyList[w],policyList[h])
            
    def quickMsg(self, msg):
        tmpMsg = QtGui.QMessageBox() # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg)
        tmpMsg.addButton("OK",QtGui.QMessageBox.YesRole)
        tmpMsg.exec_()
    def quickMsgAsk(self, msg):
        txt, ok = QtGui.QInputDialog.getText(self, "Input", msg)
        return (str(txt), ok)
        
    def mui_to_qt(self, mui_name):
        ptr = mui.MQtUtil.findControl(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findLayout(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findMenuItem(mui_name)
        if ptr is not None:
            if qtMode == 0:
                # ==== for pyside ====
                return shiboken.wrapInstance(long(ptr), QtGui.QWidget)
            elif qtMode == 1:
                # ==== for PyQt====
                return sip.wrapinstance(long(ptr), QtCore.QObject)
    def qt_to_mui(self, qt_obj):
        ref = None
        if qtMode == 0:
            # ==== for pyside ====
            ref = long(shiboken.getCppPointer(qt_obj)[0])
        elif qtMode == 1:
            # ==== for PyQt====
            ref = long(sip.unwrapinstance(qt_obj))
        if ref is not None:
            return mui.MQtUtil.fullName(ref)
            
#############################################
# window instance creation
#############################################
# If you want to be able to Keep only one copy of windows ui in Maya, use code below
single_TMP_UniversalToolUI_TND = None   
def main(mode=0):
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
    global single_TMP_UniversalToolUI_TND
    if single_TMP_UniversalToolUI_TND is None:
        single_TMP_UniversalToolUI_TND = TMP_UniversalToolUI_TND(parentWin, mode) # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_TMP_UniversalToolUI_TND.show()
    
    if deskMode == 1:
        sys.exit(app.exec_())
    
    # example: show ui stored
    # print(single_TMP_UniversalToolUI_TND.uiList.keys())
    return single_TMP_UniversalToolUI_TND
    
# If you want to be able to load multiple windows of the same ui in Maya, use code below
'''
def main(mode=0):
    parentWin = None
    if deskMode == 0:
        if qtMode == 0:
            # ==== for pyside ====
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)
        elif qtMode == 1:
            # ==== for PyQt====
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
            
    ui = TMP_UniversalToolUI_TND(parentWin) # extra note: in Maya () for no parent; (parentWin,mode) for extra mode input
    ui.show()
    # example: show ui stored
    # print(ui.uiList.keys())
    return ui
'''
if __name__ == "__main__":
    main()