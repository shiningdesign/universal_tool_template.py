from GearBox_template_1010 import *
#############################################
# User Class creation
#############################################
version = '1.1'
date = '2017.09.25'
log = '''
2017.09.25
  * update version with template 1010

'''
help = '''

'''

# --------------------
#  user module list
# --------------------


class GearBox(UniversalToolUI):
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
        self.quickMenu(['file_menu;&File', 'tree_menu;&Tree', 'setting_menu;&Setting','help_menu;&Help'])
        
        cur_menu = self.uiList['file_menu']
        self.quickMenuAction('fileLoad_atn','&Open Json Data File','Open Json Data File.','fileLoad.png', cur_menu)
        self.uiList['fileLoad_atn'].setShortcut(QtGui.QKeySequence("Ctrl+O"))
        self.quickMenuAction('fileExport_atn','&Save Json Data File','Save Json Data File.','fileExport.png', cur_menu)
        self.uiList['fileExport_atn'].setShortcut(QtGui.QKeySequence("Ctrl+S"))
        
        
        
        cur_menu = self.uiList['tree_menu']
        self.quickMenuAction('tree_newNode_atn','&Add new Node','Add New Node.','tree_newNode.png', cur_menu)
        self.uiList['tree_newNode_atn'].setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self.quickMenuAction('tree_removeNode_atn','&Remove selected Node','Remove Selected Node.','tree_removeNode.png', cur_menu)
        self.uiList['tree_removeNode_atn'].setShortcut(QtGui.QKeySequence("Ctrl+R"))
        self.quickMenuAction('tree_fontUp_atn','&Upsize Font of Tree','Upsize Font of Tree.','tree_fontUp.png', cur_menu)
        self.uiList['tree_fontUp_atn'].setShortcut(QtGui.QKeySequence("Ctrl+="))
        self.quickMenuAction('tree_fontDown_atn','&Downsize Font of Tree','Down Font of Tree.','tree_fontDown.png', cur_menu)
        self.uiList['tree_fontDown_atn'].setShortcut(QtGui.QKeySequence("Ctrl+-"))
        self.quickMenuAction('tree_fontNormal_atn','&Normal Font of Tree','Down Font of Tree.','tree_fontNormal.png', cur_menu)
        self.uiList['tree_fontNormal_atn'].setShortcut(QtGui.QKeySequence("Ctrl+0"))
        
        self.quickMenuAction('tree_sort_atn','Tree &Sort','Sort the Tree.','tree_sort.png', cur_menu)
        self.uiList['tree_sort_atn'].setShortcut(QtGui.QKeySequence("Ctrl+Shift+S"))
        
        cur_menu = self.uiList['setting_menu']
        self.quickMenuAction('toggleDragMode_atn','&Enable Drag Mode','Enable Drag Mode.','', cur_menu)
        self.uiList['toggleDragMode_atn'].setShortcut(QtGui.QKeySequence("Ctrl+E"))
        self.uiList['toggleDragMode_atn'].setCheckable(1)
        self.uiList['toggleDragMode_atn'].setChecked(0)
        cur_menu.addSeparator()
        super(self.__class__,self).setupMenu()
        
    def setupWin(self):
        super(self.__class__,self).setupWin()
        self.setGeometry(500, 300, 250, 110) # self.resize(250,250)
        
    def setupUI(self):
        super(self.__class__,self).setupUI('grid')
        #------------------------------
        # user ui creation part
        #------------------------------
        self.qui('source_txt | target_txt', 'write_layout;hbox')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('config_tree;(name,value,type) | write_layout', 'translate_split;v')
        self.qui('translate_split | fileBtn_layout', 'main_layout')
        
        self.uiList['config_tree'].setColumnWidth(0,180)
        #self.uiList['config_tree'].setColumnHidden(2,1)
        self.uiList['config_tree'].setDragEnabled(0)
        self.uiList['config_tree'].setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.memoData['tree_font_size'] = 10
        self.uiList['config_tree'].setStyleSheet("QTreeWidget { font-size: %dpt;}" % self.memoData['tree_font_size'])
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
        self.uiList['config_tree'].itemClicked[QtWidgets.QTreeWidgetItem,int].connect(self.config_tree_select_action)
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
        
   
    def config_tree_select_action(self):
        currentNode = self.uiList['config_tree'].currentItem()
        if currentNode:
            self.uiList['source_txt'].setText(currentNode.text(1))
    def tree_sort_action(self):
        self.uiList['config_tree'].sortByColumn(0, QtCore.Qt.AscendingOrder)
    def tree_fontNormal_action(self):
        self.memoData['tree_font_size'] = 10
        self.uiList['config_tree'].setStyleSheet("QTreeWidget { font-size: %dpt;}" % self.memoData['tree_font_size'])
    def tree_fontUp_action(self):
        self.memoData['tree_font_size'] += 2
        self.uiList['config_tree'].setStyleSheet("QTreeWidget { font-size: %dpt;}" % self.memoData['tree_font_size'])
    def tree_fontDown_action(self):
        if self.memoData['tree_font_size'] >= 10:
            self.memoData['tree_font_size'] -= 2
            self.uiList['config_tree'].setStyleSheet("QTreeWidget { font-size: %dpt;}" % self.memoData['tree_font_size'])
    def tree_newNode_action(self):
        cur_tree = self.uiList['config_tree']
        node_name,ok = self.quickMsgAsk('New Setting Name')
        if ok and node_name != '':
            self.quickTree(cur_tree, [node_name, ''], 1) # all editable
    def tree_removeNode_action(self):
        self.quickTreeRemove(self.uiList['config_tree'])
    def toggleDragMode_action(self):
        self.uiList['config_tree'].setDragEnabled(self.uiList['toggleDragMode_atn'].isChecked())
        if self.uiList['toggleDragMode_atn'].isChecked():
            self.uiList['config_tree'].setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        else:
            self.uiList['config_tree'].setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
    def quickTree(self, cur_tree, node_data, editable=0):
        # not per-column control on editable
        if not isinstance(node_data, (list, tuple)):
            node_data = [node_data]
        # 1. get current selection
        selected_node = cur_tree.selectedItems()
        if len(selected_node) > 0:
            selected_node = selected_node[0]
        else:
            selected_node = cur_tree.invisibleRootItem()
        # 2. create a new node
        new_node = QtWidgets.QTreeWidgetItem()
        for i,name in enumerate(node_data):
            new_node.setText(i, name)
        if editable == 1:
            new_node.setFlags(new_node.flags()|QtCore.Qt.ItemIsEditable)
        # 3. add it
        selected_node.addChild(new_node)
        # 4. expand it
        selected_node.setExpanded(1)
    def quickTreeRemove(self, cur_tree):
        root = cur_tree.invisibleRootItem()
        for item in cur_tree.selectedItems():
            (item.parent() or root).removeChild(item)
    def quickTreeInfo(self, cur_tree):
        data = []
        root = cur_tree.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            cur_node = root.child(i)
            cur_info = []
            for j in range( cur_node.columnCount() ):
                cur_info.append( unicode(cur_node.text(j)) )
            data.append(cur_info)
        return data
    def quickTreeUpdate(self, cur_tree, data):
        cur_tree.clear()
        root = cur_tree.invisibleRootItem()
        if isinstance(data, dict):
            data = [ (k,v) for k,v in data.items() ]
        else:
            if not isinstance(data, (tuple, list) ):
                return
        data_len = len(data)
        for i in range(data_len):
            self.quickTree(cur_tree, data[i], 1)
        
    def DataToTree(self, tree, parent, data):
        if isinstance(data, dict):
            for each_key in data.keys():
                new_node = QtWidgets.QTreeWidgetItem()
                new_node.setFlags(new_node.flags()|QtCore.Qt.ItemIsEditable)
                parent.addChild(new_node)
                new_node.setText(0, each_key)
                self.DataToTree(tree, new_node, data[each_key])
        else:
            if parent is tree.invisibleRootItem():
                new_node = QtWidgets.QTreeWidgetItem()
                new_node.setFlags(new_node.flags()|QtCore.Qt.ItemIsEditable)
                parent.addChild(new_node)
                parent = new_node
                parent.setText(0, '')
            # write data to tree
            if isinstance( data, (str, unicode)):
                parent.setText(1, data)
                parent.setText(2, 'text')
            else:
                parent.setText(1, json.dumps(data))
                parent.setText(2, 'data')
    def TreeToData(self, tree, parent):
        child_count = parent.childCount()
        if child_count == 0:
            if unicode( parent.text(2) ) == 'text':
                return unicode( parent.text(1) )
            else:
                return json.loads( unicode(parent.text(1)) )
        elif child_count == 1:
            # can be dict or _main_ with only 1 info
            if unicode(parent.child(0).text(0)) == '' and parent is tree.invisibleRootItem():
                if unicode( parent.child(0).text(2) ) == 'text':
                    return unicode(parent.child(0).text(1))
                else:
                    return json.loads( unicode(parent.child(0).text(1)) )
            else:
                # general case
                data = {}
                for i in range(child_count):
                    cur_node = parent.child(i)
                    data[ unicode(cur_node.text(0)) ] = self.TreeToData(tree, cur_node)
                return data
        else:
            data = {}
            for i in range(child_count):
                cur_node = parent.child(i)
                data[ unicode(cur_node.text(0)) ] = self.TreeToData(tree, cur_node)
            return data
        
    # - example file io function
    def fileExport_action(self):
        filePath_input = self.uiList['filePath_input']
        file = unicode(filePath_input.text())
        if file == "":
            file= self.quickFileAsk('export')
        if file == "":
            return
        # update ui
        filePath_input.setText(file)
        # export process
        ui_data = self.TreeToData(self.uiList['config_tree'], self.uiList['config_tree'].invisibleRootItem())
        # file process
        if file.endswith('.dat'):
            self.writeDataFile(ui_data, file, binary=1)
        else:
            self.writeDataFile(ui_data, file)
        self.quickInfo("File: '"+file+"' creation finished.")
    
    def fileLoad_action(self):
        filePath_input = self.uiList['filePath_input']
        file=unicode(filePath_input.text())
        if file == "":
            file= self.quickFileAsk('import')
        if file == "":
            return
        # update ui
        filePath_input.setText(file)
        # import process
        ui_data = []
        if file.endswith('.dat'):
            ui_data = self.readDataFile(file, binary=1)
        else:
            ui_data = self.readDataFile(file)
        self.uiList['config_tree'].clear()
        self.DataToTree(self.uiList['config_tree'], self.uiList['config_tree'].invisibleRootItem(), ui_data)
        #self.quickTreeUpdate(self.uiList['config_tree'], ui_data)
        self.quickInfo("File: '"+file+"' loading finished.")
    

