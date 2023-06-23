import os
from dotenv import load_dotenv
from crawler import crawl
from analyser import get_sentiments
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def run_sentiment_bot():

    load_dotenv()

    # Setting up of BOT
    TELE_TOKEN = os.environ.get('TELE_TOKEN')
    bot = telebot.TeleBot(TELE_TOKEN)

    # Start Command
    @bot.message_handler(commands=['start'])
    async def start(message):
        await bot.send_message(message.chat.id, "How's it going, {name}! \U0001F60A \n\nNice to meet you! I am your very own NUSMOD-erator, here to give you the best insights to the module you're curious about! \U0001F914 \U0001F914 \n\nTo start, simply /evaluate <Module Code> and we'll get started! \U0001FAE1 \n\nWant to know how /evaluate works? /info for an introduction to our process!".format(name=message.from_user.first_name))

    # Evaluate Command
    @bot.message_handler(commands=['evaluate'])
    async def evaluate(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = message.text.split(" ")[1]
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    reviews = crawl(module)
                    if len(reviews) == 0:
                        await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                        return
                    else:
                        await bot.send_message(message.chat.id, "Generating sentiments now...")
                        thisdict = get_sentiments(reviews, "Reddit", module)
                        final_message = get_msg(thisdict)
                        await bot.send_photo(message.chat.id, photo=open("bar.png", 'rb'))
                        await bot.send_message(message.chat.id, final_message)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, f"Invalid Input. Remember to add in a Module Code after /evaluate!")

    #RandReview Positive
    @bot.message_handler(commands=['PositiveReview'])
    async def good(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = message.text.split(" ")[1]
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find a random positive review on {module}...")
                    reviews = crawl(module)
                    if len(reviews) == 0:
                        await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                        return
                    else:
                        await bot.send_message(message.chat.id, "Generating positive review now...")
                        thisdict = get_sentiments(reviews, "Reddit", module)
                        final_message = get_good(thisdict)
                        await bot.send_message(message.chat.id, final_message)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, f"Invalid Input. Remember to add in a Module Code after /PositiveReview!")

    #RandReview Neutral
    @bot.message_handler(commands=['NeutralReview'])
    async def neu(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = message.text.split(" ")[1]
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find a random neutral review on {module}...")
                    reviews = crawl(module)
                    if len(reviews) == 0:
                        await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                        return
                    else:
                        await bot.send_message(message.chat.id, "Generating neutral review now...")
                        thisdict = get_sentiments(reviews, "Reddit", module)
                        final_message = get_neu(thisdict)
                        await bot.send_message(message.chat.id, final_message)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, f"Invalid Input. Remember to add in a Module Code after /NeutralReview!")

    #RandReview Negative
    @bot.message_handler(commands=['NegativeReview'])
    async def bad(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = message.text.split(" ")[1]
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find a random negative review on {module}...")
                    reviews = crawl(module)
                    if len(reviews) == 0:
                        await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                        return
                    else:
                        await bot.send_message(message.chat.id, "Generating review now...")
                        thisdict = get_sentiments(reviews, "Reddit", module)
                        final_message = get_good(thisdict)
                        await bot.send_message(message.chat.id, final_message)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, f"Invalid Input. Remember to add in a Module Code after /NegativeReview!")

    # Info Command
    @bot.message_handler(commands=['info'])
    async def info(message):
        await bot.send_message(message.chat.id, "So, how does /evaluate exactly work? \U0001F680 \n\n/evaluates goes through 3 main steps \U0001F4A5 - PRAW-ling through the subreddit of NUS for relevant comments, grouping said comments to Positive, Negative & Neutral sentiments, and subsequently outputting a bar graph followed by a brief message of the sentiments. \n\nPRAW \U0001F47E - Upon initialising /evaluate for a certain module code (i.e CS1010S), our PRAW-ler gets to work and scrapes comments that has the word ‘’CS1010S’’ mentioned anywhere in the NUS subreddit. It then gets compiled into a list to be sent for sentiment analysis. \n\nSentiment Analysis \U0001F9E0 - As of now, we are using Textblob, a pre-trained ML model, which helps to calculate a sentence’s polarity through a scoring system. We are thus able to use the scoring system to group them into what the model deems to be Positive, Neutral & Negative comments. The counts of each sentiment are then calculated and pushed for final output. \n\nFinal Output \U0001F4C8 - Our final sentiment output for the user provides a bar graph and a message. The counts of each sentiment is compiled and converted into a bar graph via MatPlotLib for the user to identify the difference in count for further analysis. For the message, it provides the user the number of posts analysed, along with the breakdown count of each sentiment and of course, the overall sentiment. We believe that having both graphs and messages would complement each other.")

    #QnA InlineKeyboard (/troubleshoot)
    def gen_markup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("No Graph Output", callback_data="graph"), InlineKeyboardButton("No Reviews", callback_data="review"), InlineKeyboardButton("Nothing Happens after /evaluate", callback_data="evaluate"), InlineKeyboardButton("Others", callback_data="others"))
        return markup

    @bot.callback_query_handler(func=lambda call: True)
    async def callback_query(call):
        if call.data == "graph":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="In most scenarios when you're unable to have a bar chart for your output, it is highly likely that an error has happend that isn't within your control. \n\nContact @Viacks or @boonlong if it happens after trying again!")
        elif call.data == "review":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Got a message saying that there are no reviews for your requested module? It is likely that there is no mention of your requested module in the NUS subreddit. As such, there would be nothing to analyse. \n\nWe understand that may be an issue for less popular modules and are looking into adding additional module review sites so stay tuned for that! For now, you can try another module and see if it works!")
        elif call.data == "evaluate":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="When nothing happens after /evaluate, there may be a couple possibilites. \n\n1. Someone else may be using the bot for /evaluate. Try waiting for 3-5 minutes without repeating the command and see if it works. We understand that the bot should be running concurrently for each unique user and are looking into running this bot asynchronously. Please give us awhile! \n\n2. The bot may be down for further improvements. You can contact @Viacks or @boonlong for further enquiries or urgent testing!")
        elif call.data == "others":
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Contact @Viacks or @boonlong for any other issues you're facing!")

    @bot.message_handler(commands=['troubleshoot'])
    async def message_handler(message):
        await bot.send_message(message.chat.id, "Require troubleshooting? Select one of the issues you're facing below!", reply_markup=gen_markup())

    #Invalid Command Handling
    @bot.message_handler(func=lambda message: True)
    async def echo_all(message):
	    await bot.send_message(message.chat.id, 'Invalid Command, try /start!')

    import asyncio
    asyncio.run(bot.polling())
