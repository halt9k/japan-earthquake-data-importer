Cls
# Do not change scope
$ErrorActionPreference = "Stop"

# include
. .\env\py_environment.ps1


function Wait-UserInput 
	{
	Write-Host -NoNewLine 'Press any key to continue...';
	$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
	}


function Run-PyScript([string]$ENVIROMENT_ACTIVATION_CMD, [string]$tmp_dir)
	{
	if (Try-Activate-PythonEnviroment $PY_ENV_FOLDER $True)
		{
		py src\main.py
		deactivate

		# Wait-UserInput
		}
	}