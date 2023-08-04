python.exe -m pip install --upgrade pip setuptools wheel
python.exe -m pip install -r requirements.txt
if not exist ".\credentials" mkdir .\credentials
@echo MAIN_DC_TOKEN=ABC> credentials\main.env
git rm --cached credentials
python main_bot.py --debug