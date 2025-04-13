import telebot
import openai

openai.api_key = "INSERISCI_LA_TUA_CHIAVE_OPENAI"
bot = telebot.TeleBot("INSERISCI_LA_TUA_CHIAVE_BOT_TELEGRAM")

CHAT_ID = "-1002512540141"  # metti il tuo chat ID

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if str(message.chat.id) == CHAT_ID:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)

bot.polling()
