python -m venv venv
venv\Scripts\activate

python3 -m venv venv
source venv/bin/activate

pyinstaller --onefile --noconsole atalho_data.py
