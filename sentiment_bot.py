import os
from dotenv import load_dotenv
import telebot
from crawler import crawl
from analyser import get_sentiments

def run_sentiment_bot():

    load_dotenv()

    # Setting up of BOT
    TELE_TOKEN = os.environ.get('TELE_TOKEN')
    bot = telebot.TeleBot(TELE_TOKEN)

    # Start Command
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "How's it going! \U0001F60A \n\nNice to meet you! I am your very own NUSMOD-erator, here to give you the best insights to the module you're curious about! \U0001F914 \U0001F914 \n\nTo start, simply /evaluate <Module Code> and we'll get started! \U0001FAE1 \U0001FAE1")

    def module_request(message):
        request = message.text.split()
        if len(request) == 2:
            return True
        else:
            return False

    # Evaluate Command
    @bot.message_handler(commands=['evaluate'])
    @bot.message_handler(func=module_request)
    def evaluate(message):
        module = message.text.split(" ")[1]
        try:
            bot.send_message(
                message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
            reviews = crawl(module)
            if len(reviews) == 0:
                bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                return
            else:
                bot.send_message(message.chat.id, "Generating sentiments now...")
                text_report = get_sentiments(reviews, "reddit", module)
                bot.send_photo(message.chat.id, photo=open("bar.png", 'rb'))
                bot.send_message(message.chat.id, text_report)
        except Exception as e:
            bot.reply_to(message.chat.id,
                         "There has been an error. Kindly try again later!")

    # Help Command
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(
            message.chat.id, "Try out Commands like /evaluate! If not you can contact @Viacks or @boonlong for any outstanding issues & Suggestions!")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        pass

    bot.infinity_polling() 
