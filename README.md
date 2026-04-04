# Atalho Data

## Build no Windows

1. Crie e ative o ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Instale as dependencias do app e a ferramenta de build:

```powershell
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

3. Gere o executavel:

```powershell
python -m PyInstaller --clean atalho_data.spec
```

## Build automatizada no Windows

Para evitar usar o Python global por engano, rode:

```powershell
.\build.ps1
```

O script:

- usa `venv\Scripts\python.exe`
- instala `requirements.txt`
- instala `pyinstaller`
- executa a build com `atalho_data.spec`
- avisa se `dist\atalho_data.exe` estiver aberto

## Causa do erro `No module named 'keyboard'`

Esse erro acontece quando o projeto e executado ou empacotado com um Python que nao tem as dependencias instaladas. Neste projeto, `keyboard` e `pyperclip` estao em `requirements.txt`, entao a build precisa rodar dentro do `venv`.
