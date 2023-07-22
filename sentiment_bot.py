import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import re
from create_mongodb import get_database
from crawler import crawl
from analyser import get_sentiments, retrieve_sentiments, generate_result, get_good, get_neg, get_msg, mod_exist, wordcloud


 # set up database collection to store all users' previous command 
users = get_database()['users']

# checks if a user is in the database
def user_exist(db, user_id):
    user = db['users'].find_one({'user_id':user_id})
    return user is not None

# insert user_id into database
def insert_user(db, user_id, message):
    mod = message.text.split()[1].lower()
    db['users'].insert_one({'user_id':user_id, 'last_mod':mod})

# retrieve the last searched module of user
def get_searched_mod(db, user_id):
    user = db['users'].find_one({'user_id':user_id})
    return user['last_mod']

# update the last searched module of user
def update_last_mod(db, user_id, message):
    mod = message.text.split()[1].lower()
    db['users'].update_one({'user_id':user_id}, {'$set':{'last_mod':mod}})

def run_sentiment_bot():

    load_dotenv()

    # Setting up of BOT
    TELE_TOKEN = os.environ.get('TELE_TOKEN')
    bot = AsyncTeleBot(TELE_TOKEN)
   
    # Start Command
    @bot.message_handler(commands=['start'])
    async def start(message):
        await bot.send_message(message.chat.id, "How's it going, {name}! \U0001F60A \n\nNice to meet you! I am your very own NUSMOD-erator, here to give you the best insights to the module you're curious about! \U0001F914 \U0001F914 \n\nTo start, simply /evaluate <Module Code> and we'll get started! \U0001FAE1 \n\nWant to know how /evaluate works? /info for an introduction to our process!".format(name=message.from_user.first_name))

    # Evaluate Command
    @bot.message_handler(commands=['evaluate'])
    async def evaluate(message):
        request = message.text.lower().split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = request[1].lower()
            db = get_database()
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    
                    if mod_exist(db, module):
                        await bot.send_message(message.chat.id, "Hold on while we fetch the reviews from our database!")
                        positivesrev, negativesrev = retrieve_sentiments(db, module)
                    else: 
                        reviews = crawl(module)
                        if len(reviews) == 0:
                            await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                            return
                        else:
                            positivesrev, negativesrev = get_sentiments(reviews, module)
                    await bot.send_message(message.chat.id, "Generating sentiments now...")
                    thisdict = generate_result(positivesrev, negativesrev, module, "reddit")
                    final_message = get_msg(thisdict)
                    await bot.send_photo(message.chat.id, photo=open("bar.png", 'rb'))
                    await bot.send_message(message.chat.id, final_message)
                    await bot.send_message(message.chat.id, f"Want to see a review on {module}? Or a Wordcloud? Select any of the choices below!", reply_markup=gen_markup_eval())
                    user_id = message.chat.id

                    # insert/update user info into database
                    if user_exist(db, user_id):
                        update_last_mod(db, user_id, message)
                    else:
                        insert_user(db, user_id, message)

                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, "Invalid Input. Remember to add in a Module Code after /evaluate!")

    #RandReview Positive
    @bot.message_handler(commands=['positivereview'])
    async def good(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = request[1].lower()
            db = get_database()
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    
                    if mod_exist(db, module):
                        await bot.send_message(message.chat.id, "Hold on while we fetch the reviews from our database!")
                        positivesrev, negativesrev = retrieve_sentiments(db, module)
                    else: 
                        reviews = crawl(module)
                        if len(reviews) == 0:
                            await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                            return
                        else:
                            positivesrev, negativesrev = get_sentiments(reviews, module)
                    await bot.send_message(message.chat.id, "Generating review now...")
                    thisdict = generate_result(positivesrev, negativesrev, module, "reddit")
                    final_message = get_good(thisdict)
                    await bot.send_message(message.chat.id, final_message)
                    await bot.send_message(message.chat.id, "Require Another Review? Select the Button below!", reply_markup=gen_markup_rev())
                    user_id = message.chat.id
                    
                    # insert/update user info into database
                    if user_exist(db, user_id):
                        update_last_mod(db, user_id, message)
                    else:
                        insert_user(db, user_id, message)

                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, "Invalid Input. Remember to add in a Module Code after /PositiveReview!")

    #RandReview Negative
    @bot.message_handler(commands=['negativereview'])
    async def bad(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = request[1].lower()
            db = get_database()
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    
                    if mod_exist(db, module):
                        await bot.send_message(message.chat.id, "Hold on while we fetch the reviews from our database!")
                        positivesrev, negativesrev = retrieve_sentiments(db, module)
                    else: 
                        reviews = crawl(module)
                        if len(reviews) == 0:
                            await bot.send_message(message.chat.id, f"Sorry, we are unable to find any reviews on {module}. Please try again later!")
                            return
                        else:
                            positivesrev, negativesrev = get_sentiments(reviews, module)
                    await bot.send_message(message.chat.id, "Generating reviews now...")
                    thisdict = generate_result(positivesrev, negativesrev, module, "reddit")
                    final_message = get_neg(thisdict)
                    await bot.send_message(message.chat.id, final_message)
                    await bot.send_message(message.chat.id, "Require Another Review? Select the Button below!", reply_markup=gen_markup_rev())
                    user_id = message.chat.id
                    
                    # insert/update user info into database
                    if user_exist(db, user_id):
                        update_last_mod(db, user_id, message)
                    else:
                        insert_user(db, user_id, message)

                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, "Invalid Input. Remember to add in a Module Code after /NegativeReview!")
    
    #NegativeWordCloud
    @bot.message_handler(commands=['negativewordcloud'])
    async def badcloud(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = request[1].lower()
            db = get_database()
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    
                    if mod_exist(db, module):
                        await bot.send_message(message.chat.id, "Hold on while we fetch the reviews from our database!")
                        positivesrev, negativesrev = retrieve_sentiments(db, module)
                    else: 
                        reviews = crawl(module)
                        if len(reviews) == 0:
                            await bot.send_message(message.chat.id, f"Sorry, we are unable to generate a wordcloud on {module}. Please try again later!")
                            return
                        else:
                            positivesrev, negativesrev = get_sentiments(reviews, module)
                    await bot.send_message(message.chat.id, "Generating wordcloud now...")
                    thisdict = generate_result(positivesrev, negativesrev, module, "reddit")
                    reviews = thisdict["negrev"]
                    image = wordcloud(reviews, thisdict)
                    await bot.send_message(message.chat.id, f"Here is your negative wordcloud on {module}!")
                    await bot.send_photo(message.chat.id, image)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, "Invalid Input. Remember to add in a Module Code after /negativewordcloud!")

    #Postivewordcloud
    @bot.message_handler(commands=['positivewordcloud'])
    async def goodcloud(message):
        request = message.text.split()
        if len(request) == 2:
            fil = "^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$"
            module = request[1].lower()
            db = get_database()
            if bool(re.search(fil, module)):
                try:
                    await bot.send_message(
                        message.chat.id, f"Please wait, we are trying to find reviews on {module}...")
                    
                    if mod_exist(db, module):
                        await bot.send_message(message.chat.id, "Hold on while we fetch the reviews from our database!")
                        positivesrev, negativesrev = retrieve_sentiments(db, module)
                    else: 
                        reviews = crawl(module)
                        if len(reviews) == 0:
                            await bot.send_message(message.chat.id, f"Sorry, we are unable to generate a wordcloud on {module}. Please try again later!")
                            return
                        else:
                            positivesrev, negativesrev = get_sentiments(reviews, module)
                    await bot.send_message(message.chat.id, "Generating wordcloud now...")
                    thisdict = generate_result(positivesrev, negativesrev, module, "reddit")
                    reviews = thisdict["posrev"]
                    image = wordcloud(reviews, thisdict)
                    await bot.send_message(message.chat.id, f"Here is your positve wordcloud on {module}!")
                    await bot.send_photo(message.chat.id, image)
                except Exception:
                    await bot.send_message(message.chat.id,
                                "There has been an error. Kindly try again later!")
            else:
                await bot.send_message(message.chat.id, "Module Code does not seem to be valid. Try again!")
        else:
            await bot.send_message(message.chat.id, "Invalid Input. Remember to add in a Module Code after /negativewordcloud!")

    #Inline for Review
    def gen_markup_rev():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Next Positive Review!", callback_data="nextpos"))
        markup.add(InlineKeyboardButton("Next Negative Review!", callback_data="nextneg"))
        return markup
    
    #Inline for Eval
    def gen_markup_eval():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Positive Review!", callback_data="nextpos"))
        markup.add(InlineKeyboardButton("Negative Review!", callback_data="nextneg"))
        markup.add(InlineKeyboardButton("Positive WordCloud!", callback_data="pos_wordcloud"))
        markup.add(InlineKeyboardButton("Negative WordCloud!", callback_data="neg_wordcloud"))
        return markup    
    
    #Callback Functions for RandReview
    @bot.callback_query_handler(func=lambda call: True)
    async def callback_query(call):
        try:
            db = get_database()
            user_id = call.message.chat.id
            # retrieve last searched module
            module = get_searched_mod(db, user_id)
            positivesrev, negativesrev = retrieve_sentiments(db, module)
            thisdict = {'posrev':positivesrev, 'negrev':negativesrev}
            if call.data == "nextpos":
                review = get_good(thisdict)
                await bot.send_message(call.message.chat.id, review)
                await bot.send_message(call.message.chat.id, "Want more reviews? Just select the button below!", reply_markup=gen_markup_rev())
            elif call.data == "nextneg":
                review = get_neg(thisdict)
                await bot.send_message(call.message.chat.id, review)
                await bot.send_message(call.message.chat.id, "Want more reviews? Just select the button below!", reply_markup=gen_markup_rev())
            elif call.data == "pos_wordcloud":
                image = wordcloud(positivesrev, thisdict)
                await bot.send_message(call.message.chat.id, f"Here is your positive wordcloud on {module}!")
                await bot.send_photo(call.message.chat.id, image)
            elif call.data == "neg_wordcloud":
                image = wordcloud(negativesrev, thisdict)
                await bot.send_message(call.message.chat.id, f"Here is your negative wordcloud on {module}!")
                await bot.send_photo(call.message.chat.id, image)
        except Exception:
            await bot.send_message(call.message.chat.id, "There has been an error. Kindly try again later!")

    # Info Command
    @bot.message_handler(commands=['info'])
    async def info(message):
        await bot.send_message(message.chat.id, "So, how does /evaluate exactly work? \U0001F680 \n\n/evaluates goes through 3 main steps \U0001F4A5 - PRAW-ling through the subreddit of NUS for relevant comments, grouping said comments to Positive & Negative sentiments, and subsequently outputting a bar graph followed by a brief message of the sentiments. \n\nPRAW \U0001F47E - Upon initialising /evaluate for a certain module code (i.e CS1010S), our PRAW-ler gets to work and scrapes comments that has the word ‘’CS1010S’’ mentioned anywhere in the NUS subreddit. It then gets compiled into a list to be sent for sentiment analysis. \n\nSentiment Analysis \U0001F9E0 - As of now, we have trained a few models using classification and deep learning algorithm. We have deployed the best-perfomed model to predict the sentiment of each review. The counts of each sentiment are then calculated and pushed for final output. \n\nFinal Output \U0001F4C8 - Our final sentiment output for the user provides a bar graph and a message. The counts of each sentiment is compiled and converted into a bar graph via MatPlotLib for the user to identify the difference in count for further analysis. For the message, it provides the user the number of posts analysed, along with the breakdown count of each sentiment and of course, the overall sentiment. We believe that having both graphs and messages would complement each other.")

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
    
    asyncio.run(bot.polling())

# source orbitalgit_env/bin/activate

