'''
template version: utt.Class_1010_20200615
ClassName:
  * description
  
v0.1:
  * base functions

'''
# ---- base lib 2020.02.13----
import os,sys
# ---- pyMode 2020.02.13----
# python 2,3 support unicode function
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    # unicode = lambda s: str(s) # this works for function but not for class check
    unicode = str
if sys.version_info[:3][0]>=3:
    import importlib
    reload = importlib.reload # add reload

pyMode = '.'.join([ str(n) for n in sys.version_info[:3] ])
print("Python: {0}".format(pyMode))
# ---- qtMode 2020.02.13 ----
qtMode = 0 # 0: PySide; 1 : PyQt, 2: PySide2, 3: PyQt5
qtModeList = ('PySide', 'PyQt4', 'PySide2', 'PyQt5')
try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    qtMode = 0
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        qtMode = 2
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
# ---- user lib ----

class ClassName(QtWidgets.QWidget):
    def __init__(self, parent=None,mode=0):
        QtWidgets.QWidget.__init__(self,parent)
        # memo
        self.parent=parent
        
        self.memoData={}
        self.memoData['last_import']=''
        self.memoData['last_export']=''
        self.memoData['last_browse']=''
        # UI
        self.uiList={}
        self.uiList['main_layout']=QtWidgets.QHBoxLayout();
        self.uiList['main_layout'].setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.uiList['main_layout'])
        
        self.qui('main_label;Example | main_input', 'main_layout')
        self.qui_policy('main_input',5,3)
        
        # hide ui
        
        # connect UI
        self.Establish_Connections()
    def Establish_Connections(self):
        for ui_name in self.uiList.keys():
            prefix = ui_name.rsplit('_', 1)[0]
            if ui_name.endswith('_btn'):
                if hasattr(self, prefix+"_action"):
                    self.uiList[ui_name].clicked.connect(getattr(self, prefix+"_action"))
        # drop support
        self.uiList['main_input'].installEventFilter(self)
    
    def eventFilter(self, object, event):
        # the main window event filter function
        if event.type() == QtCore.QEvent.DragEnter:
            data = event.mimeData()
            urls = data.urls()
            if object is self.uiList['main_input'] and (urls and urls[0].scheme() == 'file'):
                event.acceptProposedAction()
            return 1
        elif event.type() == QtCore.QEvent.Drop:
            data = event.mimeData()
            urls = data.urls()
            if object is self.uiList['main_input'] and (urls and urls[0].scheme() == 'file'):
                filePath = unicode(urls[0].path())[1:]
                self.uiList['main_input'].setText(os.path.normpath(filePath))
                
            return 1
        return 0
        
    # ---- user functions ----
    
    # ---- core functions ----
    def ___core_functions___(self):
        pass
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
    def default_menu_call(self, ui_name, point):
        if ui_name in self.uiList.keys() and ui_name+'_menu' in self.uiList.keys():
            self.uiList[ui_name+'_menu'].exec_(self.uiList[ui_name].mapToGlobal(point))
    def qui(self, ui_str, layout_str):
        ui_str_list = [x.strip() for x in ui_str.split('|') if x.strip()]
        ui_list = []
        for ui in ui_str_list:
            ui_option = ''
            if ';' in ui:
                ui,ui_option = ui.split(';',1)
            if ui not in self.uiList.keys():
                # creation process
                if ui.endswith('_choice'):
                    self.uiList[ui]= QtWidgets.QComboBox()
                elif ui.endswith('_input'):
                    self.uiList[ui]= QtWidgets.QLineEdit()
                elif ui.endswith('_txt'):
                    self.uiList[ui]= QtWidgets.QTextEdit()
                elif ui.endswith('_label'):
                    self.uiList[ui]= QtWidgets.QLabel(ui_option)
                elif ui.endswith('_btn'):
                    self.uiList[ui]= QtWidgets.QPushButton(ui_option)
                elif ui.endswith('_check'):
                    self.uiList[ui]= QtWidgets.QCheckBox(ui_option)
                elif ui.endswith('_spin'):
                    self.uiList[ui]= QtWidgets.QSpinBox()
                    if len(ui_option)>0:
                        int_list = ui_option.replace('(','').replace(')','').split(',')
                        self.uiList[ui].setMaximum(10000) # override default 99
                        if len(int_list)>0 and int_list[0].isdigit():
                            self.uiList[ui].setValue(int(int_list[0]))
                        if len(int_list)>1 and int_list[1].isdigit():
                            self.uiList[ui].setMinimum(int(int_list[1]))
                        if len(int_list)>2 and int_list[2].isdigit():
                            self.uiList[ui].setMaximum(int(int_list[2]))
                elif ui.endswith('_tree'):
                    self.uiList[ui] = QtWidgets.QTreeWidget()
                    if len(ui_option)>0:
                        label_list = ui_option.replace('(','').replace(')','').split(',')
                        self.uiList[ui].setHeaderLabels(label_list)
                elif ui.endswith('_space'):
                    self.uiList[ui] = QtWidgets.QSpacerItem(5,5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred )
                else:
                    # creation fail
                    continue
            # collect existing ui and created ui
            ui_list.append(ui)
        layout_option = ''
        if ';' in layout_str:
            layout_str, layout_option = layout_str.split(';',1)
        if layout_str not in self.uiList.keys():
            # try create layout
            if layout_str.endswith('_grp'):
                # grp option
                grp_option = layout_option.split(';',1)
                grp_title = layout_str
                if len(grp_option)>0:
                    if grp_option[0]=='vbox':
                        self.uiList[layout_str+'_layout'] = QtWidgets.QVBoxLayout()
                    elif grp_option[0]=='hbox':
                        self.uiList[layout_str+'_layout'] = QtWidgets.QHBoxLayout()
                if len(grp_option) == 2:
                    grp_title = grp_option[1]
                self.uiList[layout_str] = QtWidgets.QGroupBox(grp_title)
                self.uiList[layout_str].setLayout(self.uiList[layout_str+'_layout'])
                # pass grp layout
                layout_str = layout_str+'_layout'
            else:
                if layout_option == 'vbox':
                    self.uiList[layout_str] = QtWidgets.QVBoxLayout()
                elif layout_option == 'hbox':
                    self.uiList[layout_str] = QtWidgets.QHBoxLayout()
                else:
                    return
        cur_layout = self.uiList[layout_str]
        if not isinstance(cur_layout, QtWidgets.QBoxLayout):
            return
        for ui in ui_list:
            ui_option = ''
            if ';' in ui:
                ui,ui_option = ui.split(';',1)
            if isinstance(self.uiList[ui], QtWidgets.QWidget):
                cur_layout.addWidget(self.uiList[ui])
            elif isinstance(self.uiList[ui], QtWidgets.QSpacerItem):
                cur_layout.addItem(self.uiList[ui])
            elif isinstance(self.uiList[ui], QtWidgets.QLayout):
                cur_layout.addLayout(self.uiList[ui])
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
    def quickInfo(self, info, force=0):
        if hasattr( self.window(), "quickInfo") and force == 0:
            self.window().statusBar().showMessage(info)
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
class TestWin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_win = ClassName()
    main_win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

