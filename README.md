python -m venv venv
venv\Scripts\activate

python3 -m venv venv
source venv/bin/activate

python -m pip install pyinstaller

pyinstaller --onefile --noconsole atalho_data.py