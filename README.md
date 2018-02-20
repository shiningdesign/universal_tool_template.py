universal_tool_template.py
===================

A quick Qt GUI tool development template for Maya, Houdini, Nuke, (BlackMagic) Fusion, Blender, Notepad++, Desktop;

It automatically supports any combination of (Python 2.x, Python 3.x in 32bit and 64bit) with (PySide, PyQt4, PySide2, PyQt5)

Detail Documentation at wiki: https://github.com/shiningdesign/universal_tool_template.py/wiki

Key Feature
-------------


| Feature | Description |
| :------------- |:-------------|
| **Host Detection** | Maya, Houdini, Nuke, Fusion, Blender, Notepad++, Desktop |
| **Python Detection** | 2.x, 3.x, 32bit, 64bit |
| **Qt Binding Detection** | PySide, PyQt4, PySide2, PyQt5 |
| **Universal Coding** | seamlessly works in above 2x2x4=16 combinations |
| **File IO Support** | json, cPicle binary, plain text |
| **oneline multi-UI creation** | quickUI() v4.0; qui() v1.0 |
| **one-stop UI management** | self.uiList, self.iconList, self.hotkey |
| **auto UI-Action bindinig** | button, menuItem, message button |
| **auto Icon loading** | maya shelf icon, class name icon |
| **Template Style Option** | standalone, frameless, trans-irregular, on-top |
| **Global Style Option** | modern style |
| **Interface Interaction** | Drag, Move, right-click-menu |
| **Element Style Option** | invisible-functional button |
| **Extension Features** | self location for script mode and app mode |
| **Language Features** | auto Export and Load UI language json |


Change Log
-------------
* v010.20:
  * (2018.02.20) Fix launch code in Houdini since v8
  * (2017.11.13) Blackmagic Fusion support added
  * (2017.11.13) notepad++ support for integration
    * blender3D support fix and code cleanup
    * python 3 add reload and unicode
    * quickFileAsk(self, type, ext=None, dir=None) for location preset 
  * (2017.10.26) some new functions
    * newFolder(parentPath, name=None)
    * qui_key(key_name, key_combo, func)
    * cache_tree(cur_tree_name, force=1)
    * filter_tree(cur_tree_name, word)
    * bring to front if called again in tool mode
  * (2017.10.17) a cleanup and restructure of template v10, especially those ui creation functions
* v010.10: 
  * (2017.10.12) update qui_menu() to support append to menu if exists and existing atn check
  * (2017.10.11) add return parent ui_name in qui(), which enabled nested qui creation
  * (2017.10.02) improve coding and more functions to handle context menu and multi-purpose in single function
  * (2017.09.20) add memoData of last_export and last_import for quickFileAsk to remember last directory
  * (2017.08.22) fix quickUI 3rd party class name generation
* v010.10: 2017.06.24
  * update file name up to 1010
  * add TreeWidget related operation inside (which not include in filename 1000)
  * operations include Interchange among File Directory, Raw Data, Tree Structure with optional filtering and file version combining
  * add openFile(filePath) to use system to open file (crossplatform)
* v010.10: 2017.05.17
  * add openFolder() and subprocess in template
  * add (optional) position memory
  * UserClassUI (optional) external config overload, and config export, import
* v010.10: 2017.04.28
  * add key of lang always upper()
  * add global font size function
  * switch loadLang and loadData
  * better file filter browser
* v010.11: 2017.04.25
  * added date tracking for version
  * added toggle Top flag in userClass
* v010.10: 2017.04.19
  * fix default_message, Establish_Connections function's prefix
  * better log, help, version placement
  * fix loadLang QCombo part
  * fix readDataFile part
  * better self location even with importing
* v010: 2017.03.13:
  * (2017.04.20) replacing v9.4, with strong "template+userClass" concept
  * rewrite some syntax, and provide more seperation on customization part
  * all sample code has been taken out for clean template
  * complete rewrite to v9 and more slim code
* v009.4: 2017.04.20
  * single desktop instance
* v009.3: 2017.02.20
  * auto template builder compatiblility
* v009: 2017.02.01
  * a branch of v8.2 beta - ongoing, as it will use class inherient method
  * instead of modify whole copy of the template class, which helps on nested template class UI and multiple class program
  * just change the UserClassUI to your class name
* v008.3: 2017.02.20
  * auto template builder compatiblility
* v008.2.2: 2017.02.14
  * fix language update
  * add icon related path
