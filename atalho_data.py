import keyboard
import pyperclip
from datetime import datetime
import time
import threading
import sys
import os
import ctypes
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

ultimo_valor_monetario = None
clipboard_anterior = ""
config_file = Path(__file__).parent / "config.json"
app_window = None
app_running = True

# Configurações padrão
default_config = {
    "mensagem_template": "{data} - {valor} a ser pago via Mercado Pago. Sougás.",
    "venda_entrega_texto": "venda e entrega de"
}

# Carrega configurações do arquivo ou usa padrão
def load_config():
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default_config.copy()
    return default_config.copy()


# Salva configurações no arquivo
def save_config_to_file(config):
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")


config = load_config()


def monitorar_clipboard():
    global clipboard_anterior, ultimo_valor_monetario

    while app_running:
        try:
            conteudo = pyperclip.paste()

            if conteudo != clipboard_anterior:
                clipboard_anterior = conteudo

                texto = conteudo.strip()
                if texto.startswith("R$"):
                    ultimo_valor_monetario = texto
                    print(f"Valor monetário detectado: {ultimo_valor_monetario}")

        except Exception:
            pass

        time.sleep(0.5)


def colar_mensagem():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    valor = ultimo_valor_monetario or "valor não informado"
    
    template = config.get("mensagem_template", default_config["mensagem_template"])
    mensagem = template.format(data=data_atual, valor=valor)

    pyperclip.copy(mensagem)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")


def colar_venda_entrega():
    texto = config.get("venda_entrega_texto", default_config["venda_entrega_texto"])
    pyperclip.copy(texto)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")


# Classe da interface gráfica
class ConfigWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuração - Atalho Data")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (300)
        y = (self.root.winfo_screenheight() // 2) - (150)
        self.root.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo 1: Mensagem (Ctrl+B)
        ttk.Label(main_frame, text="Mensagem (Ctrl+B):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(main_frame, text="Use {data} e {valor} como variáveis", font=("Arial", 8, "italic")).pack(anchor=tk.W, pady=(0, 5))
        
        self.mensagem_entry = tk.Text(main_frame, height=3, width=70, wrap=tk.WORD, font=("Arial", 9))
        self.mensagem_entry.pack(fill=tk.BOTH, pady=(0, 15))
        self.mensagem_entry.insert(tk.END, config.get("mensagem_template", default_config["mensagem_template"]))
        
        # Campo 2: Texto venda e entrega (Ctrl+I)
        ttk.Label(main_frame, text="Texto Venda e Entrega (Ctrl+I):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.venda_entry = ttk.Entry(main_frame, width=70, font=("Arial", 9))
        self.venda_entry.pack(fill=tk.X, pady=(0, 20))
        self.venda_entry.insert(0, config.get("venda_entrega_texto", default_config["venda_entrega_texto"]))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Salvar", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fechar", command=self.on_closing).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.pack(anchor=tk.W, pady=(10, 0))
    
    def save_config(self):
        global config
        config["mensagem_template"] = self.mensagem_entry.get("1.0", tk.END).strip()
        config["venda_entrega_texto"] = self.venda_entry.get().strip()
        
        save_config_to_file(config)
        self.status_label.config(text="✓ Configurações salvas com sucesso!", foreground="green")
        self.root.after(2000, lambda: self.status_label.config(text=""))
        print("Configurações atualizadas!")
    
    def on_closing(self):
        global app_running
        app_running = False
        self.root.destroy()
        print("Programa encerrado.")
        os._exit(0)


def open_config_window():
    global app_window
    root = tk.Tk()
    app_window = ConfigWindow(root)
    root.mainloop()


def setup_hotkeys():
    """Configura os atalhos de teclado em uma thread separada"""
    # Atalhos
    keyboard.add_hotkey("ctrl+q", colar_mensagem)
    keyboard.add_hotkey("ctrl+y", colar_venda_entrega)
    
    print("Atalhos configurados!")
    print("Ctrl + Q → mensagem com data e valor")
    print("Ctrl + Y → venda e entrega de")
    print()
    
    keyboard.wait()
# Windows: garantir que exista uma janela de console ao rodar como .exe
def _ensure_windows_console():
    if os.name != 'nt':
        return

    kernel32 = ctypes.windll.kernel32
    # Se não houver janela de console, aloca uma
    try:
        if kernel32.GetConsoleWindow() == 0:
            kernel32.AllocConsole()
            sys.stdout = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            sys.stderr = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            sys.stdin = open('CONIN$', 'r', encoding='utf-8')

            # Handler para eventos do console (fechar, CTRL+C, etc.)
            PHANDLER = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

            def _console_handler(ctrl_type):
                global app_running
                try:
                    print('Encerrando pela janela do console...')
                except Exception:
                    pass
                app_running = False
                os._exit(0)
                return True

            handler = PHANDLER(_console_handler)
            kernel32.SetConsoleCtrlHandler(handler, True)
    except Exception:
        # se algo falhar, não impede o funcionamento do app
        pass


# Chama a função para garantir console em Windows
_ensure_windows_console()

# Thread para monitorar o clipboard
thread_clipboard = threading.Thread(target=monitorar_clipboard, daemon=True)
thread_clipboard.start()

# Thread para os atalhos de teclado
thread_hotkeys = threading.Thread(target=setup_hotkeys, daemon=False)
thread_hotkeys.start()

print("Rodando...")
print()

# Abre a UI de configuração na thread principal
open_config_window()
