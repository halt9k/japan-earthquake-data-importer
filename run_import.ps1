Cls

$ENV_PATH = '.\python\testenv\Scripts\Activate.ps1'
$DEFAULT_ENV_PATH = './env/Scripts/activate.ps1'


function Stop-OnErrors 
	{
	$ErrorActionPreference = "Stop"
	}


function Wait-UserInput 
	{
	Write-Host -NoNewLine 'Press any key to continue...';
	$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
	}


function Try-ActivatePyEnv 
	{
	# possibly unused
	Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
	
	if (Test-Path -Path $ENV_PATH) 
		{
		Write-Output "Trying to run under portable enviroment"
		& $ENV_PATH
		}
	elseif (Test-Path -Path $DEFAULT_ENV_PATH) 
		{
		Write-Output "Trying to run under default Windows python enviroment"
		& $DEFAULT_ENV_PATH		
		} 
	else 
		{
		Write-Output "No script enviroments found. Fix manually based on this script source."
		Exit
		}
	}


function Test-PyEnv 
	{
	$py_version = (&{python -V}).Exception.Message
	if ($py_version)
		{
		Write-Output "Python version is missing or lower than 3. Something is broken.", $py_version
		Exit
		}
	}

Stop-OnErrors
Try-ActivatePyEnv
Test-PyEnv

python src\main.py

# Wait-UserInput