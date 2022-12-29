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

wget https://www.python.org/ftp/python/3.9.10/python-3.9.10-embed-amd64.zip -o python-3.9.10-embed-amd64.zip
Expand-Archive python-3.9.10-embed-amd64.zip
wget https://bootstrap.pypa.io/get-pip.py -o get-pip.py
mv python-3.9.10-embed-amd64\python39._pth python-3.9.10-embed-amd64\python39.pth
mkdir python-3.9.10-embed-amd64\DLLs
python-3.9.10-embed-amd64\python.exe get-pip.py

python-3.9.10-embed-amd64\python.exe -m pip install virtualenv

python-3.9.10-embed-amd64\python.exe -m virtualenv testenv
cp python-3.9.10-embed-amd64\python39.zip testenv\Scripts\

testenv\Scripts\Activate.ps1

pip install pandas
pip install xlwings

cd ..