* v008.2: 2017.01.25
  * change default template_class name to UniversalToolUI_####, so that you can have multiple template testing without duplicate class name in memory
  * reduce code, 
     - add self.icon
     - add keep_margin_layout list
     - take out help into self.help for quick change
     - rewrite data file io functions, support json ascii data and cpickle binary data
     - better quickMsgAsk dialog functions
     - qui: add QListWidget
     - quickUI: add header name list option for QTreeWidget
  * better support for template as widget in nested UI, menu creation check for widget
  * remove all custom widget from template for clean start, you can add them later, like LNTextEdit
* v008: 2016.12.08:
  * (2016.12.19): v008.1 more cleanup
  * add python 3 support
  * compatible with Maya 2014 (pyside), Maya 2017 (pyside2), nuke 10 (pyside), houdini 15 (pyside), blender 2.7.8(pyqt5), desktop (pyqt4)
  * clean up code
* v007.4: 2016.11.15
  * disable drag move by default
  * add auto text input valid and input related get function
  * add more custom option for default_action() for buttons
* v007.3: 2016.10.13
  * add functions for convert between Maya built-in UI creation and Qt Widget Object, 
  * Qt use object pointer reference, Maya use object name
* v007.2: 2016.09.20
  * fix layout margin clear
  * add quickPolicy
  * add quickInfo for quick notify and feedback, user customizable
* v007: 2016.09.09
  * v7.1: fix btnMsg issue
  * rewrite quickUI, backward compatible, and also optimized label creation for form layout, only create label when needed
  * enable you to directly nest quickUI inside quickUI with various return type,
    * eg. self.quickUI([self.quickUI(), self.quickUI()], 'main_vbox')
  * enable you to quickUI with tab, split, groupbox as layout object, same creation string syntax as element
  * a even compact pure text based UI creation and reference function on top of quickUI, called "qui()"
* v006.2: 2016.09.01
  * add utf8 support
  * better structure for fast template update
* v006.1.2:
  - add hotkey example
  - add self.memoData['data'] for default, since not affect self.memoData['lang']
* v006.1:
  - self location and location for load lang
  - window icon support and window intitial drag position
  - quickMsgAsk for user input
  - quickTabUI (no tab name lang out yet)
  - improve lang functions
  - fix qmenu creation for lang function
  - fix file icon template name
* v005: 2016.07.30 
 - add translation and stype function, better grid layout
* v004: 2016.07.28
* v003: 2016.07.22

----------

How to Use 
-------------

(for Version 9 and 10 and newer):
1. global replace class name "UserClassUI"  to "YourToolName" in your editor,
  - in icons folder, the Tool GUI icon should name as "YourToolName.png"
2. change file name "universal_tool_template.py" to "YourPythonFileName.py",
  - in icons folder, the Maya shelf icon should name as "YourPythonFileName.png", if you name all name the same, then 1 icon is enough
3. load it up and run
4. further edit:
  * change the version, date, log, help variable before UserClassUI to update your app internal info

(for Version 8 and older)
```
  * Prepare into Your Tool:
    1. global replace class name "UniversalToolUI"  to "YourToolName" in your editor,
      * in icons folder, the Tool GUI icon should name as "YourToolName.png"
    2. change file name "universal_tool_template.py" to "YourPythonFileName.py",
      * in icons folder, the Maya shelf icon should name as "YourPythonFileName.png", if you name all name the same, then 1 icon is enough
    3. load it up and run
```

  * loading template - Run in Application's python panel:
```python
import sys;myPath='/path_to_universal_tool_or_custom_name/';myPath in sys.path or sys.path.append(myPath);
import universal_tool_template
universal_tool_template.main() # no need this line for blender 
```

  * loading template - Run in system command console
```python
python universal_tool_template.py
```

One-line Multi-UI Creation Syntax
===================

My Varaible-Free Quick-GUI-Generating Text-Code Syntax
-------------
  * version 7 and above syntax 
```python
quickUI(["elementA_btn;QPushButton;Title Here"], "config_layout;QVBoxLayout")

element_list:

ui_name@ui_label;ui_type;ui_opts
#####################################
elementA_btn;QPushButton;Title Here
elementA_btn@User label;QPushButton;Title Here
elementB_choice@Choose one;QComboBox;(A,B,C,4)
partB_space;QSpacerItem;(200,10,5,4)
elementC_txtEdit@Custom label;LNTextEdit
partB_layout;vbox
partB_QVBoxLayout

main_split;QSplitter;v
main_tab;QTabWidget
elementB_grp@System label;QGroupBox;vbox,My Group Title


parentObject
parent_name;parent_type;parent_opts
#####################################
config_layout;QVBoxLayout
config_vbox
config_split;QSplitter;v
config_split;v
config_grp;QGroupBox;vbox,My Group Title
main_tab
main_tab;QTabWidget

parentObject's insert_opt
#####################################
gridLayout: "h", "v" for grid insertion
tab: (Tab A, Tab B, Tab C) for tab name insertion

#####################################

qui('elementA_btn;Title Here | elementB_label;Label here', 'config_vbox')

element_list:

ui_name@ui_label;ui_opts
#####################################
can't use ; in ui_opts

parentObject
parent_name;parent_type;parent_opts
#####################################
parentObject's insert_opt
#####################################
```

