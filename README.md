# Citrix Log Me In

This scripts automates logging in to Citrix Workspace(currently designed just to work with Cisco CMS Citrix).

---
### Pre-requisites
Following apps should be installed already on the machine:
1. Python3 (Tested on 3.10.0 or higher)
2. Citrix Workspace
3. Google Chrome browser


### How to run this locally?
1. In the .env file, add your Citrix URL, CEC username, password and Citrix password.
2. Create a python virtual environment. `python3 -m venv .venv`
3. Activate a python virtual environment. `source .venv/bin/activate`
4. Install the required packages from requirements.txt file. `pip3 install -r requirements.txt`
5. Run the python script. `python3 citrix_logging.py`

_NOTE: The SSO DUO Push should be completed manually within two minutes. The script picks up automatically after the DUO Push completion._

#### Bonus: 
You can set up an alias in you specific shell config and initiate login process from anywhere inside the terminal:
```python
alias citrixlogin='cd /path/where/you/cloned/this/repo; source .venv/bin/activate; python3 citrix_logging.py'
```

