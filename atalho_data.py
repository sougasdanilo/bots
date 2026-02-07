import keyboard
import pyperclip
from datetime import datetime
import time
import threading
import sys
import os
import ctypes

ultimo_valor_monetario = None
clipboard_anterior = ""

def monitorar_clipboard():
    global clipboard_anterior, ultimo_valor_monetario

    while True:
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

    mensagem = f"{data_atual} - {valor} a ser pago via Mercado Pago. Sougás."

    pyperclip.copy(mensagem)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")


def colar_venda_entrega():
    texto = "venda e entrega de"
    pyperclip.copy(texto)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")


# thread para monitorar o clipboard
thread_clipboard = threading.Thread(target=monitorar_clipboard, daemon=True)
thread_clipboard.start()

# atalhos
keyboard.add_hotkey("ctrl+b", colar_mensagem)
keyboard.add_hotkey("ctrl+i", colar_venda_entrega)

print("Rodando...")
print("Ctrl + B → mensagem com data e valor")
print("Ctrl + I → 'venda e entrega de'")

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
                try:
                    print('Encerrando pela janela do console...')
                except Exception:
                    pass
                os._exit(0)
                return True

            handler = PHANDLER(_console_handler)
            kernel32.SetConsoleCtrlHandler(handler, True)
    except Exception:
        # se algo falhar, não impede o funcionamento do app
        pass


# Chama a função para garantir console em Windows
_ensure_windows_console()
