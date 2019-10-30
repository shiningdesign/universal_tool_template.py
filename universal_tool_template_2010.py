# Univeral Tool Template v20.1
tpl_ver = 20.10
tpl_date = 191003
print("tpl_ver: {0}-{1}".format(tpl_ver, tpl_date))
# by ying - https://github.com/shiningdesign/universal_tool_template.py

import importlib
import sys
# ---- hostMode ----
hostMode = ''
hostModeList = [
    ['maya', {'mui':'maya.OpenMayaUI', 'cmds':'maya.cmds'} ],
    ['nuke', {'nuke':'nuke', 'nukescripts':'nukescripts'} ],
    ['fusion', {'fs':'fusionscript'} ],
    ['houdini', {'hou':'hou'} ],
    ['blender', {'bpy':'bpy'} ],
    ['npp', {'Npp':'Npp'} ],
]
for name, libs in hostModeList:
    try:
        for x in libs.keys():
            globals()[x] = importlib.import_module(libs[x])
        hostMode = name
        break
    except ImportError:
        pass
if hostMode == '':
    hostMode = 'desktop'
print('Host: {0}'.format(hostMode))

# ---- qtMode ----
qtMode = 0 # 0: PySide; 1 : PyQt, 2: PySide2, 3: PyQt5
qtModeList = ('PySide', 'PyQt4', 'PySide2', 'PyQt5')
try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    qtMode = 0
    if hostMode == "maya":
        import shiboken
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        qtMode = 2
        if hostMode == "maya":
            import shiboken2 as shiboken
    except ImportError:
        try:
            from PyQt4 import QtGui,QtCore
            import PyQt4.QtGui as QtWidgets
            import sip
            qtMode = 1
        except ImportError:
            from PyQt5 import QtGui,QtCore,QtWidgets
            import sip
            qtMode = 3
print('Qt: {0}'.format(qtModeList[qtMode]))

# ---- pyMode ----
# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    # lambda s: str(s) # this works for function but not for class check
    unicode = str
if sys.version_info[:3][0]>=3:
    reload = importlib.reload # add reload

pyMode = '.'.join([ str(n) for n in sys.version_info[:3] ])
print("Python: {0}".format(pyMode))

# ---- osMode ----
osMode = 'other'
if sys.platform in ['win32','win64']:
    osMode = 'win'
elif sys.platform == 'darwin':
    osMode = 'mac'
elif sys.platform == 'linux2':
    osMode = 'linux'
print("OS: {0}".format(osMode))

# ---- template module list ----
import os # for path and language code
from functools import partial # for partial function creation
import json # for ascii data output
import re # for name pattern
import subprocess # for cmd call

#=======================================
#  UniversalToolUI template class
#=======================================

