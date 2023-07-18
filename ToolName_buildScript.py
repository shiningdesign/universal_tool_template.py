appName = 'ToolName'
appVer = '1.0'
subfolder_list = ["icons/"] # ,"res/","bin/"
'''
# buildScript 0.5:
v0.5: (2023.07.18)
  * add extra notes for some common build error
v0.4: (2022.12.18)
  * update for pyside2
v0.3: (2022.10.14)
  * force python3 pack all lib in zip, so less file count in folder
  * add some more exclude
v0.2 : (2020.05.18)
  * add exclude to reduce QT lib size and avoid include everything
v0.1 : (2018.09.24)
  * start of automated buildScript to convert python to binary
'''
'''
Extra notes: 
  * if you need console popup at same time, remove comment from base=None and comment the Win32GUI line
  * if you use requests, make sure in your main code, add below after import requests
# fix for cx_freeze
from multiprocessing import Queue
  * also remove ssl module from exclude_lib_list below

'''
# ---- qtMode 2020.02.13 modified ----
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
            qtMode = 1
        except ImportError:
            from PyQt5 import QtGui,QtCore,QtWidgets
            qtMode = 3
print('Qt: {0}'.format(qtModeList[qtMode]))

# main process
from cx_Freeze import setup, Executable
import sys

# ---- qt lib content detection ----
qt_lib_list = []
qt_lib = []
exclude_lib_list = []
if qtMode == 0:
    qt_lib_list = ['PySide.QtCore','PySide.QtGui']
    qt_lib = ['PySide']
    exclude_lib_list = ['PySide.QtNetwork','PySide.QtScript','PySide.QtSql']
elif qtMode == 1:
    qt_lib_list = ['PyQt4.QtCore','PyQt4.QtGui']
    qt_lib = ['PyQt4']
    exclude_lib_list = []
elif qtMode == 2: 
    qt_lib_list = ['PySide2.QtCore','PySide2.QtGui', 'PySide2.QtWidgets']
    qt_lib = ['PySide2']
    exclude_lib_list = ['PySide2.QtNetwork','PySide2.QtScript','PySide2.QtSql']
elif qtMode == 3: 
    qt_lib_list = ['PyQt5.QtCore','PyQt5.QtGui', 'PyQt5.QtWidgets']
    qt_lib = ['PyQt5']
    exclude_lib_list = []

# remove extra
exclude_lib_list.extend(["tkinter","ssl","bz2","asyncio"])

# base = None # use this if you need console with your app
base = 'Win32GUI' if sys.platform=='win32' else None
# 1. simpler buildOption without optimize
# buildOptions = dict(packages = [], excludes = [], includes = ["atexit"], include_files = ["icons/"])

# 2. smaller buildOption with only needed
# ref: https://stackoverflow.com/questions/27281317/cx-freeze-preventing-including-unneeded-packages
buildOptions = {
    'packages': [],
    'excludes': exclude_lib_list,
    'zip_include_packages': qt_lib+["*"],
    'zip_exclude_packages': [],
    'includes': ['atexit']+qt_lib_list,
    'include_files': subfolder_list,
    'optimize': 2,
}
                     
executables = [
    Executable('{0}.py'.format(appName), base=base, icon="icons/{0}.ico".format(appName))
]
setup(
    name='{0}'.format(appName),
    version = '{0}'.format(appVer),
    description = '{0} {1}.'.format(appName,appVer),
    options = dict(build_exe = buildOptions),
    executables = executables
)