#############################################
# window instance creation
#############################################

single_GearBox = None
def main(mode=0):
    # get parent window in Maya
    parentWin = None
    if hostMode == "maya":
        if qtMode in (0,2): # pyside
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        elif qtMode in (1,3): # PyQt
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
    # create app object for certain host
    app = None
    if hostMode in ("desktop", "blender"):
        # single instance app mode on windows
        if osMode == 'win':
            # check if already open for single desktop instance
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetClassName = ctypes.windll.user32.GetClassNameA
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            IsWindowVisible = ctypes.windll.user32.IsWindowVisible
            SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
            titles = []
            def foreach_window(hwnd, lParam):
                if IsWindowVisible(hwnd):
                    length = GetWindowTextLength(hwnd)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    class_name = ctypes.create_string_buffer(200)
                    GetClassName(hwnd, ctypes.byref(class_name), 200)
                    titles.append( (buff.value, class_name.value, hwnd) )
                return True
            EnumWindows(EnumWindowsProc(foreach_window), 0)
            winTitle = 'GearBox'
            #winTitle = os.path.basename(os.path.dirname(__file__))
            is_opened = 0
            for x in titles:
                if re.match(winTitle+' - v[0-9.]* - host: desktop',x[0]) and x[1] == 'QWidget':
                    is_opened += 1
                    if is_opened == 1:
                        ctypes.windll.user32.SetForegroundWindow(x[2])
                        return
        app = QtWidgets.QApplication(sys.argv)
    
    #--------------------------
    # ui instance
    #--------------------------
    # template 1 - Keep only one copy of windows ui in Maya
    global single_GearBox
    if single_GearBox is None:
        if hostMode == "maya":
            single_GearBox = GearBox(parentWin, mode)
        elif hostMode == "nuke":
            single_GearBox = GearBox(QtWidgets.QApplication.activeWindow(), mode)
        else:
            single_GearBox = GearBox()
        # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_GearBox.show()
    ui = single_GearBox
    
    # template 2 - allow loading multiple windows of same UI in Maya
    '''
    if hostMode == "maya":
        ui = GearBox(parentWin)
        ui.show()
    else:
        pass
    # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    '''
    
    # loop app object for certain host
    if hostMode in ("desktop"):
        sys.exit(app.exec_())
    
    return ui

if __name__ == "__main__":
    main()

if hostMode == "blender":
    app = QtWidgets.QApplication(sys.argv)
    ui = GearBox()
    ui.show()
