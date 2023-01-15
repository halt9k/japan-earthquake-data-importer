Cls
# Do not move to functions
$ErrorActionPreference = "Stop"

Write-Host 'This script will try to install python enviroment automatically.'


$PY_INSTALLER_DOWNLOAD_LINK = 'https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe'
$PY_ENV_FOLDER = '.\python_enviroment'


$PYTHON_LAUNCHER_EXE = "py"
$ENVIROMENT_ACTIVATION_CMD = "Scripts\Activate.ps1"


function Assert ([bool]$condition, [string]$msg)
	{
	if ($condition) 
		{ return }
		
	Write-Host ""
	Write-Host "ERROR: $msg"
	Write-Host ""
	Exit
	}


function Ensure-Dir ([string]$dir_path)
	{
	if (Test-Path -Path $dir_path) 
		{ return }

	New-Item -ItemType Directory -Force -Path $dir_path
	}


function Download-File ([string]$link, [string]$target_path)
	{
	if (Test-Path -Path $target_path) 
		{
		Write-Host "Installer already downloaded. Delete manually to retry: $target_path"		
		return
		}
	
	# wget $link -o $target_path
	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
	Invoke-WebRequest -Uri $link  -OutFile $target_path
	}


function Install-PythonSilently  ([string]$download_link, [string]$tmp_dir)
	{
	Write-Host "Downloading python installer"
	
	$exe_name = Split-Path $download_link -leaf	
	Ensure-Dir $tmp_dir
	$exe_path = Join-Path $tmp_dir $exe_name
	Download-File  $download_link $exe_path
	
	Write-Host "Installing python and launcher"
	# May easily fail with other params
	$output = & $exe_path InstallAllUsers=1 AssociateFiles=0 InstallLauncherAllUsers=1 Include_launcher=1 /passive 2>&1 | Out-String
	
	return [bool]$output
	}


function Test-PythonLauncher
	{
	Write-Host "Testing launcher"
	
    # test if launcher exists
	if (-not (Get-Command $PYTHON_LAUNCHER_EXE -errorAction SilentlyContinue)) 
		{ return $False }

    # test if python version > 3.0 activates;
	# & $PYTHON_LAUNCHER_CMD -V
	
    $output = & $PYTHON_LAUNCHER_EXE -3 -V 2>&1 | Out-String
	
	return [bool]$output
	}
	

function Ensure-Python ([string]$download_link, [string]$tmp_dir)
	{
	if (Test-PythonLauncher) 
		{ 
		Write-Host "Launcher finished successfully. Python install skipped."
		return 
		}
		
	Install-PythonSilently $download_link $tmp_dir
	
	Assert (Test-PythonLauncher) ("Python launcher is missing. `n" +
		"Try to install manually from $PY_INSTALLER_DOWNLOAD_LINK `n" +
		"Ensure launcher option in python installer. `n")
	}


function Try-Activate-PythonEnviroment ([string]$env_path, [bool]$activate)
	{
	Write-Host "Trying to activate $env_path"
		
    $activation_cmd = Join-Path $env_path $ENVIROMENT_ACTIVATION_CMD
    $exists = Test-Path -Path $activation_cmd

    if (-not $activate)
        { 
		Write-Host "Environment activation script exists: $exists"
		return $exists 
		}

    & $activation_cmd
    return $True
	}


function Ensure-PythonEnviroment ([string]$env_path)
	{
	if (Try-Activate-PythonEnviroment $env_path $False) 
		{ return }

	Write-Host "Installing virtual enviroment in $env_path"
    & $PYTHON_LAUNCHER_EXE -3 -m pip install virtualenv
	& $PYTHON_LAUNCHER_EXE -3 -m venv $env_path

	Assert (Try-Activate-PythonEnviroment $env_path $False) (
		"Python environment creation failed. Try to run *.py script manually. ")
	}


function Install-Dependencies  ([string]$env_path)
	{
	Write-Host "Installing additional python packages"
	
	Try-Activate-PythonEnviroment $env_path $True
	
	pip install pandas
	pip install xlwings

    deactivate
	}


Ensure-Python $PY_INSTALLER_DOWNLOAD_LINK $PY_ENV_FOLDER
Ensure-PythonEnviroment $PY_ENV_FOLDER
Install-Dependencies $PY_ENV_FOLDER


