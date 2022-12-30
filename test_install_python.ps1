Cls
$ErrorActionPreference = "Stop"

Write-Host 'This installer is optional and not well tested.'
Write-Host 'It worked, but may override python paths and damage other installs.' 
Write-Host 'Alternative way is to modify in run_import.ps1 path to correct activate.ps1'
Write-Host -NoNewLine 'Use at your own risk'
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')


$PYHTON_PATH = '.\python'
if (Test-Path -Path $PYHTON_PATH) {
    Write-Output "WARNING: Python folder already exists. Retrying this installer is not supposed."
} else {
    New-Item -ItemType Directory -Force -Path $PYHTON_PATH    
}
cd $PYHTON_PATH


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
function wget_safe ([string]$download_link, [string]$target_name){
	if (Test-Path -Path $target_name) {
		Write-Output "WARNING: Requested download already exists. Delete manually to download again. " $target_name
		return
	}
	
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
	Invoke-WebRequest -Uri $download_link  -OutFile $target_name
}


function Install-Embedded-Python {
	$PY_EMBED_FOLDER = 'python-3.9.10-embed-amd64'
	$PY_EMBED_ARC = $PY_EMBED_FOLDER + '.zip'
	$PY_EMBED_DOWNLOAD_LINK = 'https://www.python.org/ftp/python/3.9.10/python-3.9.10-embed-amd64.zip'
	
	#wget $PY_EMBED_DOWNLOAD_LINK -o $PY_EMBED_ARC
	wget_safe  $PY_EMBED_DOWNLOAD_LINK $PY_EMBED_ARC	
	
	Expand-Archive $PY_EMBED_ARC
	wget https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	
	mv $PY_EMBED_FOLDER\python39._pth $PY_EMBED_FOLDER\python39.pth
	mkdir $PY_EMBED_FOLDER\DLLs
	& $PY_EMBED_FOLDER\python.exe get-pip.py
	 
	& $PY_EMBED_FOLDER\python.exe -m pip install virtualenv

	& $PY_EMBED_FOLDER\python.exe -m virtualenv testenv
	cp $PY_EMBED_FOLDER\python39.zip testenv\Scripts\
}


function Install-Silent-Python {
	$PY_INST_FOLDER = 'python-3.11.1-amd64'
	$PY_INST_EXE = $PY_INST_FOLDER + '.exe'
	$PY_INST_DOWNLOAD_LINK = 'https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe'
	
	# wget $PY_INST_DOWNLOAD_LINK -o $PY_INST_EXE
	 wget_safe  $PY_INST_DOWNLOAD_LINK $PY_INST_EXE
	
    $Cur = Resolve-Path .
    $Target = Join-Path -Path $Cur -Childpath $PY_INST_FOLDER
	& .\$PY_INST_EXE InstallAllUsers=1 TargetDir=$Target AssociateFiles=0 InstallLauncherAllUsers=0 /passive | Out-Null
	
	if (-not (Test-Path -Path $PY_INST_FOLDER)) {
		Write-Output "ERROR: Python silent install failed."
		Write-Output "Unsafe solution from UI: Repair, Delete, Rerun this script"
		Write-Output "Install manually from " $PY_INST_EXE " to " $PY_INST_FOLDER
		Exit
	}

	& $PY_INST_FOLDER\python.exe -m pip install virtualenv

	& $PY_INST_FOLDER\python.exe -m virtualenv testenv	
}
Install-Silent-Python

testenv\Scripts\Activate.ps1

pip install pandas
pip install xlwings

cd ..

