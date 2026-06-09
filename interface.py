import tkinter as tk
from tkinter import ttk, messagebox

modo_escuro = False

def alternar_tema():
    global modo_escuro

    modo_escuro = not modo_escuro

    if modo_escuro:
        janela.configure(bg="#1e1e1e")
        titulo_app.config(bg="#1e1e1e", fg="white")
        rodape.config(bg="#1e1e1e", fg="lightgray")
        btn_tema.config(text="☀️ Modo Claro")
    else:
        janela.configure(bg="#f0f0f0")
        titulo_app.config(bg="#f0f0f0", fg="black")
        rodape.config(bg="#f0f0f0", fg="gray")
        btn_tema.config(text="🌙 Modo Escuro")

def enviar():
    titulo = entry_titulo.get()
    data = entry_data.get()

    if not titulo or not data:
        messagebox.showwarning(
            "Atenção",
            "Preencha todos os campos!"
        )
        return

    messagebox.showinfo(
        "Sucesso",
        f"Evento '{titulo}' criado!"
    )

# Janela
janela = tk.Tk()
janela.title("Agenda de Eventos")
janela.geometry("500x350")
janela.configure(bg="#f0f0f0")

# Título
titulo_app = tk.Label(
    janela,
    text="📅 Agenda de Eventos",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
)
titulo_app.pack(pady=15)

# Frame
frame = ttk.Frame(janela, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Título do Evento").pack(anchor="w")
entry_titulo = ttk.Entry(frame, width=50)
entry_titulo.pack(pady=5)

ttk.Label(frame, text="Data (AAAA-MM-DD)").pack(anchor="w")
entry_data = ttk.Entry(frame, width=50)
entry_data.pack(pady=5)

ttk.Button(
    frame,
    text="Criar Evento",
    command=enviar
).pack(pady=15)

# Botão tema
btn_tema = tk.Button(
    janela,
    text="🌙 Modo Escuro",
    command=alternar_tema,
    width=20
)
btn_tema.pack(pady=5)

# Rodapé
rodape = tk.Label(
    janela,
    text="Sistema de Agenda v1.0",
    bg="#f0f0f0",
    fg="gray"
)
rodape.pack(side="bottom", pady=10)

janela.mainloop()