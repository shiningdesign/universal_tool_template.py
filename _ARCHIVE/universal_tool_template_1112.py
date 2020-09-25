# Univeral Tool Template v011.0
tpl_ver = 11.12
tpl_date = 181026
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
if sys.version_info[:3][0]<3:
    import cPickle # for binary data output
else:
    import _pickle as cPickle
import re # for name pattern
import ctypes # for windows instance detection
import subprocess # for cmd call

#=======================================
#  UniversalToolUI template class
#=======================================

class UniversalToolUI(QtWidgets.QMainWindow): 
    def __init__(self, parent=None, mode=0):
        QtWidgets.QMainWindow.__init__(self, parent)
        #------------------------------
        # class variables
        #------------------------------
        self.version = '0.1'
        self.date = '2017.01.01'
        self.log = 'no version log in user class'
        self.help = 'no help guide in user class'
        
        self.uiList={} # for ui obj storage
        self.memoData = {} # key based variable data storage
        self.memoData['font_size_default'] = QtGui.QFont().pointSize()
        self.memoData['font_size'] = self.memoData['font_size_default']
        self.memoData['last_export'] = ''
        self.memoData['last_import'] = ''
        self.name = self.__class__.__name__
        self.location = ''
        if getattr(sys, 'frozen', False):
            # frozen - cx_freeze
            self.location = sys.executable
        else:
            # unfrozen
            self.location = os.path.realpath(sys.modules[self.__class__.__module__].__file__)
            
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
    
    def setupStyle(self):
        # global app style setting for desktop
        if hostMode == "desktop":
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("QLineEdit:disabled{background-color: gray;}")
        
    def setupMenu(self):
        # global help menu
        if 'help_menu' in self.uiList.keys():
            # for info review
            self.qui_atn('helpHostMode_atnNone','Host Mode - {}'.format(hostMode),'Host Running.')
            self.qui_atn('helpPyMode_atnNone','Python Mode - {}'.format(pyMode),'Python Library Running.')
            self.qui_atn('helpQtMode_atnNone','Qt Mode - {}'.format(qtModeList[qtMode]),'Qt Library Running.')
            self.qui_atn('helpTemplate_atnNone','Universal Tool Teamplate - {0}.{1}'.format(tpl_ver, tpl_date),'based on Univeral Tool Template v{0} by Shining Ying - https://github.com/shiningdesign/universal{1}tool{1}template.py'.format(tpl_ver,'_'))
            self.uiList['helpGuide_msg'] = self.help
            self.qui_atn('helpGuide_atnMsg','Usage Guide','How to Usge Guide.')
            self.uiList['helpLog_msg'] = self.log
            self.qui_atn('helpLog_atnMsg','About v{0} - {1}'.format(self.version, self.date),'Vesion Log.')
            self.qui_menu('helpHostMode_atnNone | helpPyMode_atnNone | helpQtMode_atnNone | helpTemplate_atnNone | _ | helpGuide_atnMsg | helpLog_atnMsg', 'help_menu')
    
    def setupWin(self):
        self.setWindowTitle(self.name + " - v" + self.version + " - host: " + hostMode)
        self.setWindowIcon(self.icon)
        self.drag_position=QtGui.QCursor.pos() # initial win drag position
        
    def setupUI(self, layout='grid'):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = self.quickLayout(layout, 'main_layout') # grid for auto fill window size
        main_widget.setLayout(main_layout)

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
    #=======================================
    # ui feedback functions
    #=======================================
    def ____ui_feedback_functions____():
        pass
    def quickInfo(self, info):
        self.statusBar().showMessage(info)
    def quickMsg(self, msg, block=1):
        tmpMsg = QtWidgets.QMessageBox(self) # for simple msg that no need for translation
        tmpMsg.setWindowTitle("Info")
        lineCnt = len(msg.split('\n'))
        if lineCnt > 25:
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(1)
            content = QtWidgets.QWidget()
            scroll.setWidget(content)
            layout = QtWidgets.QVBoxLayout(content)
            layout.addWidget(QtWidgets.QLabel(msg))
            tmpMsg.layout().addWidget(scroll, 0, 0, 1, tmpMsg.layout().columnCount())
            tmpMsg.setStyleSheet("QScrollArea{min-width:600 px; min-height: 400px}")
        else:
            tmpMsg.setText(msg)
        if block == 0:
            tmpMsg.setWindowModality( QtCore.Qt.NonModal )
        tmpMsg.addButton("OK",QtWidgets.QMessageBox.YesRole)
        if block:
            tmpMsg.exec_()
        else:
            tmpMsg.show()
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
    def quickFolderAsk(self):
        return unicode(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
    def openFolder(self, folderPath):
        if os.path.isfile(folderPath):
            folderPath = os.path.dirname(folderPath)
        if os.path.isdir(folderPath):
            cmd_list = None
            if sys.platform == 'darwin':
                cmd_list = ['open', '--', folderPath]
            elif sys.platform == 'linux2':
                cmd_list = ['xdg-open', '--', folderPath]
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
    #=======================================
    # ui info functions
    #=======================================
    def ____ui_info_functions____():
        pass
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
    def input_check(self, ui_name):
        if ui_name in self.uiList.keys():
            return self.uiList[ui_name].isChecked()
        else:
            return
    def output_text(self, ui_name, text):
        if ui_name in self.uiList.keys():
            self.uiList[ui_name].setText(text)
    #=======================================
    # file data functions
    #=======================================
    def ____file_functions____():
        pass
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
    def fontNormal_action(self):
        self.memoData['font_size'] = self.memoData['font_size_default']
        self.setStyleSheet("QLabel,QPushButton { font-size: %dpt;}" % self.memoData['font_size'])
    def fontUp_action(self):
        self.memoData['font_size'] += 2
        self.setStyleSheet("QLabel,QPushButton { font-size: %dpt;}" % self.memoData['font_size'])
    def fontDown_action(self):
        if self.memoData['font_size'] >= self.memoData['font_size_default']:
            self.memoData['font_size'] -= 2
            self.setStyleSheet("QLabel,QPushButton { font-size: %dpt;}" % self.memoData['font_size'])
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
    #  qui functions
    #=======================================
    def ____ui_creation_functions____():
        pass
    def setAsUI(self):
        # turn win to widget
        self.setWindowFlags(QtCore.Qt.Widget)
        self.statusBar().hide()
        self.uiList['main_layout'].setContentsMargins(0, 0, 0, 0)
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
        return parent_uiName
        
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
    def qui_atn(self, ui_name, title, tip=None, icon=None, parent=None, key=None):
        self.uiList[ui_name] = QtWidgets.QAction(title, self)
        if icon!=None:
            self.uiList[ui_name].setIcon(QtGui.QIcon(icon))
        if tip !=None:
            self.uiList[ui_name].setStatusTip(tip)
        if key != None:
            self.uiList[ui_name].setShortcut(QtGui.QKeySequence(key))
        if parent !=None:
            if isinstance(parent, (str, unicode)) and parent in self.uiList.keys():
                self.uiList[parent].addAction(self.uiList[ui_name])
            elif isinstance(parent, QtWidgets.QMenu):
                parent.addAction(self.uiList[ui_name])
        return ui_name
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
    
    #=======================================
    # ui creation functions
    #=======================================
    
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
                        self.uiList[uiName] = getattr(sys.modules[uiType], uiType)() # getattr(eval(uiType), uiType)()
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
            
    #=======================================
    # widget specific functions
    #=======================================
    def ____TreeWidget_Process_Functions____():
        pass
    def path_pattern_to_task(self, path_pattern):
        # break config text into section of sub-directory search task
        # each task: 'sub_directory_path_to/content_list', 'content_dir_variable_name'
        # also, 'content_dir_variable_name' also is the key to its filter pattern
        # example: [('/VFX/assets/models', 'category'), ('', 'asset'), ('/Mesh/publish', 'model_file')])
        part_list = path_pattern.split('/')
        task_config = []
        task_pattern = re.compile('{.+}') # grab variable name in path_pattern with {variable} format
        sub = ''
        for each in part_list:
            if task_pattern.match(each):
                task_config.append( (sub,each[1:-1]) )
                sub = ''
            else:
                sub=sub+'/'+each
        return task_config
    
    def getPathChild(self, scanPath, pattern='', isfile=0):
        resultList =[]
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
    def path_info(self, scanPath, file_pattern='', folder_pattern='', file=0, folder=0):
        # alternative method of getPathChild
        file_list = []
        folder_list = []
        # prepare filter
        cur_file_pattern = None
        if file_pattern != '':
            cur_file_pattern = file_pattern # re object
            if isinstance(file_pattern, (unicode,str)):
                cur_file_pattern = re.compile(file_pattern)
        cur_folder_pattern = None
        if folder_pattern != '':
            cur_folder_pattern = folder_pattern # re object
            if isinstance(folder_pattern, (unicode,str)):
                cur_folder_pattern = re.compile(folder_pattern)
        # category file and folder
        for x in os.listdir(scanPath):
            if os.path.isdir(os.path.join(scanPath,x)):
                folder_list.append(x)
            elif os.path.isfile(os.path.join(scanPath,x)):
                file_list.append(x)
        file_list.sort()
        folder_list.sort()
        # filter result
        result = []
        if file == 1:
            if cur_file_pattern is None:
                result.append(file_list)
            else:
                result.append( [x for x in file_list if cur_file_pattern.match(x)] )
        if folder == 1:
            if cur_folder_pattern is None:
                result.append(folder_list)
            else:
                result.append( [x for x in folder_list if cur_folder_pattern.match(x)] )
        if len(result) == 1:
            result = result[0]
        return result
    def DirToData(self, scanPath, task_config, pattern_config, currentTag=''):
        '''
            [ 
                node_info
                node_child
            ]
        '''
        if not isinstance(task_config, (tuple, list)):
            return ( [], [] )
        else:
            if len(task_config)== 0:
                return ( [], [] )
        task_list = task_config
        # 1. get path if at least 1 task
        cur_task = task_list[0]
        rest_task = [] if len(task_list)==1 else task_list[1:]
        scanPath = scanPath.replace('\\','/')
        if cur_task[0] != '':
            scanPath = scanPath+cur_task[0] # note join path with /startswith/ will goto top path
        if not os.path.isdir(scanPath):
            print('Error: path not exists: {}'.format(scanPath))
            return ( [], [] )
        # 2. get list and filter list
        cur_pattern = '' if cur_task[1] not in pattern_config.keys() else pattern_config[cur_task[1]]
        isfile = 0 # folder only
        if cur_task[1].endswith('_file'):
            isfile = 1 # file only
        if cur_task[1].endswith('_all'):
            isfile = 2 # folder and file
        node_name = os.path.basename(scanPath)
        node_info = ['', '', scanPath ] if currentTag == '' else [node_name, currentTag, scanPath ]
        node_info_child = []
        parentTag = currentTag
        for each_name in self.getPathChild(scanPath, cur_pattern, isfile):
            cur_path = os.path.join(scanPath, each_name).replace('\\','/')
            cur_tag = each_name if parentTag == '' else parentTag+':'+each_name
            if os.path.isdir(cur_path):
                if len(rest_task) > 0:
                    # go next level task
                    node_info_child.append( self.DirToData(cur_path, rest_task, pattern_config, cur_tag) )
                else:
                    node_info_child.append( ( [os.path.basename(cur_path), cur_tag, cur_path ], [] ) )
            else:
                node_info_child.append( ( [os.path.basename(cur_path), '', cur_path ], [] ) )
        return (node_info, node_info_child)
        
    def DirToTree(self, cur_tree, parentNode, scanPath, task_config, pattern_config):
        if not isinstance(task_config, (tuple, list)):
            return
        else:
            if len(task_config)== 0:
                return
        task_list = task_config
        # 1. get path if at least 1 task
        cur_task = task_list[0]
        rest_task = [] if len(task_list)==1 else task_list[1:]
        scanPath = scanPath.replace('\\','/')
        if cur_task[0] != '':
            # because join path with /startswith/ will goto top path
            scanPath = scanPath+cur_task[0] 
        if not os.path.isdir(scanPath):
            print('Error: path not exists: {}'.format(scanPath))
            return
        # 2. get list and filter list
        cur_pattern = '' if cur_task[1] not in pattern_config.keys() else pattern_config[cur_task[1]]
        isfile = 0 # folder only
        if cur_task[1].endswith('_file'):
            isfile = 1 # file only
        if cur_task[1].endswith('_all'):
            isfile = 2 # folder and file
        child_list = self.getPathChild(scanPath, cur_pattern, isfile)
        node_list = {}
        # 3. create node in normal style
        parentNode_info = unicode(parentNode.text(1))
        
        if isfile == 2:
            group_dict = {}
            for each_name in child_list:
                if os.path.isdir(os.path.join(scanPath, each_name)):
                    new_node = QtWidgets.QTreeWidgetItem()
                    new_node.setText(0, each_name)
                    new_node.setText(2, os.path.join(scanPath,each_name).replace('\\','/') )
                    parentNode.addChild(new_node)
                    node_list[each_name]=new_node
                else:
                    prefix, ext = os.path.splitext(each_name)
                    # file type
                    fileType = ext[1:]
                    # file version
                    version_txt = ""
                    possible_version_list = re.findall(r'_v([\d]+)[_\.]', each_name) # last _v999.ext or _v999_xxx.ext
                    if len(possible_version_list) > 0:
                        version_txt = possible_version_list[-1]
                    # file prefix
                    if version_txt != "":
                        prefix = each_name.rsplit("_v"+version_txt, 1)[0]
                    # file group
                    group_name = prefix+':'+fileType
                    if group_name not in group_dict.keys():
                        group_dict[group_name] = []
                    group_dict[group_name].append(each_name)
            # add group node first
            for group_name in sorted(group_dict.keys()):
                group_dict[group_name].sort(reverse=1)
                group_item_list = group_dict[group_name]
                fileType = group_name.split(':')[1]
            
                group_node = QtWidgets.QTreeWidgetItem()
                group_node_top_name = group_item_list[0]
                cur_filePath = os.path.join(scanPath,group_node_top_name).replace("\\","/")
                
                group_node.setText(0, group_node_top_name)
                group_node.setText(1, fileType)
                group_node.setText(2, cur_filePath)
                
                parentNode.addChild(group_node)
               
                # add sub version to the tree
                if len(group_item_list) == 1:
                    node_list[group_node_top_name]=group_node
                if len(group_item_list) > 1:
                    for each_name in group_item_list:
                        sub_node = QtWidgets.QTreeWidgetItem()
                        cur_filePath = os.path.join(scanPath,each_name).replace("\\","/")
                       
                        sub_node.setText(0, each_name)
                        sub_node.setText(1, fileType)
                        sub_node.setText(2, cur_filePath)
                        
                        group_node.addChild(sub_node)
                        node_list[each_name]=sub_node
        elif isfile == 0:
            for each_name in child_list:
                new_node = QtWidgets.QTreeWidgetItem()
                new_node.setText(0, each_name)
                if parentNode_info == '':
                    new_node.setText(1, each_name)
                else:
                    new_node.setText(1, parentNode_info+':'+each_name)
                new_node.setText(2, os.path.join(scanPath,each_name).replace('\\','/') )
                parentNode.addChild(new_node)
                node_list[each_name]=new_node
        elif isfile == 1:
            # 3. create node in combine style
            #-- group similar
            group_dict = {}
            for each_name in child_list:
                prefix, ext = os.path.splitext(each_name)
                # file type
                fileType = ext[1:]
                # file version
                version_txt = ""
                possible_version_list = re.findall(r'_v([\d]+)[_\.]', each_name) # last _v999.ext or _v999_xxx.ext
                if len(possible_version_list) > 0:
                    version_txt = possible_version_list[-1]
                # file prefix
                if version_txt != "":
                    prefix = each_name.rsplit("_v"+version_txt, 1)[0]
                # file group
                group_name = prefix+':'+fileType
                if group_name not in group_dict.keys():
                    group_dict[group_name] = []
                group_dict[group_name].append(each_name)
            # add group node first
            for group_name in sorted(group_dict.keys()):
                group_dict[group_name].sort(reverse=1)
                group_item_list = group_dict[group_name]
                fileType = group_name.split(':')[1]
            
                group_node = QtWidgets.QTreeWidgetItem()
                group_node_top_name = group_item_list[0]
                cur_filePath = os.path.join(scanPath,group_node_top_name).replace("\\","/")
                
                group_node.setText(0, group_node_top_name)
                group_node.setText(1, fileType)
                group_node.setText(2, cur_filePath)
                
                parentNode.addChild(group_node)
               
                # add sub version to the tree
                if len(group_item_list) == 1:
                    node_list[group_node_top_name]=group_node
                if len(group_item_list) > 1:
                    for each_name in group_item_list:
                        sub_node = QtWidgets.QTreeWidgetItem()
                        cur_filePath = os.path.join(scanPath,each_name).replace("\\","/")
                       
                        sub_node.setText(0, each_name)
                        sub_node.setText(1, fileType)
                        sub_node.setText(2, cur_filePath)
                        
                        group_node.addChild(sub_node)
                        node_list[each_name]=sub_node
        
        # go next level task
        if len(rest_task) > 0:
            for each_name in child_list:
                cur_parentPath = os.path.join(scanPath, each_name).replace('\\', '/')
                if os.path.isdir(cur_parentPath):
                    self.DirToTree(cur_tree, node_list[each_name], cur_parentPath, rest_task, pattern_config)
    def TreeToData(self, tree, cur_node):
        # now take widghet col count instead tree column count with hidden ones
        child_count = cur_node.childCount()
        node_info = [ unicode( cur_node.text(i) ) for i in range(cur_node.columnCount()) ]
        node_info_child = []
        for i in range(child_count):
            node_info_child.append( self.TreeToData(tree, cur_node.child(i) ) )
        return (node_info, node_info_child)
    def DataToTree(self, tree, cur_node, data, filter='', col=0):
        node_info = data[0]
        node_info_child = data[1]
        [cur_node.setText(i, node_info[i]) for i in range(len(node_info))]
        # re filter
        if filter != '' and isinstance(filter, (str, unicode)):
            filter = re.compile(filter, re.IGNORECASE)
        for sub_data in node_info_child:
            if filter == '':
                new_node = QtWidgets.QTreeWidgetItem()
                cur_node.addChild(new_node)
                self.DataToTree(tree, new_node, sub_data)
            else:
                if not filter.search(sub_data[0][col]) and not self.DataChildCheck(sub_data[1], filter, col):
                    pass
                else:
                    new_node = QtWidgets.QTreeWidgetItem()
                    cur_node.addChild(new_node)
                    new_node.setExpanded(1)
                    self.DataToTree(tree, new_node, sub_data, filter, col)
    def DataChildCheck(self, DataChild, filter, col):
        ok_cnt = 0
        if isinstance(filter, (str, unicode)):
            filter = re.compile(filter, re.IGNORECASE)
        for sub_data in DataChild:
            if filter.search(sub_data[0][col]) or self.DataChildCheck(sub_data[1], filter, col):
                ok_cnt +=1
        return ok_cnt
    def TreeExport(self, tree_name, file):
        # export process
        ui_data = self.TreeToData(self.uiList[tree_name], self.uiList[tree_name].invisibleRootItem())
        # file process
        if file.endswith('.dat'):
            self.writeDataFile(ui_data, file, binary=1)
        else:
            self.writeDataFile(ui_data, file)
        self.quickInfo("File: '"+file+"' creation finished.")
    def TreeImport(self, tree_name, file):
        # import process
        ui_data = ""
        if file.endswith('.dat'):
            ui_data = self.readDataFile(file, binary=1)
        else:
            ui_data = self.readDataFile(file)
        self.uiList['dir_tree'].clear()
        self.DataToTree(self.uiList['dir_tree'], self.uiList['dir_tree'].invisibleRootItem(), ui_data)
        self.quickInfo("File: '"+file+"' loading finished.")
    def cache_tree(self, cur_tree_name, force=1):
        cur_tree = self.uiList[cur_tree_name]
        if 'cache' not in self.memoData:
            self.memoData['cache'] = {}
        if force == 1:
            self.memoData['cache'][cur_tree_name] = self.TreeToData(cur_tree, cur_tree.invisibleRootItem())
        else:
            if cur_tree_name not in self.memoData['cache']:
                self.memoData['cache'][cur_tree_name] = self.TreeToData(cur_tree, cur_tree.invisibleRootItem())
    def filter_tree(self, cur_tree_name, word):
        self.filter_tree_col(cur_tree_name, 0, word)
    def filter_tree_col(self, cur_tree_name, col, word):
        word = unicode(word)
        cur_tree = self.uiList[cur_tree_name]
        parentNode = cur_tree.invisibleRootItem()
        # read cache, if no cache, create cache
        self.cache_tree(cur_tree_name, force = 0)
        # filter and show, reset back to cache
        cur_tree.clear()
        if word != '':
            self.DataToTree(cur_tree, parentNode, self.memoData['cache'][cur_tree_name], filter=word, col=col)
        else:
            self.DataToTree(cur_tree, parentNode, self.memoData['cache'][cur_tree_name])
#############################################
# User Class creation
#############################################
version = '0.1'
date = '2017.01.01'
log = '''
#------------------------------
# How to Use: 
# 1. global replace class name "UserClassUI"  to "YourToolName" in your editor,
#  - in icons folder, the Tool GUI icon should name as "YourToolName.png"
# 2. change file name "universal_tool_template.py" to "YourPythonFileName.py",
#  - in icons folder, the Maya shelf icon should name as "YourPythonFileName.png", if you name all name the same, then 1 icon is enough
# 3. load it up and run
#------------------------------
'''
help = '''
# loading template - Run in python panel
myPath='/path_to_universal_tool_or_custom_name/'
import sys;myPath in sys.path or sys.path.append(myPath);
import universal_tool_template
universal_tool_template.main()

# loading template - Run in system command console

python universal_tool_template.py
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
        self.qui_user_dict = {} # e.g: 'edit': 'LNTextEdit',
        
        self.setupStyle()
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
        super(self.__class__,self).setupMenu()
        
    def setupWin(self):
        super(self.__class__,self).setupWin()
        self.setGeometry(500, 300, 250, 110) # self.resize(250,250)
        
    def setupUI(self):
        super(self.__class__,self).setupUI('grid')
        #------------------------------
        # user ui creation part
        #------------------------------
        # + template: qui version since universal tool template v7
        #   - no extra variable name, all text based creation and reference
        
        self.qui('box_btn;Box | sphere_btn;Sphere | ring_btn;Ring', 'my_layout;grid', 'h')
        self.qui('box2_btn;Box2 | sphere2_btn;Sphere2 | ring2_btn;Ring2', 'my_layout', 'h')
        
        self.qui('cat_btn;Cat | dog_btn;Dog | pig_btn;Pig', 'pet_layout;grid', 'v')
        self.qui('cat2_btn;Cat2 | dog2_btn;Dog2 | pig2_btn;Pig2', 'pet_layout', 'v')
        
        self.qui('name_input@Name:;John | email_input@Email:;test@test.com', 'entry_form')
        
        self.qui('user2_btn;User2 | info2_btn;Info2', 'my_grp;vbox,Personal Data')
        
        self.qui('source_txt | process_btn;Process and Update', 'upper_vbox')
        self.qui('upper_vbox | result_txt', 'input_split;v')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('my_layout | my_table | input_split | entry_form | fileBtn_layout | pet_layout | my_grp', 'main_layout')
        
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
    # ---- user response list ----
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
        
        # load user data
        user_dirPath = os.path.join(os.path.expanduser('~'), 'Tool_Config', self.__class__.__name__)
        user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
        if os.path.isfile(user_setting_filePath):
            sizeInfo = self.readDataFile(user_setting_filePath)
            self.setGeometry(*sizeInfo)
    
    def closeEvent(self, event):
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
        geoInfo = self.geometry()
        sizeInfo = [geoInfo.x(), geoInfo.y(), geoInfo.width(), geoInfo.height()]
        user_setting_filePath = os.path.join(user_dirPath, 'setting.json')
        self.writeDataFile(sizeInfo, user_setting_filePath)
        
    def toggleTop_action(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.show()
    # - example button functions
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
    # template 1 - Keep only one copy of windows ui in Maya
    global single_UserClassUI
    if single_UserClassUI is None:
        if hostMode == 'maya':
            single_UserClassUI = UserClassUI(parentWin, mode)
        elif hostMode == 'nuke':
            single_UserClassUI = UserClassUI(QtWidgets.QApplication.activeWindow(), mode)
        else:
            single_UserClassUI = UserClassUI()
        # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_UserClassUI.show()
    ui = single_UserClassUI
    if hostMode != 'desktop':
        ui.activateWindow()
    # template 2 - allow loading multiple windows of same UI in Maya
    '''
    if hostMode == "maya":
        ui = UserClassUI(parentWin)
        ui.show()
    else:
        pass
    # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    '''
    
    # loop app object for certain host
    if hostMode in ('desktop'):
        sys.exit(app_UserClassUI.exec_())
    elif hostMode in ('npp','fusion'):
        app_UserClassUI.exec_()
    return ui

if __name__ == "__main__":
    main()
