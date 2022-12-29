Cls

$PYHTON_PATH = '.\python'
if (Test-Path -Path $PYHTON_PATH) {
    Write-Output "Python folder already exists. To try reinstall, delete folder or modify ps1"
    Exit
} else {
    New-Item -ItemType Directory -Force -Path $PYHTON_PATH
    cd $PYHTON_PATH
}

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

function Install-Embedded-Python {
	wget https://www.python.org/ftp/python/3.9.10/python-3.9.10-embed-amd64.zip -o python-3.9.10-embed-amd64.zip
	Expand-Archive python-3.9.10-embed-amd64.zip
	wget https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	mv python-3.9.10-embed-amd64\python39._pth python-3.9.10-embed-amd64\python39.pth
	mkdir python-3.9.10-embed-amd64\DLLs
	python-3.9.10-embed-amd64\python.exe get-pip.py
	 
	python-3.9.10-embed-amd64\python.exe -m pip install virtualenv

	python-3.9.10-embed-amd64\python.exe -m virtualenv testenv
	cp python-3.9.10-embed-amd64\python39.zip testenv\Scripts\
}


function Install-Silent-Python {
	wget https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe -o python-3.11.1-amd64.exe
    $Target = Resolve-Path .
    $Target = Join-Path -Path $Target -Childpath 'python-3.11.1-amd64'
	.\python-3.11.1-amd64.exe InstallAllUsers=1 TargetDir=$Target AssociateFiles=0 InstallLauncherAllUsers=0 /passive

	python-3.11.1-amd64\python.exe -m pip install virtualenv

	python-3.11.1-amd64\python.exe -m virtualenv testenv	
}
Install-Silent-Python

testenv\Scripts\Activate.ps1

pip install pandas
pip install xlwings

cd ..