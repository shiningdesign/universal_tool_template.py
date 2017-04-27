tpl_ver = 10.0
print("tpl_ver: {}".format(tpl_ver))
# Univeral Tool Template v010.0
# by ying - https://github.com/shiningdesign/universal_tool_template.py

# ---- hostMode detect ----
# ref: https://github.com/fredrikaverpil/pyvfx-boilerplate/blob/master/boilerplate.py
hostMode = ""
try:
    import maya.OpenMayaUI as mui
    import maya.cmds as cmds
    hostMode = "maya" # maya detection
except ImportError:
    try:
        import hou 
        hostMode = "houdini" # houdini detection
    except ImportError:
        try:
            import nuke
            import nukescripts
            hostMode = "nuke" # nuke detection
        except ImportError:
            try:
                import bpy 
                hostMode = "blender" # blender detection
            except ImportError:
                hostMode = "desktop"
print("Host: {}".format(hostMode))
    
# ---- QtMode detection ----
# ref: https://github.com/mottosso/Qt.py
qtMode = 0 # 0: PySide; 1 : PyQt, 2: PySide2, 3: PyQt5
qtModeList = ("PySide", "PyQt4", "PySide2", "PyQt5")
try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    print("PySide Try")
    qtMode = 0
    if hostMode == "maya":
        import shiboken
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        print("PySide2 Try")
        qtMode = 2
        if hostMode == "maya":
            import shiboken2 as shiboken
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

# ---- PyMode detection ----
# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

import sys
pyMode = '.'.join([ str(n) for n in sys.version_info[:3] ])
print("Python: {}".format(pyMode))
# ---- osMode detect ----
osMode = 'other'
if sys.platform in ['win32','win64']:
    osMode = 'win'
elif sys.platform == 'darwin':
    osMode = 'mac'
elif sys.platform == 'linux2':
    osMode = 'linux'
print("OS: {}".format(osMode))
# ---- template module list ----
import os # for path and language code
import glob # for file list
from functools import partial # for partial function creation
import json # for ascii data output
if sys.version_info[:3][0]<3:
    import cPickle # for binary data output
else:
    import _pickle as cPickle
import re # for name pattern
import ctypes # for windows instance detection
#------------------------------
# user UI class choice
#------------------------------
super_class = QtWidgets.QMainWindow # note: only one supports menu
#super_class = QtWidgets.QDialog
#super_class = QtWidgets.QWidget

