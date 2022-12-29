cls
@echo off

REM Modify next line:
REM set PYHTON_EXE_PATH=""
set PYHTON_EXE_PATH=python-3.9.10-embed-amd64

set PATH=%PYHTON_EXE_PATH%;%PATH%;
python --version 2>NUL

if ERRORLEVEL 1 (
	echo "Python scripting enviroment not found. Options:"
	echo "1) find python.exe already installed on drives"
	echo "3) download from official https://www.python.org/downloads/"
	echo "TODO) use windows store to install"
	echo "TODO) try included simple auto installer"
	echo.
	echo "After any of options done - modify run_import.bat with correct PYHTON_EXE_PATH"
	echo "TODO) packages like pandas, numpy, tkinter may still be missing."
	REM python
	goto:exit
)

python src\main.py

if ERRORLEVEL 1 (
	echo.
	echo "If result was No module named 'pandas'"
	echo "These commands may fix it:"
	echo PYHTON_EXE_PATH"\Scripts\pip install pandas"
	echo PYHTON_EXE_PATH"\Scripts\pip install xslx"
)

:exit
set /p DUMMY=Hit ENTER to continue...
