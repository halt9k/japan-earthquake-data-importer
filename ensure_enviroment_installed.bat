if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )
powershell .\env\ensure_enviroment.ps1