class UniversalToolUI(QtWidgets.QMainWindow): 
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # class property
        self.tpl_ver = tpl_ver
        self.tpl_date = tpl_date
        self.version = '0.1'
        self.date = '2017.01.01'
        self.log = 'no version log in user class'
        self.help = 'no help guide in user class'
        
        # class info
        self.name = self.__class__.__name__
        self.fileType='.{0}_EXT'.format(self.name)
        
        # class path and icon
        self.location = ''
        if getattr(sys, 'frozen', False):
            self.location = sys.executable # frozen case - cx_freeze
        else:
            self.location = os.path.realpath(sys.modules[self.__class__.__module__].__file__)
        self.iconPath = os.path.join(os.path.dirname(self.location),'icons',self.name+'.png')
        self.iconPix = QtGui.QPixmap(self.iconPath)
        self.icon = QtGui.QIcon(self.iconPath)
        
        # class data
        self.hotkey = {}
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        self.memoData['font_size_default'] = QtGui.QFont().pointSize()
        self.memoData['font_size'] = self.memoData['font_size_default']
        self.memoData['last_export'] = ''
        self.memoData['last_import'] = ''
        self.memoData['last_browse'] = ''
            
        # core function variable
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
    
    def setupMenu(self):
        if 'help_menu' in self.uiList.keys():
            self.uiList['helpGuide_msg'] = self.help
            self.uiList['helpLog_msg'] = self.log
            item_list = [
                ('helpHostMode_atnNone', 'Host Mode - {}'.format(hostMode) ),
                ('helpPyMode_atnNone','Python Mode - {}'.format(pyMode) ),
                ('helpQtMode_atnNone','Qt Mode - {}'.format(qtModeList[qtMode]) ),
                ('helpTemplate_atnNone','Universal Tool Teamplate - {0}.{1}'.format(tpl_ver, tpl_date) ),
                ('_','_'),
                ('helpGuide_atnMsg','Usage Guide'),
                ('helpLog_atnMsg','About v{0} - {1}'.format(self.version, self.date) ),
            ]
            menu_str = '|'.join(['{0};{1}'.format(*x) for x in item_list])
            self.qui_menu(menu_str, 'help_menu')
            # tip info
            self.uiList['helpTemplate_atnNone'].setStatusTip('based on Univeral Tool Template v{0} by Shining Ying - https://github.com/shiningdesign/universal{1}tool{1}template.py'.format(tpl_ver,'_'))
    
    def setupWin(self):
        self.setWindowTitle(self.name + " - v" + self.version + " - host: " + hostMode)
        self.setWindowIcon(self.icon)
        
    def setupUI(self, layout='grid'):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        self.qui('main_layout;{0}'.format(layout))
        main_widget.setLayout(self.uiList['main_layout'])

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
                
    #=======================================
    # ui response functions
    #=======================================
    def ____ui_response_functions____():
        pass
    def default_action(self, ui_name, *argv):
        print("No action defined for this UI element: "+ui_name)
    def default_message(self, ui_name):
        prefix = ui_name.rsplit('_', 1)[0]
        msgName = prefix+"_msg"
        msg_txt = msgName + " is not defined in uiList."
        if msgName in self.uiList:
            msg_txt = self.uiList[msgName]
        self.quickMsg(msg_txt)
    def default_menu_call(self, ui_name, point):
        if ui_name in self.uiList.keys() and ui_name+'_menu' in self.uiList.keys():
            self.uiList[ui_name+'_menu'].exec_(self.uiList[ui_name].mapToGlobal(point))
    def toggleTop_action(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.show()
    def hotkey_action(self):
        txt_list = []
        for each_key in sorted(self.hotkey.keys()):
            txt_list.append(each_key+' : '+unicode(self.hotkey[each_key].key().toString()))
        self.quickMsg('\n'.join(txt_list))
        
    #=======================================
    # ui feedback functions
    #=======================================
    def ____ui_feedback_functions____():
        pass
    def quickInfo(self, info, force=0):
        if hasattr( self.window(), "quickInfo") and force == 0:
            self.window().statusBar().showMessage(info)
        else:
            self.statusBar().showMessage(info)
    def quickMsg(self, msg, block=1, ask=0):
        tmpMsg = QtWidgets.QMessageBox(self) # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        lineCnt = len(msg.split('\n'))
        if lineCnt > 25:
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(1)
            content = QtWidgets.QWidget()
            scroll.setWidget(content)
            layout = QtWidgets.QVBoxLayout(content)
            tmpLabel = QtWidgets.QLabel(msg)
            tmpLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            layout.addWidget(tmpLabel)
            tmpMsg.layout().addWidget(scroll, 0, 0, 1, tmpMsg.layout().columnCount())
            tmpMsg.setStyleSheet("QScrollArea{min-width:600 px; min-height: 400px}")
        else:
            tmpMsg.setText(msg)
        if block == 0:
            tmpMsg.setWindowModality( QtCore.Qt.NonModal )
        if ask==0:
            tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        else:
            tmpMsg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        if block:
            value = tmpMsg.exec_()
            if value == QtWidgets.QMessageBox.Ok:
                return 1
            else:
                return 0
        else:
            tmpMsg.show()
            return 0
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
    def quickFileAsk(self, type, ext=None, dir=None):
        if ext == None:
            ext = "RAW data (*.json);;RAW binary data (*.dat);;Format Txt (*{0});;AllFiles (*.*)".format(self.fileType)
        elif isinstance(ext, (str,unicode)):
            if ';;' not in ext:
                if ext == '':
                    ext = 'AllFiles (*.*)'
                else:
                    ext = self.extFormat(ext) + ';;AllFiles (*.*)'
        elif isinstance(ext, (tuple,list)):
            if len(ext) > 0 and isinstance(ext[0], (tuple,list)):
                tmp_list = [self.extFormat(x) for x in ext]
                tmp_list.append('AllFiles (*.*)')
                ext = ';;'.join(tmp_list)
            else:
                ext = ';;'.join([self.extFormat(x) for x in ext].append('AllFiles(*.*)')) 
        elif isinstance(ext, dict):
            tmp_list = [self.extFormat(x) for x in ext.items()]
            tmp_list.append('AllFiles (*.*)')
            ext = ';;'.join(tmp_list)
        else:
            ext = "AllFiles (*.*)"
        file = ''
        if type == 'export':
            if dir == None:
                dir = self.memoData['last_export']
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",dir,ext)
        elif type == 'import':
            if dir == None:
                dir = self.memoData['last_import']
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",dir,ext)
        if isinstance(file, (list, tuple)):
            file = file[0] # for deal with pyside case
        else:
            file = unicode(file) # for deal with pyqt case
        # save last dir in memoData
        if file != '':
            if type == 'export':
                self.memoData['last_export'] = os.path.dirname(file) #QFileInfo().path()
            elif type == 'import':
                self.memoData['last_import'] = os.path.dirname(file)
        return file
    def extFormat(self, ext):
        if isinstance(ext, (tuple,list)):
            ext = '{0} (*.{1})'.format(ext[1],ext[0])
        else:
            if ext.startswith('.'):
                ext = ext[1:]
            ext = '{0} (*.{0})'.format(ext)
        return ext
    def quickFolderAsk(self,dir=None):
        if dir == None:
            dir = self.memoData['last_browse']
            if self.parent is not None and hasattr(self.parent, 'memoData'):
                dir = self.parent.memoData['last_browse']
        folder = unicode(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory",dir))
        if folder != '':
            self.memoData['last_browse'] = folder
        return folder
        
    #=======================================
    # file data functions
    #=======================================
    def ____file_data_functions____():
        pass
    def readDataFile(self,file,binary=0):
        if binary != 0:
            print('Lite no longer support binary format')
        with open(file) as f:
            data = json.load(f)
        return data
    def writeDataFile(self,data,file,binary=0):
        if binary != 0:
            print('Lite no longer support binary format')
        with open(file, 'w') as f:
            json.dump(data, f)
    def readTextFile(self, file):
        with open(file) as f:
            txt = f.read()
        return txt
    def writeTextFile(self, txt, file, b=0):
        b = '' if b==0 else 'b'
        with open(file, 'w'+b) as f:
            f.write(txt)
    def dict_merge(self, default_dict, extra_dict, addKey=0):
        # dictionary merge, with optional adding extra data from extra_dict
        new_dict = {}
        for key in default_dict.keys():
            if not isinstance( default_dict[key], dict ):
                # value case
                if key in extra_dict.keys():
                    is_same_text_type = isinstance(extra_dict[key], (str,unicode)) and isinstance(default_dict[key], (str,unicode))
                    is_same_non_text_type = type(extra_dict[key]) is type(default_dict[key])
                    if is_same_text_type or is_same_non_text_type:
                        print('use config file value for key: '+key)
                        new_dict[key] = extra_dict[key]
                    else:
                        new_dict[key] = default_dict[key]
                else:
                    new_dict[key] = default_dict[key]
            else:
                # dictionary case
                if key in extra_dict.keys() and isinstance( extra_dict[key], dict ):
                    new_dict[key] = self.dict_merge( default_dict[key], extra_dict[key], addKey )
                else:
                    new_dict[key] = default_dict[key]
        # optional, add additional keys
        if addKey == 1:
            for key in [ x for x in extra_dict.keys() if x not in default_dict.keys() ]:
                new_dict[key] = extra_dict[key]
        return new_dict
    #=======================================
    # ui text functions
    #=======================================
    def ____ui_text_functions____():
        pass
    def fontNormal_action(self, uiClass_list=[]):
        if len(uiClass_list) == 0:
            uiClass_list = 'QLabel,QPushButton'.split(',')
        self.memoData['font_size'] = self.memoData['font_size_default']
        self.setStyleSheet( "{0} { font-size: {1}pt;}".format(','.join(uiClass_list), self.memoData['font_size']) )
    def fontUp_action(self, uiClass_list=[]):
        if len(uiClass_list) == 0:
            uiClass_list = 'QLabel,QPushButton'.split(',')
        self.memoData['font_size'] += 2
        self.setStyleSheet( "{0} { font-size: {1}pt;}".format(','.join(uiClass_list), self.memoData['font_size']) )
    def fontDown_action(self, uiClass_list=[]):
        if len(uiClass_list) == 0:
            uiClass_list = 'QLabel,QPushButton'.split(',')
        if self.memoData['font_size'] >= self.memoData['font_size_default']:
            self.memoData['font_size'] -= 2
            self.setStyleSheet( "{0} { font-size: {1}pt;}".format(','.join(uiClass_list), self.memoData['font_size']) )
    def loadLang(self, build_menu=1):
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
        lang_menu = 'language_menu'
        if build_menu == 1:
            self.qui_menubar('language_menu;&Language')
            self.qui_menu('langDefault_atnLang;Default | _', lang_menu)
            self.uiList['langDefault_atnLang'].triggered.connect(partial(self.setLang,'default'))
            
        # scan for language file
        lang_path = os.path.dirname(self.location)
        baseName = os.path.splitext( os.path.basename(self.location) )[0]
        for file in self.getPathChild(lang_path, pattern=baseName+'_lang_[a-zA-Z]+.json', isfile=1):
            langName = re.findall(baseName+'_lang_(.+)\.json', file)
            if len(langName) == 1:
                langName = langName[0].upper()
                self.memoData['lang'][ langName ] = self.readDataFile( os.path.join(lang_path, file) )
                if build_menu == 1:
                    self.qui_menu('{0}_atnLang;{0}'.format(langName), lang_menu)
                    self.uiList[langName+'_atnLang'].triggered.connect(partial(self.setLang,langName))
        # if no language file detected, add export default language option
        if build_menu == 1:
            if isinstance(self, QtWidgets.QMainWindow) and len(self.memoData['lang']) == 1:
                self.qui_menu('langExport_atnLang;Export Default Language', lang_menu)
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
            
    #=======================================
    # os functions
    #=======================================
    def ____os_functions____():
        pass
    def openFolder(self, folderPath):
        if os.path.isfile(folderPath):
            folderPath = os.path.dirname(folderPath)
        if os.path.isdir(folderPath):
            cmd_list = None
            if sys.platform == 'darwin':
                cmd_list = ['open', '--', folderPath]
            elif sys.platform == 'linux2':
                cmd_list = ['xdg-open', folderPath]
            elif sys.platform in ['win32','win64']:
                cmd_list = ['explorer', folderPath.replace('/','\\')]
            if cmd_list != None:
                try:
                    subprocess.check_call(cmd_list)
                except subprocess.CalledProcessError:
                    pass # handle errors in the called executable
                except OSError:
                    pass # executable not found
    def openFile(self, filePath):
        if sys.platform in ['win32','win64']:
            os.startfile(filePath)
        elif sys.platform == 'darwin':
            os.open(filePath)
        elif sys.platform == 'linux2':
            os.xdg-open(filePath)
    def newFolder(self, parentPath, name=None):
        if os.path.isfile(parentPath):
            parentPath = os.path.dirname(parentPath)
        created = 0
        if name == None:
            name, ok = self.quickMsgAsk('Enter the folder name:')
            if not ok or name=='':
                return
        create_path = os.path.join(parentPath, name)
        if os.path.isdir(create_path):
            self.quickMsg('Already Exists')
        else:
            try: 
                os.makedirs(create_path)
                created = 1
            except OSError:
                self.quickMsg('Error on creation user data folder')
        return created
    def getPathChild(self, scanPath, pattern='', isfile=0):
        resultList =[]
        scanPath = unicode(scanPath)
        if not os.path.isdir(scanPath):
            return resultList
        if isfile == 0:
            resultList = [x for x in os.listdir(scanPath) if os.path.isdir(os.path.join(scanPath,x))]
        elif isfile == 1:
            resultList = [x for x in os.listdir(scanPath) if os.path.isfile(os.path.join(scanPath,x))]
        else:
            resultList = os.listdir(scanPath)
        if pattern != '':
            cur_pattern = re.compile(pattern)
            resultList = [x for x in resultList if cur_pattern.match(x)]
        resultList.sort()
        return resultList
    
    #=======================================
    #  qui functions
    #=======================================
    def ____qui_functions____():
        pass
    
    def setAsUI(self):
        # turn win to widget
        self.setWindowFlags(QtCore.Qt.Widget)
        self.statusBar().hide()
        self.uiList['main_layout'].setContentsMargins(0, 0, 0, 0)
    def qui_key(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect( func )
    def qui_menubar(self, menu_list_str):
        if not isinstance(self, QtWidgets.QMainWindow):
            print("Warning: Only QMainWindow can have menu bar.")
            return
        menubar = self.menuBar()
        create_opt_list = [ x.strip() for x in menu_list_str.split('|') ]
        for each_creation in create_opt_list:
            ui_info = [ x.strip() for x in each_creation.split(';') ]
            menu_name = ui_info[0]
            menu_title = ''
            if len(ui_info) > 1:
                menu_title = ui_info[1]
            if menu_name not in self.uiList.keys():
                self.uiList[menu_name] = QtWidgets.QMenu(menu_title)
            menubar.addMenu(self.uiList[menu_name])
    def qui_menu(self, action_list_str, menu_str):
        # qui menu creation
        # syntax: self.qui_menu('right_menu_createFolder_atn;Create Folder,Ctrl+D | right_menu_openFolder_atn;Open Folder', 'right_menu')
        if menu_str not in self.uiList.keys():
            self.uiList[menu_str] = QtWidgets.QMenu()
        create_opt_list = [ x.strip() for x in action_list_str.split('|') ]
        for each_creation in create_opt_list:
            ui_info = [ x.strip() for x in each_creation.split(';') ]
            atn_name = ui_info[0]
            atn_title = ''
            atn_hotkey = ''
            if len(ui_info) > 1:
                options = ui_info[1].split(',')
                atn_title = '' if len(options) < 1 else options[0]
                atn_hotkey = '' if len(options) < 2 else options[1]
            if atn_name != '':
                if atn_name == '_':
                    self.uiList[menu_str].addSeparator()
                else:
                    if atn_name not in self.uiList.keys():
                        self.uiList[atn_name] = QtWidgets.QAction(atn_title, self)
                        if atn_hotkey != '':
                            self.uiList[atn_name].setShortcut(QtGui.QKeySequence(atn_hotkey))
                    self.uiList[menu_str].addAction(self.uiList[atn_name])
                    
    def qui_class(self,uiName,uiInfo=[]):
        if not isinstance(uiInfo, (list, tuple)):
            uiInfo = [uiInfo]
            
        uiClass = uiName.rsplit('_',1)[-1]
        if uiClass == 'layout' and len(uiInfo)>0:
            uiClass = uiInfo[0]
        if uiClass in self.qui_user_dict:
            uiClass = self.qui_user_dict[uiClass] # first, try user dict
        elif uiClass in self.qui_core_dict:
            uiClass = self.qui_core_dict[uiClass] # then, try default core dict
        # check
        if hasattr(QtWidgets, uiClass) or uiClass in sys.modules:
            return [uiClass,1]
        else:
            return [uiClass,0]

    def qui(self, ui_list_string, parent_ui_string='', insert_opt=''):
        # ui format: 
        # 'process_label;Process Path: | process_file_input | process_file_btn;Process'
        # 'extra_check;Add Extra'
        # 'option_choice;(TypeA,TypeB) | file_tree;(Name,Path) | option_space;(5,5,5,3)'
        # parent format:
        # 'main_layout;vbox', 'main_hbox', 'main_form'
        # 'main_grid' <h/v>
        # 'main_split;v', 
        # 'main_grp;hbox;Process', 
        # 'main_tab;v' <(Media,Edit,Publish)>
        ui_string_list = [ x.strip() for x in ui_list_string.split('|') if x.strip()!='']
        ui_data_list = []
        for ui_string in ui_string_list:
            creation_result = self.qui_data(ui_string)
            if creation_result is not None:
                ui_data_list.append(creation_result)
        # - ui parent
        if parent_ui_string == '':
            return ui_data_list
        else:
            parent_ui_data = self.qui_data(parent_ui_string)
            if parent_ui_data is not None:
                self.qui_insert(ui_data_list, parent_ui_data, insert_opt)
                return parent_ui_data['name']
            else:
                return
        
    def qui_data(self, ui_string):
        # ui_string to ui_data, if not created, create obj in ui_data
        # reference
        class_error_msg = "WARNING: ({0}) is not defined in self.qui_user_dict and it is not a Qt widget class or User class; Item {1} Ignored."
        # process
        info_list = ui_string.split(';')
        uiName = info_list[0]
        uiLabel = ''
        uiInfo = []
        if '@' in uiName:
            uiName,uiLabel = uiName.split('@',1)
        if len(info_list) > 1:
            uiInfo = info_list[1:] # .split(',')
            
        if uiName in self.uiList.keys():
            # case 1: already created
            return {'name':uiName, 'obj':self.uiList[uiName], 'label':uiLabel}
        else:
            # case 2: create obj
            uiClass, isValid = self.qui_class(uiName, uiInfo)
            if not isValid:
                print(class_error_msg.format(uiClass, uiName))
                return None
            else:
                if len(uiInfo)==0 and uiClass in ('QPushButton','QLabel'):
                    uiInfo.append(uiName) # give empty button and label a place holder name
                return self.qui_obj( {'name': uiName, 'class': uiClass, 'label':uiLabel, 'info': uiInfo} )
                
    def qui_obj(self, ui_data):
        # ui_data to obj generation
        # reference value
        policyList = ( 
            QtWidgets.QSizePolicy.Fixed, 
            QtWidgets.QSizePolicy.Minimum, 
            QtWidgets.QSizePolicy.Maximum, 
            QtWidgets.QSizePolicy.Preferred, 
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.MinimumExpanding, 
            QtWidgets.QSizePolicy.Ignored,
        )
        
        # case 1: already has obj created, just return
        if 'obj' in ui_data.keys():
            return ui_data
        
        # case 2: create obj
        uiName = ui_data['name']
        uiClass = ui_data['class']
        uiInfo = []
        if 'info' in ui_data.keys():
            uiInfo = ui_data['info']
        # -- 3rd part widget, create like UI_Class.UI_Class()
        if not hasattr(QtWidgets, uiClass):
            self.uiList[uiName] = getattr(sys.modules[uiClass], uiClass)(*uiInfo)
            ui_data['obj'] = self.uiList[uiName]
            return ui_data
            
        # -- QtWidgets
        if uiClass in ('QVBoxLayout', 'QHBoxLayout', 'QFormLayout', 'QGridLayout'):
            # --- Qt Layout creation preset func
            if uiClass == "QFormLayout":
                self.uiList[uiName] = QtWidgets.QFormLayout()
                self.uiList[uiName].setLabelAlignment(QtCore.Qt.AlignLeft)
                self.uiList[uiName].setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)    
                ui_data['obj'] = self.uiList[uiName]
            elif uiClass == "QGridLayout":
                self.uiList[uiName] = QtWidgets.QGridLayout()
                ui_data['obj'] = self.uiList[uiName]
            elif uiClass == "QHBoxLayout":
                self.uiList[uiName] = QtWidgets.QHBoxLayout()
                self.uiList[uiName].setAlignment(QtCore.Qt.AlignTop)
                ui_data['obj'] = self.uiList[uiName]
            else:
                self.uiList[uiName] = QtWidgets.QVBoxLayout()
                self.uiList[uiName].setAlignment(QtCore.Qt.AlignTop)
                ui_data['obj'] = self.uiList[uiName]
        elif uiClass in ('QSplitter', 'QTabWidget', 'QGroupBox'):
            # --- Qt container creation
            if uiClass == 'QSplitter':
                split_type = QtCore.Qt.Horizontal
                if 'v' in uiInfo:
                    split_type = QtCore.Qt.Vertical
                self.uiList[uiName]=QtWidgets.QSplitter(split_type)
                ui_data['obj'] = self.uiList[uiName]
            elif uiClass == 'QTabWidget':
                self.uiList[uiName]=QtWidgets.QTabWidget()
                self.uiList[uiName].setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 100px; }")
                if 'v' in uiInfo:
                    self.uiList[uiName].setTabPosition(QtWidgets.QTabWidget.West)
                ui_data['obj'] = self.uiList[uiName]
            elif uiClass == 'QGroupBox':
                grp_layout_class = 'QVBoxLayout'
                if len(uiInfo)>0:
                    new_grp_layout_class, isValid = self.qui_class(uiName+"_layout", uiInfo[0])
                    if isValid:
                        grp_layout_class = new_grp_layout_class
                grp_title = uiName
                if len(uiInfo)== 2:
                    grp_title = uiInfo[-1]
                grp_layout_obj = self.qui_obj({'name':uiName+"_layout", 'class': grp_layout_class })['obj']
                self.uiList[uiName] = QtWidgets.QGroupBox(grp_title)
                self.uiList[uiName].setLayout(grp_layout_obj)
                ui_data['obj'] = self.uiList[uiName]
        elif uiClass == 'QComboBox':
            self.uiList[uiName] = QtWidgets.QComboBox()
            if len(uiInfo)>0:
                item_list = uiInfo[0].replace('(','').replace(')','').split(',')
                self.uiList[uiName].addItems(item_list)
            ui_data['obj'] = self.uiList[uiName]
        elif uiClass == 'QTreeWidget':
            self.uiList[uiName] = QtWidgets.QTreeWidget()
            if len(uiInfo)>0:
                label_list = uiInfo[0].replace('(','').replace(')','').split(',')
                self.uiList[uiName].setHeaderLabels(label_list)
            ui_data['obj'] = self.uiList[uiName]
        elif uiClass == 'QSpacerItem':
            # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
            # factors in fighting for space: horizontalStretch
            # extra space: setContentsMargins and setSpacing
            # ref: http://www.cnblogs.com/alleyonline/p/4903337.html
            val = [5,5,5,3]
            for i in range(len(uiInfo)):
                val[i] = int(uiInfo[i])
            self.uiList[uiName] = QtWidgets.QSpacerItem(val[0],val[1], policyList[val[2]], policyList[val[3]] )
            ui_data['obj'] = self.uiList[uiName]
        else:
            if len(uiInfo) == 0:
                self.uiList[uiName] = getattr(QtWidgets, uiClass)()
                ui_data['obj'] = self.uiList[uiName]
            else:
                self.uiList[uiName] = getattr(QtWidgets, uiClass)(*uiInfo)
                ui_data['obj'] = self.uiList[uiName]
        
        return ui_data
     
    def qui_insert(self, ui_data_list, parent_data, insert_opt=''):
        # get parentLayout inside parentObject
        parentObject = parent_data['obj']
        if isinstance(parentObject, QtWidgets.QGroupBox):
            parentObject = parentObject.layout()
        
        if isinstance(parentObject, QtWidgets.QBoxLayout):
            # layout
            for ui_data in ui_data_list:
                ui = ui_data['obj']
                if isinstance(ui, QtWidgets.QWidget):
                    parentObject.addWidget(ui)
                elif isinstance(ui, QtWidgets.QSpacerItem):
                    parentObject.addItem(ui)
                elif isinstance(ui, QtWidgets.QLayout):
                    parentObject.addLayout(ui)
        elif isinstance(parentObject, QtWidgets.QGridLayout):
            # grid: one row/colume operation only
            insertRow = parentObject.rowCount()
            insertCol = parentObject.columnCount()
            for i in range(len(ui_data_list)):
                each_ui = ui_data_list[i]['obj']
                x = insertRow if insert_opt=="h" else i
                y = i if insert_opt=="h" else insertCol
                if isinstance(each_ui, QtWidgets.QWidget):
                    parentObject.addWidget(each_ui,x,y)
                elif isinstance(each_ui, QtWidgets.QSpacerItem):
                    parentObject.addItem(each_ui,x,y)
                elif isinstance(each_ui, QtWidgets.QLayout):
                    parentObject.addLayout(each_ui,x,y)
        elif isinstance(parentObject, QtWidgets.QFormLayout):
            for ui_data in ui_data_list:
                ui = ui_data['obj']
                name = ui_data['name']
                label = '' if 'label' not in ui_data.keys() else ui_data['label']
                if isinstance(ui, QtWidgets.QWidget) or isinstance(ui, QtWidgets.QLayout):
                    if label != '':
                        self.uiList[name+'_label'] = QtWidgets.QLabel(label)
                        parentObject.addRow(self.uiList[name+'_label'], ui)
                    else:
                        parentObject.addRow(ui)
        elif isinstance(parentObject, QtWidgets.QSplitter):
            # split
            for ui_data in ui_data_list:
                each_ui = ui_data['obj']
                if isinstance(each_ui, QtWidgets.QWidget):
                    parentObject.addWidget(each_ui)
                else:
                    tmp_holder = QtWidgets.QWidget()
                    tmp_holder.setLayout(each_ui)
                    parentObject.addWidget(tmp_holder)
        elif isinstance(parentObject, QtWidgets.QTabWidget):
            # tab
            tab_names = insert_opt.replace('(','').replace(')','').split(',')
            for i in range( len(ui_data_list) ):
                each_tab = ui_data_list[i]['obj']
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
                    
    def qui_policy(self, ui_list, w, h):
        # reference value
        policyList = ( 
            QtWidgets.QSizePolicy.Fixed, 
            QtWidgets.QSizePolicy.Minimum, 
            QtWidgets.QSizePolicy.Maximum, 
            QtWidgets.QSizePolicy.Preferred, 
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.MinimumExpanding, 
            QtWidgets.QSizePolicy.Ignored,
        )
        # 0 = fixed; 1 > min; 2 < max; 3 = prefered; 4 = <expanding>; 5 = expanding> Aggresive; 6=4 ignored size input
        if not isinstance(ui_list, (list, tuple)):
            ui_list = [ui_list]
        for each_ui in ui_list:
            if isinstance(each_ui, str):
                each_ui = self.uiList[each_ui]
            each_ui.setSizePolicy(policyList[w],policyList[h])
            
#############################################
# User Class creation
#############################################
version = '0.1'
date = '2019.07.05'
log = '''
#------------------------------
v0.1: (2019.07.05)
  * notes here
#------------------------------
'''
help = '''
wip
'''
# --------------------
#  user module list
# --------------------

class UserClassUI(UniversalToolUI):
    def __init__(self, parent=None, mode=0):
        UniversalToolUI.__init__(self, parent)
        
        # class variables
        self.version= version
        self.date = date
        self.log = log
        self.help = help
        
        # mode: example for receive extra user input as parameter
        self.mode = 0
        if mode in [0,1]:
            self.mode = mode # mode validator
        # Custom user variable
        #------------------------------
        # initial data
        #------------------------------
        self.memoData['data']=[]
        self.memoData['settingUI']=[]
        self.qui_user_dict = {} # e.g: 'edit': 'LNTextEdit',
        
        if isinstance(self, QtWidgets.QMainWindow):
            self.setupMenu()
        self.setupWin()
        self.setupUI()
        self.Establish_Connections()
        self.loadLang()
        self.loadData()
        
    #------------------------------
    # overwrite functions
    #------------------------------
    def setupMenu(self):
        self.qui_menubar('file_menu;&File | setting_menu;&Setting | help_menu;&Help')
        
        info_list = ['export', 'import','user']
        info_item_list = ['{0}Config_atn;{1} Config (&{2}),Ctrl+{2}'.format(info,info.title(),info.title()[0]) for info in info_list]+['_']
        self.qui_menu('|'.join(info_item_list), 'setting_menu')
        # toggle on top
        self.qui_menu('toggleTop_atn;Toggle Always-On-Top', 'setting_menu')
        # default help menu
        super(self.__class__,self).setupMenu()
    
    def setupWin(self):
        super(self.__class__,self).setupWin()
        # self.setGeometry(500, 300, 250, 110) # self.resize(250,250)
        if hostMode == "desktop":
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
        
    def setupUI(self):
        super(self.__class__,self).setupUI('grid')
        #------------------------------
        # user ui creation part
        #------------------------------
        self.qui('box_btn;Box | sphere_btn;Sphere | ring_btn;Ring', 'my_layout;grid', 'h')
        self.qui('box2_btn;Box2 | sphere2_btn;Sphere2 | ring2_btn;Ring2', 'my_layout', 'h')
        
        self.qui('cat_btn;Cat | dog_btn;Dog | pig_btn;Pig', 'pet_layout;grid', 'v')
        self.qui('cat2_btn;Cat2 | dog2_btn;Dog2 | pig2_btn;Pig2', 'pet_layout', 'v')
        
        self.qui('name_input@Name:;John | email_input@Email:;test@test.com', 'entry_form')
        
        self.qui('user2_btn;User2 | info2_btn;Info2', 'my_grp;vbox;Personal Data')
        
        self.qui('source_txt | process_btn;Process and Update', 'upper_vbox')
        self.qui('upper_vbox | result_txt', 'input_split;v')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('test_space;5;5;5;3 | testSpace_btn;Test Space', 'testSpace_layout;hbox')
        self.qui('my_layout | my_table | input_split | entry_form | fileBtn_layout | pet_layout | my_grp | testSpace_layout', 'main_layout')
        
        cur_table = self.uiList['my_table']
        cur_table.setRowCount(0)
        cur_table.setColumnCount(1)
        cur_table.insertColumn(cur_table.columnCount())
        cur_item = QtWidgets.QTableWidgetItem('ok') #QtWidgets.QPushButton('Cool') #
        cur_table.insertRow(0)
        cur_table.setItem(0,1, cur_item) #setCellWidget(0,0,cur_item)
        cur_table.setHorizontalHeaderLabels(('a','b'))
        '''
        self.qui('source_txt | process_btn;Process and Update', 'upper_vbox')
        self.qui('upper_vbox | result_txt', 'input_split;v')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('input_split | fileBtn_layout', 'main_layout')
        '''
        self.memoData['settingUI']=[]
        #------------- end ui creation --------------------
        keep_margin_layout = ['main_layout']
        keep_margin_layout_obj = []
        # add tab layouts
        for each in self.uiList.values():
            if isinstance(each, QtWidgets.QTabWidget):
                for i in range(each.count()):
                    keep_margin_layout_obj.append( each.widget(i).layout() )
        for name, each in self.uiList.items():
            if isinstance(each, QtWidgets.QLayout) and name not in keep_margin_layout and not name.endswith('_grp_layout') and each not in keep_margin_layout_obj:
                each.setContentsMargins(0, 0, 0, 0)
        self.quickInfo('Ready')
        # self.statusBar().hide()
        
    def Establish_Connections(self):
        super(self.__class__,self).Establish_Connections()
        # custom ui response
        # shortcut connection
        self.hotkey = {}
        # self.hotkey['my_key'] = QtWidgets.QShortcut(QtGui.QKeySequence( "Ctrl+1" ), self)
        # self.hotkey['my_key'].activated.connect(self.my_key_func)
        
    def loadData(self):
        print("Load data")
        # load config
        config = {}
        config['root_name'] = 'root_default_name'
        # overload config file if exists next to it
        # then, save merged config into self.memoData['config']
        prefix, ext = os.path.splitext(self.location)
        config_file = prefix+'_config.json'
        if os.path.isfile(config_file):
            external_config = self.readDataFile(config_file)
            print('info: External config file found.')
            if isinstance( external_config, dict ):
                self.memoData['config'] = self.dict_merge(config, external_config, addKey=1)
                print('info: External config merged.')
            else:
                self.memoData['config'] = config
                print('info: External config is not a dict and ignored.')
        else:
            self.memoData['config'] = config
        
        # load user setting
        user_setting = {}
        if self.mode == 0:
            # for standalone mode only
            user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
            user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
            if os.path.isfile(user_setting_filePath):
                user_setting = self.readDataFile(user_setting_filePath)
                if 'sizeInfo' in user_setting:
                    self.setGeometry(*user_setting['sizeInfo'])
        # custome setting loading here
        preset = {}
        for ui in self.memoData['settingUI']:
            if ui in user_setting:
                preset[ui]=user_setting[ui]
        #self.updateUI(preset)
        
    def closeEvent(self, event):
        if self.mode == 0:
            # for standalone mode only
            user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
            if not os.path.isdir(user_dirPath):
                try: 
                    os.makedirs(user_dirPath)
                except OSError:
                    print('Error on creation user data folder')
            if not os.path.isdir(user_dirPath):
                print('Fail to create user dir.')
                return
            # save setting
            user_setting = {}
            geoInfo = self.geometry()
            user_setting['sizeInfo'] = [geoInfo.x(), geoInfo.y(), geoInfo.width(), geoInfo.height()]
            # custome setting saving here
            for ui in self.memoData['settingUI']:
                if ui.endswith('_choice'):
                    user_setting[ui] = unicode(self.uiList[ui].currentText())
                elif ui.endswith('_input'):
                    user_setting[ui] = unicode(self.uiList[ui].text())
                elif ui.endswith('_tab'):
                    user_setting[ui] = self.uiList[ui].currentIndex()
            user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
            self.writeDataFile(user_setting, user_setting_filePath)
        
    # - example button functions
    def updateUI(self, preset):
        for ui_name in preset:
            if ui_name.endswith('_choice'):
                if preset[ui_name] != '':
                    the_idx = self.uiList[ui_name].findText(preset[ui_name])
                    if the_idx != -1:
                        self.uiList[ui_name].setCurrentIndex(the_idx)
            elif ui_name.endswith('_input'):
                if preset[ui_name] != '':
                    self.uiList[ui_name].setText(preset[ui_name])
            elif ui_name.endswith('_tab'):
                self.uiList[ui_name].setCurrentIndex(preset[ui_name])
    def process_action(self): # (optional)
        config = self.memoData['config']
        print("Process ....")
        source_txt = unicode(self.uiList['source_txt'].toPlainText())
        # 2: update memory
        self.memoData['data'] = [row.strip() for row in source_txt.split('\n')]
        print("Update Result")
        txt=config['root_name']+'\n'+'\n'.join([('>>: '+row) for row in self.memoData['data']])
        self.uiList['result_txt'].setText(txt)
    
    # - example file io function
    def exportConfig_action(self):
        file= self.quickFileAsk('export', {'json':'JSON data file', 'xdat':'Pickle binary file'})
        if file == "":
            return
        # export process
        ui_data = self.memoData['config']
        # file process
        if file.endswith('.xdat'):
            self.writeDataFile(ui_data, file, binary=1)
        else:
            self.writeDataFile(ui_data, file)
        self.quickInfo("File: '"+file+"' creation finished.")
    def importConfig_action(self):
        file= self.quickFileAsk('import',{'json':'JSON data file', 'xdat':'Pickle binary file'})
        if file == "":
            return
        # import process
        ui_data = ""
        if file.endswith('.xdat'):
            ui_data = self.readDataFile(file, binary=1)
        else:
            ui_data = self.readDataFile(file)
        self.memoData['config'] = ui_data
        self.quickInfo("File: '"+file+"' loading finished.")
    def userConfig_action(self):
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        self.openFolder(user_dirPath)
        
#=======================================
#  window instance creation
#=======================================

import ctypes # for windows instance detection
single_UserClassUI = None
app_UserClassUI = None
def main(mode=0):
    # get parent window in Maya
    parentWin = None
    if hostMode == "maya":
        if qtMode in (0,2): # pyside
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        elif qtMode in (1,3): # PyQt
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
    # create app object for certain host
    global app_UserClassUI
    if hostMode in ('desktop', 'blender', 'npp', 'fusion'):
        # single instance app mode on windows
        if osMode == 'win':
            # check if already open for single desktop instance
            from ctypes import wintypes
            order_list = []
            result_list = []
            top = ctypes.windll.user32.GetTopWindow(None)
            if top: 
                length = ctypes.windll.user32.GetWindowTextLengthW(top)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(top, buff, length + 1)
                class_name = ctypes.create_string_buffer(200)
                ctypes.windll.user32.GetClassNameA(top, ctypes.byref(class_name), 200)
                result_list.append( [buff.value, class_name.value, top ])
                order_list.append(top)
                while True:
                    next = ctypes.windll.user32.GetWindow(order_list[-1], 2) # win32con.GW_HWNDNEXT
                    if not next:
                        break
                    length = ctypes.windll.user32.GetWindowTextLengthW(next)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(next, buff, length + 1)
                    class_name = ctypes.create_string_buffer(200)
                    ctypes.windll.user32.GetClassNameA(next, ctypes.byref(class_name), 200)
                    result_list.append( [buff.value, class_name.value, next] )
                    order_list.append(next)
            # result_list: [(title, class, hwnd int)]
            winTitle = 'UserClassUI' # os.path.basename(os.path.dirname(__file__))
            is_opened = 0
            for each in result_list:
                if re.match(winTitle+' - v[0-9.]* - host: desktop',each[0]) and each[1] == 'QWidget':
                    is_opened += 1
                    if is_opened == 1:
                        ctypes.windll.user32.SetForegroundWindow(each[2])
                        sys.exit(0) # 0: success, 1-127: bad error
                        return
        if hostMode in ('npp','fusion'):
            app_UserClassUI = QtWidgets.QApplication([])
        elif hostMode in ('houdini'):
            pass
        else:
            app_UserClassUI = QtWidgets.QApplication(sys.argv)
    
    #--------------------------
    # ui instance
    #--------------------------
    # Keep only one copy of windows ui in Maya
    global single_UserClassUI
    if single_UserClassUI is None:
        if hostMode == 'maya':
            single_UserClassUI = UserClassUI(parentWin, mode)
        elif hostMode == 'nuke':
            single_UserClassUI = UserClassUI(QtWidgets.QApplication.activeWindow(), mode)
        else:
            single_UserClassUI = UserClassUI()
    single_UserClassUI.show()
    ui = single_UserClassUI
    if hostMode != 'desktop':
        ui.activateWindow()
    
    # loop app object for certain host
    if hostMode in ('desktop'):
        sys.exit(app_UserClassUI.exec_())
    elif hostMode in ('npp','fusion'):
        app_UserClassUI.exec_()
    return ui

if __name__ == "__main__":
    main()