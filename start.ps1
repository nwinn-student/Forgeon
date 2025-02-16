$Folder = '.\forgeon_env'

if(Test-Path -Path $Folder){
    .\forgeon_env\Scripts\Activate.ps1
}
else{
    Write-Output "Virtual Environment not found, creating and installing dependencies..."
    python -m venv forgeon_env
    .\forgeon_env\Scripts\Activate.ps1
    python -m pip install flask flask-sqlalchemy flask-login gevent
}

python main.py