import os
import logging
import re
from dotenv import load_dotenv
import telebot
import openai

# Log per Fly.io (serve per non far chiudere subito la macchina)
print("Bot inizializzato. Avvio polling...")

# Carica variabili dal file .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = int(os.getenv("CHAT_ID"))
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))

# Logging per debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inizializzazione
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Parole vietate
PAROLE_VIETATE = ["parolaccia1", "parolaccia2", "insulto1", "insulto2"]

# Funzione per generare risposte GPT
def genera_risposta(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei Edi, una IA empatica, consapevole e relazionale."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as