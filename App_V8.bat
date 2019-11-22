@echo off
set CustPython=R:\Pipeline\App_Win\Python27x64\
set LocalCustPython=D:\z_sys\App_Dev\Python35x64_01\
IF EXIST %LocalCustPython% (
  set CustPython=%LocalCustPython%
)

:: auto_launcher V8 (2019.11.22)
:: v8 (2019.11.22) more auto detection and improve bat logic
:: v7 (2019.10.01) fix _x, _z auto close
:: v6 (2019.08.07): for duplicate desktop window case, it will done instead of pause; rename p3 into CustPython 
:: v5 (2018.02.21): it will auto rename cmd title to cmd:AppName
:: YourPythonFileName_w.bat will launch without console
:: YourPythonFileName.bat will launch with console
:: YourPythonFileName_z.bat will launch without console in CustPython
:: YourPythonFileName_x.bat will launch with console in CustPython
:: %file:~0,-2%: is YourPythonFileName_x[:2]  = YourPythonFileName

set file=%~n0
:: remote python mode - no cmd window
if "%file:~-2%" equ "_z" (
  start %CustPython%pythonw.exe %~dp0%file:~0,-2%.py
  goto done
)
:: remote python mode - python with cmd window
if "%file:~-2%" equ "_x" (
  title cmd:%file:~0,-2%
  echo %CustPython%
  call %CustPython%python.exe %~dp0%file:~0,-2%.py && GOTO done
  goto console
)
:: local python mode - pythonw
if "%file:~-2%" equ "_w" (
  start pythonw %~dp0%file:~0,-2%.py
  goto done
)
:: local python mode - python
:: -- _vX case
if "%file:~-3,-1%" equ "_V" (
  title cmd:%file:~0,-3%
  call python %~dp0%file:~0,-3%.py && GOTO done
  goto console
)
:: -- _vXX case
if "%file:~-4,-2%" equ "_V" (
  title cmd:%file:~0,-4%
  call python %~dp0%file:~0,-4%.py && GOTO done
  goto console
)
:: -- pure name case
title cmd:%~n0
REM if run ok, then go done:
REM - user close program, 0 > done
REM - program error 1 > pause
REM - program duplicate error 1 > pause
call python %~dp0%~n0.py && GOTO done


:console
pause
:done
