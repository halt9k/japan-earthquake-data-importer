if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )
powershell .\run_import.ps1