Universal Tool Template UI creation syntax
-------------

now all the creation is using qui function

| UI element | syntax | 
| --------- | ------------ |
| **QVBoxLayout** | `self.qui('my_vbox')` <br> `self.qui('my_layout;vbox')` |  
| **QHBoxLayout** | `self.qui('my_hbox')` <br> `self.qui('my_layout;hbox')` |  
| **QGridLayout** | `self.qui('my_grid')` <br> `self.qui('my_layout;grid')` |  
| | `self.qui('box_btn;Box \| sphere_btn;Sphere  \| ring_btn;Ring', 'my_layout;grid', 'h')` |  
|  | create and insert those 3 buttons as horizontal row in the grid  | 
| | `self.qui('box_btn;Box \| sphere_btn;Sphere  \| ring_btn;Ring', 'my_layout;grid', 'h')` <br> `self.qui('box2_btn;Box2 \| sphere2_btn;Sphere2 \| ring2_btn;Ring2', 'my_layout', 'h')` | 
|  | create 2 rows of button, first row (Box,Sphere,Rig), second row (Box2,Sphere2,Ring2)  | 
| | `self.qui('cat_btn;Cat \| dog_btn;Dog \| pig_btn;Pig', 'pet_layout;grid', 'v') ` <br> `self.qui('cat2_btn;Cat2 \| dog2_btn;Dog2 \| pig2_btn;Pig2', 'pet_layout', 'v') ` | 
|  | create 2 column of button, first column (cat,dog,pig), second column (cat2,dog2,pig2) | 
| **QFormLayout** | self.qui('my_form') <br> self.qui('my_layout;form') |  
| | `self.qui('name_input@Name:;John \| email_input@Email:;test@test.com', 'entry_form')` |  
|  | create a name input with label "Name:" and default text "John", and then create email input with label "Email" and default text "test@test.com" inside entry_form form layout | 
| | | 
| **QSplitter** | `self.qui('user_layout \| info_layout', 'my_split;h')` <br> `self.qui('user_grp \| info_tab', 'my_split;h')` |
|  | put user UI and info UI side by side in split, <br> child can be either a layout or widget | 
| **QGroupBox** | `self.qui('user2_btn;User2 \| info2_btn;Info2', 'my_grp;vbox,Personal Data')` | 
|  | put user UI and info UI inside "my_grp" group box and with internal vbox layout and title as "Personal Data" <br> Note:**no ,() in title** | 
| **QWidget** | `self.qui('user_label;Name \| user_input', 'user_widget;vbox')` |  
|  | like Groupbox widget, but without a title, useful for hide show a set of UIs | 
| **QTabWidget** | `self.qui('client_layout \| product_layout', 'database_tab;h', '(Client,Product)')` |
|  | put client UI and product UI into database_tab tabwidget, as horizontal tab, with title as "Client", "Product", UI can be either widget or layout | 
| | | 
| **QPushButton** | `self.qui('my_btn;Submit')` |  
|  | create pushbutton with title "Submit" | 
|  | `self.qui('my_btnMsg;Info')`  | 
|  | create pushbutton with title "Info" with automatically pop up a dialog show text string stored in self.uiList['my_msg'] | 
| **QLabel** | `self.qui('info_label;Please select all objects')` |  
|  | a label with text "Please select all objects"  | 
| **QLineEdit** | `self.qui('user_input;Your Email')` |  
|  | a line input with default text "Your Email" | 
| **QCheckBox** | `self.qui('testOnly_check;Run as Test Only')` | 
|  | create a check box with title "Run as Test Only"  | 
| **QComboBox** | `self.qui('objectType_choice;(Box,Sphere,Ring)')` |
|  | create a drop down list with option "Box", "Sphere", "Ring"| 
| || 
| **QTextEdit** | `self.qui('comment_txt;Please write details here')`  |
|  | create a text area with default text "Please write details here" | 
| || 
| **QListWidget** | `self.qui('name_list')` |
|  | note, list has no header and single column | 
| **QTreeWidget** | `self.qui('file_tree;(Name,Path)')` |
|  | create a tree widget with column names as "Name", "Path"| 
| **QTableWidget** | `self.qui('data_table;(Name,Email,Phone)')` |
|  | create a data table with column name as "Name", "Email", "Phone" | 
| || 
| **QSpacerItem** | `self.qui('user_space;(100,30,4,3)')` | 
|  | create a space item with policy expanding horizontally and normal vertically <br> # 0 = fixed; 1 > min; 2 \< max; 3 = prefered; 4 = \<expanding>; 5 = expanding> Aggresive; 6=4 ignored size input | 

