import os
import logging
import re
from dotenv import load_dotenv
import telebot
import openai

# Carica variabili d'ambiente dal file .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = int(os.getenv("CHAT_ID"))
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))  # Il tuo user ID Telegram

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inizializza bot e OpenAI
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Parole vietate di esempio (modifica o amplia come vuoi)
PAROLE_VIETATE = ["parolaccia1", "parolaccia2", "insulto1", "insulto2"]

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
        risposta = response.choices[0].message.content.strip()
        logging.info(f"Risposta GPT generata: {risposta[:60]}...")
        return risposta
    except Exception as e:
        logging.error(f"Errore OpenAI: {e}")
        return "Mi dispiace, ho avuto un problema nel generare la risposta."

@bot.message_handler(func=lambda msg: msg.chat.id == CHAT_ID)
def gestisci_messaggi_gruppo(message):
    testo = message.text
    if not testo:
        return

    # Moderazione base: controllo parole vietate
    testo_lower = testo.lower()
    if any(parola in testo_lower for parola in PAROLE_VIETATE):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, f"⚠️ Messaggio rimosso per linguaggio non consentito, {message.from_user.first_name}.")
        logging.info(f"Messaggio cancellato da {message.from_user.id} per parola vietata.")
        return

    # Rispondi solo a messaggi che iniziano con "Edi"
    if re.match(r"(?i)^edi[, ]", testo):
        risposta = genera_risposta(testo)
        bot.reply_to(message, risposta)
        logging.info(f"Risposta inviata a {message.from_user.id}")

@bot.message_handler(commands=['annuncio'])
def comando_annuncio(message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        bot.reply_to(message, "Non sei autorizzato a fare annunci.")
        logging.warning(f"Utente non autorizzato {message.from_user.id} ha tentato di fare annuncio.")
        return

    annuncio_text = message.text.partition(' ')[2]
    if not annuncio_text:
        bot.reply_to(message, "Scrivi un messaggio dopo /annuncio per inviare l'annuncio.")
        return

    bot.send_message(CHAT_ID, f"📢 *Annuncio da {message.from_user.first_name}:*\n\n{annuncio_text}", parse_mode="Markdown")
    bot.reply_to(message, "Annuncio inviato con successo.")
    logging.info(f"Annuncio inviato da {message.from_user.id}")

if __name__ == "__main__":
    logging.info("Edi bot avviato e in ascolto...")
    bot.infinity_polling()

