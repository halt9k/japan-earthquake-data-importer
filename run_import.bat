REM Check for Python Installation

echo off
set PYTHON_DIR="C:\ProgramData\Anaconda3\envs\temp\"
%PYTHON_DIR%\python.exe --version 2>NUL

if errorlevel 1 (
	echo Error^: Python not installed
	goto:exit
	)

REM OpenSSL fix for Anacodna
SET PATH=%PATH%;%PYTHON_DIR%\Library\bin\
%PYTHON_DIR%\python.exe src\main.py

:exit
set /p DUMMY=Hit ENTER to continue...
