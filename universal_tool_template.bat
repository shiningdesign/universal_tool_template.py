@echo off
set CustPython=D:\z_sys\App_Dev\Python35x64_01\

REM auto_launcher V7 (2019.10.01)
REM v7 (2019.10.01) fix _x, _z auto close
REM v6 (2019.08.07): for duplicate desktop window case, it will done instead of pause; rename p3 into CustPython 
REM v5 (2018.02.21): it will auto rename cmd title to cmd:AppName
REM YourPythonFileName_w.bat will launch without console
REM YourPythonFileName.bat will launch with console
REM YourPythonFileName_z.bat will launch without console in CustPython
REM YourPythonFileName_x.bat will launch with console in CustPython


set file=%~n0
if "%file:~-2%" equ "_w" (
  title cmd:%file:~0,-2%
  start pythonw %~dp0%file:~0,-2%.py
  goto done
)
if "%file:~-2%" equ "_z" (
  start %CustPython%pythonw.exe %~dp0%file:~0,-2%.py
  goto done
)
if "%file:~-2%" equ "_x" (
  title cmd:%file:~0,-2%
  %CustPython%python.exe %~dp0%file:~0,-2%.py
  goto done
)
title cmd:%~n0
REM if run ok, then go done:
REM - user close program, 0 > done
REM - program error 1 > pause
REM - program duplicate error 1 > pause
call python %~dp0%~n0.py && GOTO :done


:console
pause
:done
