cls

REM @echo off
set PYTHON_DIR="C:\ProgramData\Anaconda3\envs\temp\"
REM set ENV_DIR="C:\ProgramData\Anaconda3\Scripts\"

IF [%ENV_DIR%] == [] (
	goto try_python
)
if exist %ENV_DIR% (
	echo "Run via environment"

	REM OpenSSL fix for Anacodna
	REM SET PATH=%PATH%;%PYTHON_DIR%\Library\bin\
	
	%ENV_DIR%\conda.exe run -n base python src\main.py
	
	echo "Run via environment done"
	goto exit	
)


:try_python
IF [%PYTHON_DIR%] == [] goto try_raw

if exist %PYTHON_DIR% (
	echo "Run via Python Installation"
	
	%PYTHON_DIR%\python.exe --version 2>NUL

	if errorlevel 1 (
		echo Error^: Python not installed
		goto:exit
		)
		
	%PYTHON_DIR%\python.exe src\main.py
	echo "Run via Python Installation done"
	goto exit
)

:try_raw
echo "Run via bare python"
python.exe src\main.py

:exit
set /p DUMMY=Hit ENTER to continue...