class UniversalToolUI(super_class): 
    def __init__(self, parent=None, mode=0):
        super_class.__init__(self, parent)
        #------------------------------
        # class variables
        #------------------------------
        self.version = "0.1"
        self.log = 'no version log in user class'
        self.help = 'no help guide in user class'
        
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        
        self.location = ""
        if getattr(sys, 'frozen', False):
            # frozen - cx_freeze
            self.location = sys.executable
        else:
            # unfrozen
            self.location = os.path.realpath(sys.modules[self.__class__.__module__].__file__)
            
        self.name = self.__class__.__name__
        self.iconPath = os.path.join(os.path.dirname(self.location),'icons',self.name+'.png')
        self.iconPix = QtGui.QPixmap(self.iconPath)
        self.icon = QtGui.QIcon(self.iconPath)
        self.fileType='.{0}_EXT'.format(self.name)
        
        #------------------------------
        # core function variable
        #------------------------------
        self.qui_core_dict = {
            'vbox': 'QVBoxLayout','hbox':'QHBoxLayout','grid':'QGridLayout', 'form':'QFormLayout',
            'split': 'QSplitter', 'grp':'QGroupBox', 'tab':'QTabWidget',
            'btn':'QPushButton', 'btnMsg':'QPushButton', 'label':'QLabel', 'input':'QLineEdit', 'check':'QCheckBox', 'choice':'QComboBox',
            'txt': 'QTextEdit',
            'list': 'QListWidget', 'tree': 'QTreeWidget', 'table': 'QTableWidget',
            'space': 'QSpacerItem',
            'menu' : 'QMenu', 'menubar' : 'QMenuBar',
        }
        self.qui_user_dict = {}
        #------------------------------
        
    def setupStyle(self):
        # global app style setting for desktop
        if hostMode == "desktop":
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
    
    def setupMenu(self):
        # global help menu
        if 'help_menu' in self.uiList.keys():
            # for info review
            cur_menu = self.uiList['help_menu']
            self.quickMenuAction('helpHostMode_atnNone','Host Mode - {}'.format(hostMode),'Host Running.','', cur_menu)
            self.quickMenuAction('helpPyMode_atnNone','Python Mode - {}'.format(pyMode),'Python Library Running.','', cur_menu)
            self.quickMenuAction('helpQtMode_atnNone','Qt Mode - {}'.format(qtModeList[qtMode]),'Qt Library Running.','', cur_menu)
            self.quickMenuAction('helpTemplate_atnNone','Universal Tool Teamplate - {}'.format(tpl_ver),'based on Univeral Tool Template v{0} by Shining Ying - https://github.com/shiningdesign/universal{1}tool{1}template.py'.format(tpl_ver,'_'),'', cur_menu)
            cur_menu.addSeparator()
            self.uiList['helpGuide_msg'] = self.help
            self.quickMenuAction('helpGuide_atnMsg','Usage Guide','How to Usge Guide.','helpGuide.png', cur_menu)
            self.uiList['helpLog_msg'] = self.log
            self.quickMenuAction('helpLog_atnMsg','About','Vesion Log.','helpLog.png', cur_menu)
    def setupWin(self):
        self.setWindowTitle(self.name + " - v" + self.version + " - host: " + hostMode)
        self.setWindowIcon(self.icon)
        # initial win drag position
        self.drag_position=QtGui.QCursor.pos()
        
    ########################################
    # UI CORE function
    ########################################
    def qui(self, ui_list_string, parent_ui_string='', insert_opt=''):
        ui_creation_list = [ x.strip() for x in ui_list_string.split('|') ]
        ui_creation_quickUI_list = []
        # ------------
        # - ui list
        # ------------
        for ui_creation in ui_creation_list:
            arg_list = ui_creation.split(';')
            uiName = arg_list[0].split('@')[0]
            # ------------
            # continue if ui is already created. pass as ui reference
            if uiName in self.uiList.keys():
                ui_creation_quickUI_list.append(self.uiList[uiName])
                continue
            # ------------
            # create quickUI string
            # - expand short name for Class
            uiClass = uiName.rsplit('_',1)[-1]
            if uiClass == 'layout' and len(arg_list)>1:
                uiClass = arg_list[1]
                arg_list = [ arg_list[0] ]
                
            if uiClass in self.qui_user_dict:
                uiClass = self.qui_user_dict[uiClass] # first, try user dict
            elif uiClass in self.qui_core_dict:
                uiClass = self.qui_core_dict[uiClass] # then, try default core dict
            
            # - check it is valid Qt class or a user class
            if hasattr(QtWidgets, uiClass) or uiClass in sys.modules:
                pass # uiClass is valid for Qt class, user module
            else:
                print("WARNING: ({0}) is not defined in self.qui_user_dict and it is not a Qt widget class or User class; Item {1} Ignored.".format(uiClass, uiName))
                continue
            # - set quickUI creation format
            arg_list[0] = arg_list[0] +';'+uiClass
            if len(arg_list)==1:
                if uiClass in ('QPushButton','QLabel'):
                    arg_list.append(uiName) # give empty button and label a place holder name
            ui_creation_quickUI_list.append(';'.join(arg_list))
        # ------------
        # - ui parent
        # ------------
        parent_creation_quickUI_input = ''
        parent_arg_list = parent_ui_string.split(';')
        parent_uiName = parent_arg_list[0]
        # - continue if parent ui is already created. pass as ui reference
        if parent_uiName in self.uiList.keys():
            parent_creation_quickUI_input = self.uiList[parent_uiName]
        else:
            parent_uiClass = parent_uiName.rsplit('_',1)[-1]
            if parent_uiClass == 'layout' and len(parent_arg_list)>1:
                parent_uiClass = parent_arg_list[1]
                parent_arg_list = [ parent_arg_list[0] ]
        
            if parent_uiClass in self.qui_user_dict:
                parent_uiClass = self.qui_user_dict[parent_uiClass] # first, try user dict
            elif parent_uiClass in self.qui_core_dict:
                parent_uiClass = self.qui_core_dict[parent_uiClass] # then, try default core dict
            
            # - check it is valid Qt class or a user class
            if hasattr(QtWidgets, parent_uiClass) or parent_uiClass in sys.modules:
                pass # uiClass is valid for Qt class, user module
            else:
                print("WARNING: ({0}) is not defined in self.qui_user_dict and it is not a Qt widget class or User class; Item {1} Ignored.".format(parent_uiClass, parent_uiName))
                return
            
            # - set quickUI creation format
            parent_arg_list[0] = parent_arg_list[0] +';'+parent_uiClass
            
            parent_creation_quickUI_input = ';'.join(parent_arg_list)

        self.quickUI(ui_creation_quickUI_list, parent_creation_quickUI_input, insert_opt)
        
    def setupUI(self, layout='grid'):
        #------------------------------
        # main_layout auto creation for holding all the UI elements
        #------------------------------
        main_layout = None
        if isinstance(self, QtWidgets.QMainWindow):
            main_widget = QtWidgets.QWidget()
            self.setCentralWidget(main_widget)        
            main_layout = self.quickLayout(layout, 'main_layout') # grid for auto fill window size
            main_widget.setLayout(main_layout)
        else:
            # main_layout for QDialog
            main_layout = self.quickLayout(layout, 'main_layout')
            self.setLayout(main_layout)
            
    def Establish_Connections(self):
        for ui_name in self.uiList.keys():
            prefix = ui_name.rsplit('_', 1)[0]
            if ui_name.endswith('_btn'):
                self.uiList[ui_name].clicked.connect(getattr(self, prefix+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_atn'):
                self.uiList[ui_name].triggered.connect(getattr(self, prefix+"_action", partial(self.default_action,ui_name)))
            elif ui_name.endswith('_btnMsg'):
                self.uiList[ui_name].clicked.connect(getattr(self, prefix+"_message", partial(self.default_message,ui_name)))
            elif ui_name.endswith('_atnMsg'):
                self.uiList[ui_name].triggered.connect(getattr(self, prefix+"_message", partial(self.default_message,ui_name)))
    
    #############################################
    # UI Response functions (custom + prebuilt functions)
    #############################################

    #---- template response functions ----
    def default_action(self, ui_name):
        print("No action defined for this button: "+ui_name)
    def default_message(self, ui_name):
        prefix = ui_name.rsplit('_', 1)[0]
        msgName = prefix+"_msg"
        msg_txt = msgName + " is not defined in uiList."
        if msgName in self.uiList:
            msg_txt = self.uiList[msgName]
        self.quickMsg(msg_txt)
    
    ########################################
    ########################################
    # ----  CORE TEMPLATE FUNCTIONS ----   #
    #     note: dont touch code below      #
    ########################################

    # ----  input get with validation functions ----
    def input_text(self, input_name, msg=None):
        name = unicode(self.uiList[input_name].text())
        if name == '':
            print("Please define the name. {0}".format(msg))
            return
        return name
    def input_int(self, input_name, min=None, max=None, msg=None):
        input_txt = str(self.uiList[input_name].text())
        result = None
        # int valid
        if not input_txt.isdigit():
            print("Please enter a valid int. {0}".format(msg))
            return
        result = int(input_txt)
        # min
        if min != None:
            if result < min:
                print("Please enter a valid int number >= {0}. {1}".format(min, msg))
                return
        # max
        if max != None:
            if result > max:
                print("Please enter a valid int number <= {0}. {1}".format(max, msg))
                return
        return result
    def input_float(self, input_name, min=None, max=None, msg=None):
        input_txt = str(self.uiList[input_name].text())
        result = None
        try:
            result = float(input_txt)
        except (ValueError, TypeError):
            return
        # min
        if min != None:
            if result < min:
                print("Please enter a valid int number >= {0}. {1}".format(min, msg))
                return
        # max
        if max != None:
            if result > max:
                print("Please enter a valid int number <= {0}. {1}".format(max, msg))
                return
        return result
    def input_choice(self, ui_name):
        if ui_name in self.uiList.keys():
            return self.uiList[ui_name].currentIndex()
        else:
            return
    def output_text(self, ui_name, text):
        if ui_name in self.uiList.keys():
            self.uiList[ui_name].setText(text)

    # ---- data and text data functions ----
    def readDataFile(self,file,binary=0):
        with open(file) as f:
            if binary == 0:
                data = json.load(f)
            else:
                data = cPickle.load(f)
        return data
    def writeDataFile(self,data,file,binary=0):
        with open(file, 'w') as f:
            if binary == 0:
                json.dump(data, f)
            else:
                cPickle.dump(data, f)
    def readTextFile(self, file):
        with open(file) as f:
            txt = f.read()
        return txt
    def writeTextFile(self, txt, file):    
        with open(file, 'w') as f:
            f.write(txt)
        
    # ---- UI language functions ----
    def loadLang(self):
        # store default language
        self.memoData['lang']={}
        self.memoData['lang']['default']={}
        for ui_name in self.uiList.keys():
            ui_element = self.uiList[ui_name]
            if isinstance(ui_element, (QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QAction, QtWidgets.QCheckBox) ):
                # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                self.memoData['lang']['default'][ui_name] = unicode(ui_element.text())
            elif isinstance(ui_element, (QtWidgets.QGroupBox, QtWidgets.QMenu) ):
                # uiType: QMenu, QGroupBox
                self.memoData['lang']['default'][ui_name] = unicode(ui_element.title())
            elif isinstance(ui_element, QtWidgets.QTabWidget):
                # uiType: QTabWidget
                tabCnt = ui_element.count()
                tabNameList = []
                for i in range(tabCnt):
                    tabNameList.append(unicode(ui_element.tabText(i)))
                self.memoData['lang']['default'][ui_name]=';'.join(tabNameList)
            elif isinstance(ui_element, QtWidgets.QComboBox):
                # uiType: QComboBox
                itemCnt = ui_element.count()
                itemNameList = []
                for i in range(itemCnt):
                    itemNameList.append(unicode(ui_element.itemText(i)))
                self.memoData['lang']['default'][ui_name]=';'.join(itemNameList)
            elif isinstance(ui_element, QtWidgets.QTreeWidget):
                # uiType: QTreeWidget
                labelCnt = ui_element.headerItem().columnCount()
                labelList = []
                for i in range(labelCnt):
                    labelList.append(unicode(ui_element.headerItem().text(i)))
                self.memoData['lang']['default'][ui_name]=';'.join(labelList)
            elif isinstance(ui_element, QtWidgets.QTableWidget):
                # uiType: QTableWidget
                colCnt = ui_element.columnCount()
                headerList = []
                for i in range(colCnt):
                    if ui_element.horizontalHeaderItem(i):
                        headerList.append( unicode(ui_element.horizontalHeaderItem(i).text()) )
                    else:
                        headerList.append('')
                self.memoData['lang']['default'][ui_name]=';'.join(headerList)
            elif isinstance(ui_element, (str, unicode) ):
                # uiType: string for msg
                self.memoData['lang']['default'][ui_name] = self.uiList[ui_name]
        
        # language menu
        if isinstance(self, QtWidgets.QMainWindow):
            self.quickMenu(['language_menu;&Language'])
            cur_menu = self.uiList['language_menu']
            self.quickMenuAction('langDefault_atnLang', 'Default','','langDefault.png', cur_menu)
            self.uiList['langDefault_atnLang'].triggered.connect(partial(self.setLang,'default'))
            cur_menu.addSeparator()
            
        # scan for language file
        lang_path = os.path.dirname(self.location)
        baseName = os.path.splitext( os.path.basename(self.location) )[0]
        for filePath in [ x for x in glob.glob(os.path.join(lang_path,baseName+'_lang_*.json')) if os.path.isfile(x) ]:
            langName = re.findall(baseName+'_lang_(.+)\.json', os.path.basename(filePath))
            if len(langName) == 1:
                langName = langName[0]
                self.memoData['lang'][ langName ] = self.readDataFile( filePath )
                if 'language_menu' in self.uiList:
                    self.quickMenuAction(langName+'_atnLang', langName.upper(),'',langName + '.png', self.uiList['language_menu'])
                    self.uiList[langName+'_atnLang'].triggered.connect(partial(self.setLang,langName))
        # if no language file detected, add export default language option
        if isinstance(self, QtWidgets.QMainWindow) and len(self.memoData['lang']) == 1:
            self.quickMenuAction('langExport_atnLang', 'Export Default Language','','langExport.png', self.uiList['language_menu'])
            self.uiList['langExport_atnLang'].triggered.connect(self.exportLang)
    
    def setLang(self, langName):
        lang_data = self.memoData['lang'][langName]
        for ui_name in lang_data.keys():
            if ui_name in self.uiList.keys() and lang_data[ui_name] != '':
                ui_element = self.uiList[ui_name]
                # '' means no translation availdanle in that data file
                if isinstance(ui_element, (QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QAction, QtWidgets.QCheckBox) ):
                    # uiType: QLabel, QPushButton, QAction(menuItem), QCheckBox
                    ui_element.setText(lang_data[ui_name])
                elif isinstance(ui_element, (QtWidgets.QGroupBox, QtWidgets.QMenu) ):
                    # uiType: QMenu, QGroupBox
                    ui_element.setTitle(lang_data[ui_name])
                elif isinstance(ui_element, QtWidgets.QTabWidget):
                    # uiType: QTabWidget
                    tabCnt = ui_element.count()
                    tabNameList = lang_data[ui_name].split(';')
                    if len(tabNameList) == tabCnt:
                        for i in range(tabCnt):
                            if tabNameList[i] != '':
                                ui_element.setTabText(i,tabNameList[i])
                elif isinstance(ui_element, QtWidgets.QComboBox):
                    # uiType: QComboBox
                    itemCnt = ui_element.count()
                    itemNameList = lang_data[ui_name].split(';')
                    ui_element.clear()
                    ui_element.addItems(itemNameList)
                elif isinstance(ui_element, QtWidgets.QTreeWidget):
                    # uiType: QTreeWidget
                    labelCnt = ui_element.headerItem().columnCount()
                    labelList = lang_data[ui_name].split(';')
                    ui_element.setHeaderLabels(labelList)
                elif isinstance(ui_element, QtWidgets.QTableWidget):
                    # uiType: QTableWidget
                    colCnt = ui_element.columnCount()
                    headerList = lang_data[ui_name].split(';')
                    cur_table.setHorizontalHeaderLabels( headerList )
                elif isinstance(ui_element, (str, unicode) ):
                    # uiType: string for msg
                    self.uiList[ui_name] = lang_data[ui_name]
    def exportLang(self):
        file = self.quickFileAsk('export', ext='json')
        if file != '':
            self.writeDataFile( self.memoData['lang']['default'], file )
            self.quickMsg("Languge File created: '"+file)
    
    # ---- Quick UI creation functions ----
    def quickMenu(self, ui_names):
        if not isinstance(ui_names, (list, tuple)):
            # support qui format menu creation
            ui_names = [ x.strip() for x in ui_names.split('|') ]
        if isinstance(self, QtWidgets.QMainWindow):
            menubar = self.menuBar()
            for each_ui in ui_names:
                createOpt = each_ui.split(';')
                if len(createOpt) > 1:
                    uiName = createOpt[0]
                    uiLabel = createOpt[1]
                    self.uiList[uiName] = QtWidgets.QMenu(uiLabel)
                    menubar.addMenu(self.uiList[uiName])
        else:
            print("Warning (QuickMenu): Only QMainWindow can have menu bar.")
        
    def quickMenuAction(self, objName, title, tip, icon, menuObj):
        self.uiList[objName] = QtWidgets.QAction(QtGui.QIcon(icon), title, self)
        self.uiList[objName].setStatusTip(tip)
        menuObj.addAction(self.uiList[objName])
    
    def quickLayout(self, type, ui_name=""):
        the_layout = ''
        if type in ("form", "QFormLayout"):
            the_layout = QtWidgets.QFormLayout()
            the_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
            the_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)    
        elif type in ("grid", "QGridLayout"):
            the_layout = QtWidgets.QGridLayout()
        elif type in ("hbox", "QHBoxLayout"):
            the_layout = QtWidgets.QHBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        else:        
            the_layout = QtWidgets.QVBoxLayout()
            the_layout.setAlignment(QtCore.Qt.AlignTop)
        if ui_name != "":
            self.uiList[ui_name] = the_layout
        return the_layout
    
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
                                self.uiList[uiName]=QtWidgets.QSplitter(split_type)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            elif uiType == 'QTabWidget':
                                # ---- QTabWidget as element, no tab label need for input
                                self.uiList[uiName]=QtWidgets.QTabWidget()
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
                                self.uiList[uiName] = QtWidgets.QGroupBox(grp_title)
                                self.uiList[uiName].setLayout(grp_layout)
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                        else:
                            # --- Qt widget creation
                            if uiArgs == "":
                                # ---- widget with no uiArgs
                                self.uiList[uiName] = getattr(QtWidgets, uiType)()
                                ui_list.append(self.uiList[uiName])
                                ui_create_state = 1
                            else:
                                # ---- widget with uiArgs
                                if not ( uiArgs.startswith("(") and uiArgs.endswith(")") ):
                                    # ----- with string arg
                                    self.uiList[uiName] = getattr(QtWidgets, uiType)(uiArgs)
                                    ui_list.append(self.uiList[uiName])
                                    ui_create_state = 1
                                else:
                                    # ----- with array arg
                                    arg_list = uiArgs.replace('(','').replace(')','').split(',')
                                    if uiType == 'QComboBox':
                                        self.uiList[uiName] = QtWidgets.QComboBox()
                                        self.uiList[uiName].addItems(arg_list)
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    elif uiType == 'QTreeWidget':
                                        self.uiList[uiName] = QtWidgets.QTreeWidget()
                                        self.uiList[uiName].setHeaderLabels(arg_list)
                                        ui_list.append(self.uiList[uiName])
                                        ui_create_state = 1
                                    elif uiType == 'QSpacerItem':
                                        policyList = ( QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored)
                                        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
                                        # factors in fighting for space: horizontalStretch
                                        # extra space: setContentsMargins and setSpacing
                                        # ref: http://www.cnblogs.com/alleyonline/p/4903337.html
                                        arg_list = [ int(x) for x in arg_list ]
                                        self.uiList[uiName] = QtWidgets.QSpacerItem(arg_list[0],arg_list[1], policyList[arg_list[2]], policyList[arg_list[3]] )
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
                if isinstance(each_part, (QtWidgets.QWidget, QtWidgets.QLayout, QtWidgets.QSpacerItem)):
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
                            self.uiList[parentName]=QtWidgets.QSplitter(split_type)
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QTabWidget', 'tab'):
                            # ---- QTabWidget as element, no tab label need for input
                            self.uiList[parentName]=QtWidgets.QTabWidget()
                            self.uiList[parentName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                            parentObject = self.uiList[parentName]
                        elif parentType in ('QGroupBox', 'grp'):
                            # ---- QGroupBox as element, with layout type and optional title
                            arg_list = [x.strip() for x in parentArgs.split(',')]
                            grp_layout = arg_list[0] if arg_list[0]!='' else 'vbox'
                            grp_title = arg_list[1] if len(arg_list)>1 else parentName
                            # create layout and set grp layout
                            grp_layout = self.quickLayout(grp_layout, parentName+"_layout" )
                            self.uiList[parentName] = QtWidgets.QGroupBox(grp_title)
                            self.uiList[parentName].setLayout(grp_layout)
                            parentObject = self.uiList[parentName]
            
            # 3. get parentLayout inside parentObject
            parentLayout = ''
            if isinstance(parentObject, QtWidgets.QLayout):
                parentLayout = parentObject
            elif isinstance(parentObject, QtWidgets.QGroupBox):
                parentLayout = parentObject.layout()
            # 3.1 insert part_list into parentLayout for layout and groupbox
            if isinstance(parentLayout, QtWidgets.QBoxLayout):
                for each_ui in ui_list:
                    if isinstance(each_ui, QtWidgets.QWidget):
                        parentLayout.addWidget(each_ui)
                    elif isinstance(each_ui, QtWidgets.QSpacerItem):
                        parentLayout.addItem(each_ui)
                    elif isinstance(each_ui, QtWidgets.QLayout):
                        parentLayout.addLayout(each_ui)
            elif isinstance(parentLayout, QtWidgets.QGridLayout):
                # one row/colume operation only
                insertRow = parentLayout.rowCount()
                insertCol = parentLayout.columnCount()
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    x = insertRow if insert_opt=="h" else i
                    y = i if insert_opt=="h" else insertCol
                    if isinstance(each_ui, QtWidgets.QWidget):
                        parentLayout.addWidget(each_ui,x,y)
                    elif isinstance(each_ui, QtWidgets.QSpacerItem):
                        parentLayout.addItem(each_ui,x,y)
                    elif isinstance(each_ui, QtWidgets.QLayout):
                        parentLayout.addLayout(each_ui,x,y)
            elif isinstance(parentLayout, QtWidgets.QFormLayout):
                for i in range(len(ui_list)):
                    each_ui = ui_list[i]
                    if isinstance(each_ui, QtWidgets.QWidget) or isinstance(each_ui, QtWidgets.QLayout):
                        # create and add label: (uiName, uiLabel)
                        if ui_label_list[i] != '':
                            uiLabelName = ui_label_list[i][0] + "_label"
                            uiLabelText = ui_label_list[i][1]
                            self.uiList[uiLabelName] = QtWidgets.QLabel(uiLabelText)
                            parentLayout.addRow(self.uiList[uiLabelName], each_ui)
                        else:
                            parentLayout.addRow(each_ui)
            else:
                # 3.2 insert for empty parentLayout for split, and tab
                if isinstance(parentObject, QtWidgets.QSplitter):
                    for each_ui in ui_list:
                        if isinstance(each_ui, QtWidgets.QWidget):
                            parentObject.addWidget(each_ui)
                        else:
                            tmp_holder = QtWidgets.QWidget()
                            tmp_holder.setLayout(each_ui)
                            parentObject.addWidget(tmp_holder)
                elif isinstance(parentObject, QtWidgets.QTabWidget):
                    tab_names = insert_opt.replace('(','').replace(')','').split(',')
                    for i in range( len(ui_list) ):
                        each_tab = ui_list[i]
                        each_name = 'tab_'+str(i)
                        if i < len(tab_names):
                            if tab_names[i] != '':
                                each_name = tab_names[i]
                        if isinstance(each_tab, QtWidgets.QWidget):
                            parentObject.addTab(each_tab, each_name)
                        else:
                            tmp_holder = QtWidgets.QWidget()
                            tmp_holder.setLayout(each_tab)
                            parentObject.addTab(tmp_holder, each_name)
            return parentObject
    def quickSplitUI(self, name, part_list, type):
        split_type = QtCore.Qt.Horizontal
        if type == 'v':
            split_type = QtCore.Qt.Vertical
        self.uiList[name]=QtWidgets.QSplitter(split_type)
        
        for each_part in part_list:
            if isinstance(each_part, QtWidgets.QWidget):
                self.uiList[name].addWidget(each_part)
            else:
                tmp_holder = QtWidgets.QWidget()
                tmp_holder.setLayout(each_part)
                self.uiList[name].addWidget(tmp_holder)
        return self.uiList[name]
        
    def quickTabUI(self, name, tab_list, tab_names):
        self.uiList[name]=QtWidgets.QTabWidget()
        self.uiList[name].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
        for i in range( len(tab_list) ):
            each_tab = tab_list[i]
            each_name = tab_names[i]
            if isinstance(each_tab, QtWidgets.QWidget):
                self.uiList[name].addTab(each_tab, each_name)
            else:
                tmp_holder = QtWidgets.QWidget()
                tmp_holder.setLayout(each_tab)
                self.uiList[name].addTab(tmp_holder, each_name)
        return self.uiList[name]
        
    def quickGrpUI(self, ui_name, ui_label, ui_layout):
        self.uiList[ui_name] = QtWidgets.QGroupBox(ui_label)
        if isinstance(ui_layout, QtWidgets.QLayout):
            self.uiList[ui_name].setLayout(ui_layout)
        elif isinstance(ui_layout, str):
            ui_layout = self.quickLayout(ui_name+"_layout", ui_layout)
            self.uiList[ui_name].setLayout(ui_layout)
        return [self.uiList[ui_name], ui_layout]
    
    def quickPolicy(self, ui_list, w, h):
        if not isinstance(ui_list, (list, tuple)):
            ui_list = [ui_list]
        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
        policyList = ( QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored)
        for each_ui in ui_list:
            if isinstance(each_ui, str):
                each_ui = self.uiList[each_ui]
            each_ui.setSizePolicy(policyList[w],policyList[h])
    
    def quickInfo(self, info):
        self.statusBar().showMessage(info)            
    def quickMsg(self, msg):
        tmpMsg = QtWidgets.QMessageBox() # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        tmpMsg.setText(msg)
        tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        tmpMsg.exec_()
    def quickMsgAsk(self, msg, mode=0, choice=[]):
        # getItem, getInteger, getDouble, getText
        modeOpt = (QtWidgets.QLineEdit.Normal, QtWidgets.QLineEdit.NoEcho, QtWidgets.QLineEdit.Password, QtWidgets.QLineEdit.PasswordEchoOnEdit)
        # option: QtWidgets.QInputDialog.UseListViewForComboBoxItems
        if len(choice)==0:
            txt, ok = QtWidgets.QInputDialog.getText(self, "Input", msg, modeOpt[mode])
            return (unicode(txt), ok)
        else:
            txt, ok = QtWidgets.QInputDialog.getItem(self, "Input", msg, choice, 0, 0)
            return (unicode(txt), ok)
    def quickFileAsk(self, type, ext=None):
        if ext == None:
            ext = "RAW data (*.json);;RAW binary data(*.dat);;Format Txt(*{0});;AllFiles(*.*)".format(self.fileType)
        else:
            if ext == '':
                ext = "AllFiles(*.*)"
            else:
                if not ext.startswith('.'):
                    ext = '.'+ext # standard ext ref format
                ext = '{0}(*{0});;AllFiles(*.*)'.format(ext)
        file = ""
        if type == 'export':
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File","",ext)
        elif type == 'import':
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File","",ext)
        if isinstance(file, (list, tuple)):
            file = file[0] # for deal with pyside case
        else:
            file = unicode(file) # for deal with pyqt case
        return file
    def quickFolderAsk(self):
        return unicode(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
    def mui_to_qt(self, mui_name):
        if hostMode != "maya":
            return
        ptr = mui.MQtUtil.findControl(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findLayout(mui_name)
        if ptr is None:
            ptr = mui.MQtUtil.findMenuItem(mui_name)
        if ptr is not None:
            if qtMode in (0,2):
                # ==== for pyside ====
                return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)
            elif qtMode in (1,3):
                # ==== for PyQt====
                return sip.wrapinstance(long(ptr), QtCore.QObject)
    def qt_to_mui(self, qt_obj):
        if hostMode != "maya":
            return
        ref = None
        if qtMode in (0,2):
            # ==== for pyside ====
            ref = long(shiboken.getCppPointer(qt_obj)[0])
        elif qtMode in (1,3):
            # ==== for PyQt====
            ref = long(sip.unwrapinstance(qt_obj))
        if ref is not None:
            return mui.MQtUtil.fullName(ref)
