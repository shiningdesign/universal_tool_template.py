@echo off
set p3=D:\z_sys\App_Dev\Python35x64_01\

REM YourPythonFileName_w.bat will launch without console
REM YourPythonFileName.bat will launch with console
REM YourPythonFileName_z.bat will launch without console in Python3
REM YourPythonFileName_x.bat will launch with console in Python3

set file=%~n0
if "%file:~-2%" equ "_w" (
  start pythonw %~dp0%file:~0,-2%.py
  goto done
)
if "%file:~-2%" equ "_z" (
  start %p3%pythonw.exe %~dp0%file:~0,-2%.py
  goto done
)
if "%file:~-2%" equ "_x" (
  %p3%python.exe %~dp0%file:~0,-2%.py
  goto console
)
call python %~dp0%~n0.py

:console
pause
:done