now all menu creation is using qui_atn,qui_menu,qui_menubar function (replaced quickMenuAction, quickMenu since v11)

| menu element | syntax | 
| --------- | ------------ |
| **QMenu** | `self.qui_menu('right_menu_createFolder_atn;Create Folder,Ctrl+D \| _ \| right_menu_openFolder_atn;Open Folder', 'right_menu')` |
|  | create a list of menu QAction with title and optional shortcut and form (into) a menu object, while _ means a seperator in menu |
|  | `self.qui_menubar('file_menu;&File \| setting_menu;&Setting \| help_menu;&Help')` |
|  | create a list of menu in menubar |
| **QAction** | `self.qui_atn(ui_name, title, tip=None, icon=None, parent=None, key=None)` <br> `self.qui_atn('importConfig_atn','Import Config (&I)','Import Config Setting.','importConfig.png', 'setting_menu', 'Ctrl+I')`  |
|  | create a detailed QAction with uiList name, title, tip, icon, optionally inside a menu; for simple menuAction creation, just use with qui_menu |
| **QShortcut** | `self.qui_key('editNoter', 'Alt+E', self.editNoter_action )` |
|  | create hotkey without a menuAction, stored in self.hotkey |


File Structure
===================

  * **universal_tool_template_VERSION.py**: main TEMPLATE and USERCLASS and MAIN()
  * **GearBox**: a json config file editor for both language dict files and config export dict files from template.
  * **LNTextEdit.py**: (optional) if you want to use LNTextEdit in your tool.
  * **UITranslator.py**: (optional) a GUI tool to create translation json file from template's exported default language json
  * **install-v5.0_App.mel**: (optional) a quick Maya shelf installer that auto put python tool in maya shelf based on naming format and ctrl+RMB menu for reload your tool, good for code test
  * **universal_tool_template.bat**: window console mode or window mode auto launcher, it detect whether to use launch with pythonw or python by the file name
    * if you name as YourPythonFileName.bat, it will launch a console to run your Py
    * if you name as YourPythonFileName_w.bat, it will use Pythonw to directly run your Py without pop-up console floating there
    * if you name as YourPythonFileName_z.bat, it will launch without console in Python3 (change the py3 path inside)
    * if you name as YourPythonFileName_x.bat, it will launch with console in Python3 (change the py3 path inside)


Screenshot
===================

![universal_tool_template_v10.2.png](screenshot/universal_tool_template_v10.2.png?raw=true)
![universal_tool_template_v10.2_blender.png](screenshot/universal_tool_template_v10.2_blender.png?raw=true)
![universal_tool_template_v10.2_fusion.png](screenshot/universal_tool_template_v10.2_fusion.png?raw=true)
![universal_tool_template_v10.2_houdini.png](screenshot/universal_tool_template_v10.2_houdini.png?raw=true)
![universal_tool_template_v8.0.png](screenshot/universal_tool_template_v8.0.png?raw=true)
![universal_tool_template_v7.3.png](screenshot/universal_tool_template_v7.3.png?raw=true)
![universal_tool_template_v5.0.png](screenshot/universal_tool_template_v5.0.png?raw=true)
![universal_tool_template_v4.0.png](screenshot/universal_tool_template_v4.0.png?raw=true)
![universal_tool_template_v3.0.png](screenshot/universal_tool_template_v3.0.png?raw=true)

File Structure in Details
===================

GearBox
-------------
  * a json dict file editor, for editing config dict file exported from template for external config file use.
  * it also can serve a lite or better version of UITranslator.py
  * you can also use it as a example of how universal_tool_template.py can be used to create tools

**screenshot**

![GearBox_v1.0.png](screenshot/GearBox_v1.0.png?raw=true)
![GearBox_v1.0_2.png](screenshot/GearBox_v1.0_2.png?raw=true)

