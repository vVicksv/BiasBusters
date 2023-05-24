import os 
import telebot
#from dotenv import load_dotenv
#load_dotenv()
#from reddit_crawler import get_data
#from sentiment_analyzer import get_sentiments

#Setting up of BOT
bot = telebot.TeleBot('5891415447:AAHZ_7D6qQpKNovPLbxhi-F6vmLZ75mlrmA')

#Start Command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "How's it going! \U0001F60A \n\nNice to meet you! I am your very own NUSMOD-erator, here to give you the best insights to the module you're curious about! \U0001F914 \U0001F914 \n\nTo start, simply /evaluate <Module Code> and we'll get started! \U0001FAE1 \U0001FAE1") 

#Evaluate Command
@bot.message_handler(commands=['evaluate'])
def evaluate(message):
    bot.send_message(message.chat.id, "Work In Progress, Check back later!")
    #Boon

#Help Command
@bot.message_handler(commands=['help'])
def help(message):
     bot.send_message(message.chat.id, "Try out Commands like /evaluate! If not you can contact @Viacks or @Boonlong for any outstanding issues & Suggestions!")

#Invalid Command Handling
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'Invalid Command, try /start!')

bot.infinity_polling()

