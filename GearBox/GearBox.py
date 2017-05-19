from GearBox_template_0903 import *
#############################################
# User Class creation
#############################################
'''
v001. 2017.04.17
  * import and export with json dumps loads text format
'''
# --------------------
#  user module list
# --------------------


class GearBox(UniversalToolUI):
    def __init__(self, parent=None, mode=0):
        UniversalToolUI.__init__(self, parent)
        
        # class variables
        self.version="0.1"
        self.help = "(GearBox)How to Use:\n1. Put source info in\n2. Click Process button\n3. Check result output\n4. Save memory info into a file."
        
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
        self.loadData()
        self.loadLang()
        
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
        self.setGeometry(500, 300, 500, 600) # self.resize(250,250)
        
    def setupUI(self):
        super(self.__class__,self).setupUI('grid')
        #------------------------------
        # user ui creation part
        #------------------------------
        # + template: qui version since universal tool template v7
        #   - no extra variable name, all text based creation and reference
        self.qui('source_txt | target_txt', 'write_layout;hbox')
        self.qui('filePath_input | fileLoad_btn;Load | fileExport_btn;Export', 'fileBtn_layout;hbox')
        self.qui('config_tree;(name,value,type) | write_layout', 'translate_split;v')
        self.qui('translate_split | fileBtn_layout', 'main_layout')
        
        self.uiList['config_tree'].setColumnWidth(0,180)
        #self.uiList['config_tree'].setColumnHidden(2,1)
        self.uiList['config_tree'].setDragEnabled(0)
        #self.uiList['config_tree'].setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.memoData['tree_font_size'] = 10
        self.uiList['config_tree'].setStyleSheet("QTreeWidget { font-size: %dpt;}" % self.memoData['tree_font_size'])
        
        #------------- end ui creation --------------------
        keep_margin_layout = ['main_layout']
        for name, each in self.uiList.items():
            if isinstance(each, QtWidgets.QLayout) and name not in keep_margin_layout and not name.endswith('_grp_layout'):
                each.setContentsMargins(0, 0, 0, 0)
        self.quickInfo('Ready')
        # self.statusBar().hide()
        
    def Establish_Connections(self):
        super(self.__class__,self).Establish_Connections()
        # custom ui response
        self.uiList['config_tree'].itemClicked[QtWidgets.QTreeWidgetItem,int].connect(self.config_tree_select_action)
    # ---- user response list ----
    def loadData(self):
        print("Load data")
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
            self.writeFileData(ui_data, file, binary=1)
        else:
            self.writeFileData(ui_data, file)
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
            ui_data = self.readFileData(file, binary=1)
        else:
            ui_data = self.readFileData(file)
        self.uiList['config_tree'].clear()
        self.DataToTree(self.uiList['config_tree'], self.uiList['config_tree'].invisibleRootItem(), ui_data)
        #self.quickTreeUpdate(self.uiList['config_tree'], ui_data)
        self.quickInfo("File: '"+file+"' loading finished.")
        

#############################################
# window instance creation
#############################################

single_UserClassUI = None
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
        app = QtWidgets.QApplication(sys.argv)
    
    #--------------------------
    # ui instance
    #--------------------------
    # template 1 - Keep only one copy of windows ui in Maya
    global single_UserClassUI
    if single_UserClassUI is None:
        if hostMode == "maya":
            single_UserClassUI = GearBox(parentWin, mode)
        elif hostMode == "nuke":
            single_UserClassUI = GearBox(QtWidgets.QApplication.activeWindow(), mode)
        else:
            single_UserClassUI = GearBox()
        # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    single_UserClassUI.show()
    ui = single_UserClassUI
    
    # template 2 - allow loading multiple windows of same UI in Maya
    '''
    if hostMode == "maya":
        ui = GearBox(parentWin)
        ui.show()
    else:
        
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
