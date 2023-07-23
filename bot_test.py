import pytest
import telebot
from sentiment_bot import start, evaluate, good, goodcloud, info, message_handler
from telebot.types import Message
from unittest.mock import AsyncMock

bot=AsyncMock()

# /start sends a response
@pytest.mark.asyncio
async def test_start_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=123456789, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False
            ),
        text="/start",
        content_type="text",
        options={},
        json_string={}
    )
    await start(message)
    expected_response = "How's it going, John! \U0001F60A \n\nNice to meet you! I am your very own NUSMOD-erator, here to give you the best insights to the module you're curious about! \U0001F914 \U0001F914 \n\nTo start, simply /evaluate <Module Code> and we'll get started! \U0001FAE1 \n\nWant to know how /evaluate works? /info for an introduction to our process!"
    assert bot.send_message == expected_response

# /evaluate with valid module code that is inside database
@pytest.mark.asyncio
async def test_evaluate_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/evaluate cs1010s",
        content_type="text",
        options={},
        json_string={},
    )

    await evaluate(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Please wait, we are trying to find reviews on cs1010s...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Hold on while we fetch the reviews from our database!")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Generating sentiments now...")
    bot.send_photo.assert_called_once()

# /evaluate with valid module code that is NOT inside database
@pytest.mark.asyncio
async def test_evaluate2_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/evaluate is2218",
        content_type="text",
        options={},
        json_string={},
    )
    await evaluate(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Please wait, we are trying to find reviews on is2218...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Generating sentiments now...")
    bot.send_photo.assert_called_once()
    

# /evaluate with no input
@pytest.mark.asyncio
async def test_evaluate3_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/evaluate",
        content_type="text",
        options={},
        json_string={},
    )
    await evaluate(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Invalid Input. Remember to add in a Module Code after /evaluate!")

# /evaluate with invalid module code
@pytest.mark.asyncio
async def test_evaluate4_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/evaluate abc123",
        content_type="text",
        options={},
        json_string={},
    )
    await evaluate(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Module Code does not seem to be valid. Try again!")

# /positivereview with valid module code inside database
@pytest.mark.asyncio
async def test_positivereview_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/positivereview cs1010s",
        content_type="text",
        options={},
        json_string={},
    )
    await good(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Please wait, we are trying to find reviews on cs1010s...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Hold on while we fetch the reviews from our database!")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Generating reviews now...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Want more reviews? Just select the button below!")

# /positivewordcloud with valid module code inside database
@pytest.mark.asyncio
async def test_positivewordcloud_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/positivewordcloud cs1010s",
        content_type="text",
        options={},
        json_string={},
    )
    await goodcloud(message)
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Please wait, we are trying to find reviews on cs1010s...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Hold on while we fetch the reviews from our database!")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Generating wordcloud now...")
    bot.send_message.assert_called_once_with(message.chat.id,
                                             "Here is your positve wordcloud on cs1010s!")
    bot.send_photo.assert_called_once()

# /info sends a correct response
@pytest.mark.asyncio
async def test_info_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/info",
        content_type="text",
        options={},
        json_string={},
    )
    await info(message)
    expected_response = "So, how does /evaluate exactly work? \U0001F680 \n\n/evaluates goes through 3 main steps \U0001F4A5 - PRAW-ling through the subreddit of NUS for relevant comments, grouping said comments to Positive & Negative sentiments, and subsequently outputting a bar graph followed by a brief message of the sentiments. \n\nPRAW \U0001F47E - Upon initialising /evaluate for a certain module code (i.e CS1010S), our PRAW-ler gets to work and scrapes comments that has the word ‘’CS1010S’’ mentioned anywhere in the NUS subreddit. It then gets compiled into a list to be sent for sentiment analysis. \n\nSentiment Analysis \U0001F9E0 - As of now, we have trained a few models using classification and deep learning algorithm. We have deployed the best-perfomed model to predict the sentiment of each review. The counts of each sentiment are then calculated and pushed for final output. \n\nFinal Output \U0001F4C8 - Our final sentiment output for the user provides a bar graph and a message. The counts of each sentiment is compiled and converted into a bar graph via MatPlotLib for the user to identify the difference in count for further analysis. For the message, it provides the user the number of posts analysed, along with the breakdown count of each sentiment and of course, the overall sentiment. We believe that having both graphs and messages would complement each other."
    assert bot.send_message == expected_response

# /troubleshoot sends a correct response
@pytest.mark.asyncio
async def test_troubleshoot_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="/troubleshoot",
        content_type="text",
        options={},
        json_string={},
    )
    await message_handler(message)
    expected_response = "Require troubleshooting? Select one of the issues you're facing below!"
    assert bot.send_message == expected_response

# invalid command handling
@pytest.mark.asyncio
async def test_troubleshoot_command_handler():
    message = Message(
        message_id=123,
        date=1234567890,
        chat=telebot.types.Chat(id=1498424748, type="private"),
        from_user=telebot.types.User(
            id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_bot=False,
            ),
        text="hello",
        content_type="text",
        options={},
        json_string={},
    )
    await message_handler(message)
    expected_response = "Invalid Command, try /start!"
    assert bot.send_message == expected_response
