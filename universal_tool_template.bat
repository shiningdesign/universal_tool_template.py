@echo off
REM YourPythonFileName_w.bat will launch without console
REM YourPythonFileName.bat will launch with console
set file=%~n0
if "%file:~-2%" equ "_w" (
  start pythonw %~dp0%file:~0,-2%.py
  goto done
)
call python %~dp0%~n0.py
pause
:done
