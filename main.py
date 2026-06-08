from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import webbrowser

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Login no Google
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

# Conecta ao Google Agenda
service = build('calendar', 'v3', credentials=creds)

# Evento
evento = {
    'summary': 'PROVA',
    'description': 'Levar documento, caneta preta e chegar 30 minutos antes.',
    'start': {
        'date': '2026-06-09'
    },
    'end': {
        'date': '2026-06-10'
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 1440},  # 1 dia antes
            {'method': 'popup', 'minutes': 60}     # 1 hora antes
        ]
    }
}

# Cria o evento
service.events().insert(
    calendarId='primary',
    body=evento
).execute()

print("✅ Evento criado com sucesso!")

# Abre o Google Agenda
webbrowser.open("https://calendar.google.com/calendar/u/0/r")
