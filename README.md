# Forgeon
Forgeon is a mapping generator FOR game designers, D&amp;D game masters, and other individuals who may benefit from dungeon content who wish to boost their productivity and focus on storytelling rather than the tedious aspects


# How to Download/Run
Click the "Code" button and then "Download ZIP".
Navigate to the zip location, unzip it, and attempt to run start.ps1 by Right-clicking and clicking Run Powershell.

# Troubleshooting
When downloading and attempting to test, one may get errors. The start.ps1 is meant to be run in a Windows machine on PowerShell.

You may get the error "File .ps1 cannot be loaded because running scripts is disabled on this system.". In this case, you can open up a new PowerShell instance and enter "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser". There is a security precaution however, so you should remember to enter "Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser" once you are done using the website application.

You may be told that Python was not found, meaning that either you do not have python, or you need to perform some adjustments. The adjustments would be first checking whether entering "python" in PowerShell sends you to the Microsoft Store, if so then you need to go to "Manage App Execution Aliases" and turn off the python related App Installers. Should the issue persist, go to "Edit environment variables for your account", click "Path", then "Edit", then "New", then find your python.exe path. It may be inside the location "C:/Users//AppData/Local/Programs/Python/Python312". Upon doing so, retry running the start.ps1, if it does not work still then research the error message and let us know in an issue.