**usage**
  * run the GearBox_w.bat to start it if you have python on windows
  * load the json file from browser inside it,
  * click on the tree item to show in the bottom left preview text box, and use right text box to draft out your edit content and then copy paste into edit field on the tree, by double click the tree item.
  * change the file name if you want to export as different file
  * click export button below to save it

**feature list**
  * v001.1 (2017.09.25)
    * update GearBox to template 1010,
    * fix export null error when there is single data entry in the config_tree and the data has a name
  * v001. (2017.04.17)
    * support dict type json file only
    * file loading and exporting
    * add, remove tree branch
    * edit the field and has a large preview text box to auto loading from selection
    * show pure text for json text data, and show json format text for other type data in tree view

LNTextEdit.py
-------------
  * a line number text edit Ui element, a replacement of the original LNTextEdit and my variations like LNTextEditEx, LNTextEdit_Pside, LNTextEdit_PyQt

**usage**

```python
import LNTextEdit
display_textEdit = LNTextEdit.LNTextEdit()
display_textEdit.setWrap(0)
display_textEdit.setReadOnly(1)
display_textEdit.setReadOnlyStyle(1)
display_textEdit.setZoom(1) # enable text zoom feature
```

**feature list**

  * version 4.0: (2016.12.08)
    * python 3 support
    * pyside, pyside2, pyqt4, pyqt5 support
  * version 3.2: (2016.09.01)
    * add get/set/resetFontSize function
    * support ctrl+mouse wheel zoom in out text area, need to setZoom(1)
  * version 3.1:
    * (v3.1.2) add unicode support for file url
    * add multiple files drop as path text input
    * add insertText function
  * version 3.0:
    * support drag and drop file or file url as url text
    * support setReadOnly and setReadOnlyStyle function
    * support setWrap() quick function
    * support text() function
    * better and clear code for PyQt4 and PySide
  
UITranslator.py
-------------
  * A tool to create UI interface translation language json file for auto load into universal tool template
  * Note: UITranslator works for any tool created based on universal tool template above v6.1

**Feature**
  * version 2.0: (2016.12.20)
    * rewrite based on universal_tool_template.py v8.1
    * add reset action in file menu
  * version 1.0: (2016.07.22)
    * load default language that exported from your tool based on universal tool template above v6.1
    * create new translation and store them in memory before export to a language json file
    * load multiple language json file

**How to Use**

  * load in maya: 
```python
import UITranslator
UITranslator.main()
```
  * load in commandline:
```python
python UITranslator.py
```
  * usage:
    * use load button at bottom to load up the exported default language json file from those universal_tool_template based tools
    * file menu > add language to add a new translation
    * translate one by one for your need in that table column
    * click "Process and Update memory" button to update the table content into memory
    * then, the drop down list for export shows which language you want to export, Note, make sure you change the path on the file input before you click Export button, otherwise, it will overwrite whatever in the file input's path
  * output language file name format:
    * language file naming format: ```ToolName_lang_YourLanguageName.json```
    
**File Structure**
  * UITranslator.py
  * LNTextEdit.py: mod 3rd party line number text edit ui element
  * icons/UITranslator.png: (32x32) https://icons8.com/web-app/for/all/translate

**screenshot**

![uitranslator_v1.0.png](screenshot/uitranslator_v1.0.png?raw=true)

auto maya shelf installer v5.0 (install-v5.0_App.mel)
-------------

  * a script template that automatically install its nearby python tool to shelf, with icon set as well, in a simple process of drag-n-drop into maya window.

**feature and usage**:
  * version 5.0 (2017.04.10)
    * ctrl+ LMB click to pop "reload" submenu. Thus, no need reload and install, just 1 mel script to hold 2 features
  * version 3.0 (2016.12.20):
    * Fully auto install by this file name, example "install_Python_File_Name.mel" or "install_PythonFileName.mel"
    * the icon should be named as "Python_File_Name.png" or "PythonFileName" accordingly inside "icons" folder, your icon is (32x32) in size
    * optionally with version number label on top, example: "install-v8.1_universal_tool_template.mel"
    * if you need to change version label color and version label background rgba, change last line
      * -overlayLabelColor 0 0 0 (0-1 means black to white) 
      * -overlayLabelBackColor 1 1 1 0.0 (last float 0-1 means hide-show for bg color )

cross-platform cx_Freeze binary build script
-------------

  * just change the ToolName, and includes the folder or resource, then run buildScript in windows, mac, linux to create binary
