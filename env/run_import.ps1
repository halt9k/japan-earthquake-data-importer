Cls
# Do not change scope
$ErrorActionPreference = "Stop"

. .\env\py_environment.ps1


function Wait-UserInput 
	{
	Write-Host -NoNewLine 'Press any key to continue...';
	$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
	}

Try-Activate-PythonEnviroment $PY_ENV_FOLDER $True

python src\main.py
deactivate

# Wait-UserInput