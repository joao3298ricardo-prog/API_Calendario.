import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import webbrowser

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ==========================
# GOOGLE CALENDAR
# ==========================

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build(
    'calendar',
    'v3',
    credentials=creds
)

# ==========================
# TEMA
# ==========================

modo_escuro = False

def alternar_tema():
    global modo_escuro

    modo_escuro = not modo_escuro

    if modo_escuro:

        janela.configure(bg="#1e1e1e")

        titulo.config(
            bg="#1e1e1e",
            fg="white"
        )

        rodape.config(
            bg="#1e1e1e",
            fg="lightgray"
        )

        descricao.config(
            bg="#2d2d2d",
            fg="white",
            insertbackground="white"
        )

        btn_tema.config(
            text="☀️ Modo Claro",
            bg="#2d2d2d",
            fg="white"
        )

        btn_criar.config(
            bg="#2e7d32",
            fg="white"
        )

    else:

        janela.configure(bg="#f0f0f0")

        titulo.config(
            bg="#f0f0f0",
            fg="black"
        )

        rodape.config(
            bg="#f0f0f0",
            fg="gray"
        )

        descricao.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        btn_tema.config(
            text="🌙 Modo Escuro",
            bg="SystemButtonFace",
            fg="black"
        )

        btn_criar.config(
            bg="#4CAF50",
            fg="white"
        )

# ==========================
# TROCAR IDIOMA
# ==========================

def trocar_idioma(event=None):

    idioma = combo_idioma.get()

    if idioma == "Português":
        calendario.configure(locale="pt_BR")
    else:
        calendario.configure(locale="en_US")

# ==========================
# CRIAR EVENTO
# ==========================

def criar_evento():

    titulo_evento = entry_titulo.get().strip()
    descricao_evento = descricao.get("1.0", tk.END).strip()

    if not titulo_evento:
        messagebox.showerror(
            "Erro",
            "Digite um título para o evento."
        )
        return

    try:

        data_evento = calendario.get_date()

        hora = combo_hora.get()
        minuto = combo_minuto.get()

        data_hora_inicio = datetime.strptime(
            f"{data_evento.strftime('%Y-%m-%d')} {hora}:{minuto}",
            "%Y-%m-%d %H:%M"
        )

        data_hora_fim = data_hora_inicio + timedelta(hours=1)

        evento = {
            'summary': titulo_evento,
            'description': descricao_evento,

            'start': {
                'dateTime': data_hora_inicio.isoformat(),
                'timeZone': 'America/Sao_Paulo'
            },

            'end': {
                'dateTime': data_hora_fim.isoformat(),
                'timeZone': 'America/Sao_Paulo'
            },

            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 1440},
                    {'method': 'popup', 'minutes': 60}
                ]
            }
        }

        service.events().insert(
            calendarId='primary',
            body=evento
        ).execute()

        messagebox.showinfo(
            "Sucesso",
            f"Evento '{titulo_evento}' criado!"
        )

        entry_titulo.delete(0, tk.END)
        descricao.delete("1.0", tk.END)

        webbrowser.open(
            "https://calendar.google.com"
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )

# ==========================
# JANELA
# ==========================

janela = tk.Tk()

janela.title("Agenda Google")
janela.geometry("700x650")
janela.resizable(False, False)
janela.configure(bg="#f0f0f0")

titulo = tk.Label(
    janela,
    text="📅 Agenda Google",
    font=("Arial", 22, "bold"),
    bg="#f0f0f0"
)

titulo.pack(pady=15)

frame = ttk.Frame(
    janela,
    padding=20
)

frame.pack(fill="both", expand=True)
# ==========================
# TÍTULO EVENTO
# ==========================

ttk.Label(
    frame,
    text="Título do Evento"
).pack(anchor="w")

entry_titulo = ttk.Entry(
    frame,
    width=60
)

entry_titulo.pack(pady=5)

# ==========================
# IDIOMA
# ==========================

ttk.Label(
    frame,
    text="Idioma do Calendário"
).pack(anchor="w", pady=(10, 0))

combo_idioma = ttk.Combobox(
    frame,
    values=["Português", "English"],
    state="readonly",
    width=20
)

combo_idioma.pack(
    anchor="w",
    pady=5
)

combo_idioma.current(0)

# ==========================
# CALENDÁRIO
# ==========================

ttk.Label(
    frame,
    text="Selecione a Data"
).pack(anchor="w")

calendario = DateEntry(
    frame,
    width=20,
    locale="pt_BR",
    date_pattern="dd/MM/yyyy"
)

calendario.pack(
    anchor="w",
    pady=5
)

combo_idioma.bind(
    "<<ComboboxSelected>>",
    trocar_idioma
)

# ==========================
# HORÁRIO
# ==========================

ttk.Label(
    frame,
    text="Horário do Evento"
).pack(anchor="w", pady=(10, 0))

frame_hora = ttk.Frame(frame)
frame_hora.pack(anchor="w", pady=5)

hora_var = tk.StringVar(value="08")
minuto_var = tk.StringVar(value="00")

combo_hora = ttk.Combobox(
    frame_hora,
    values=[f"{i:02d}" for i in range(24)],
    textvariable=hora_var,
    width=5,
    state="readonly"
)

combo_hora.pack(side="left")

ttk.Label(
    frame_hora,
    text=":"
).pack(side="left")

combo_minuto = ttk.Combobox(
    frame_hora,
    values=[f"{i:02d}" for i in range(60)],
    textvariable=minuto_var,
    width=5,
    state="readonly"
)

combo_minuto.pack(side="left")

# ==========================
# DESCRIÇÃO
# ==========================

ttk.Label(
    frame,
    text="Descrição"
).pack(anchor="w", pady=(15, 0))

descricao = tk.Text(
    frame,
    width=70,
    height=10
)

descricao.pack(pady=5)

# ==========================
# BOTÃO CRIAR
# ==========================

btn_criar = tk.Button(
    frame,
    text="📌 Criar Evento",
    font=("Arial", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    width=25,
    command=criar_evento
)

btn_criar.pack(pady=20)

# ==========================
# MODO ESCURO
# ==========================

btn_tema = tk.Button(
    janela,
    text="🌙 Modo Escuro",
    width=20,
    command=alternar_tema
)

btn_tema.pack(pady=5)

# ==========================
# RODAPÉ
# ==========================

rodape = tk.Label(
    janela,
    text="Sistema Agenda Google v4.0",
    bg="#7b0dd4",
    fg="gray"
)

rodape.pack(side="bottom", pady=10)

janela.mainloop()
webbrowser.open("https://calendar.google.com/calendar/u/0/r")
