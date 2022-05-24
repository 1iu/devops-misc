# Miscellaneous Devops Projects
## Pre
```
pip install -r requirements.txt
```
## Usage

``` sh
# connect once
python sim_connect.py --notify --timer=10
# add to task scheduler (windows) Monday 9:30
SCHTASKS /CREATE /SC WEEKLY /D MON /TN "ConnectTHU" /TR "cd \PATH_TO_YOUR_TASK\thu-sim-connect\ & \PATH_TO_YOUR_PYTHON\pythonw.exe sim_connect.py --notify --timer=10" /ST 09:30 
```

