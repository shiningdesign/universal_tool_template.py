@echo off
SetLocal EnableDelayedExpansion

echo AutoLaucher v9 (2020.09.01)
set CustPython=
set CustList=(R:\Pipeline\App_Win\Python27x64\ D:\z_sys\App_Dev\Python35x64_01\ D:\z_sys\App\Python27\ D:\App\Python27\)

:: auto_launcher V9 (2020.09.01)
:: v9 (2020.09.01) re-writen detection and use method
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
set folder=%~dp0
set useCust=0
set winMode=0

:: Detect Name
:: default
set className=%file%
:: remote python mode - no cmd window
if "%file:~-2%" equ "_z" (
    set useCust=1
    set winMode=1
    set className=%file:~0,-2%
)
:: remote python mode - python with cmd window
if "%file:~-2%" equ "_x" (
    set useCust=1
    set className=%file:~0,-2%
)
:: local python mode - pythonw
if "%file:~-2%" equ "_w" (
    set winMode=1
    set className=%file:~0,-2%
)
:: local python mode - python
:: -- _vX case
if "%file:~-3,-1%" equ "_V" (
    set className=%file:~0,-3%
)
:: -- _vXX case
if "%file:~-4,-2%" equ "_V" (
    set className=%file:~0,-4%
)
REM if run ok, then go done:
REM - user close program, 0 > done
REM - program error 1 > pause
REM - program duplicate error 1 > pause
echo %className% (:cmd;_w:window;_z:cust_win;_x:cust_cmd)
if %useCust% == 0 (
    REM check local python
    :CHECK_PYTHON_EXIST
    python --version 2>NUL
    if errorlevel 1 (
        set useCust=1
        goto CUSTPROCESS 
    ) else (
        REM local python
        if %winMode% == 1 (
            start pythonw %folder%%className%.py
            goto done
        )
        if %winMode% == 0 (
            title cmd:%className%
            call python %folder%%className%.py && GOTO done
            goto console
        )
    )
)
:CUSTPROCESS
if %useCust% == 1 (
    REM load cust python path
    for %%x in %CustList% do (
        IF EXIST %%x (
            set CustPython=%%x
        )
    )
    echo Use Python:!CustPython!
    if %winMode% == 1 (
        start !CustPython!pythonw.exe %folder%%className%.py
        goto done
    )
    if %winMode% == 0 (
        title cmd:%className%
        call !CustPython!python.exe %folder%%className%.py && GOTO done
        goto console
    )
)
:console
pause
:done