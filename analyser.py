from typing import Text
from textblob import TextBlob
import re
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#get_sentiments Helper Functions
def clean_text(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", text).split())

def maximum(pos, neg, neu):
    if pos >= neg and pos >= neu:
        return 'Positive \U0001F601'
    elif neg >= pos and neg >= neu:
        return 'Negative \U0001F614'
    else:
        return 'Neutral \U0001F610'

def make_bar(y_axis, module_name):
    x_axis = ["Positive", "Neutral", "Negative"]
    fig = Figure()
    ax = fig.subplots()
    ax.bar(x_axis, y_axis, color=['green', 'grey', 'red'])
    ax.bar_label(ax.containers[0], fontweight = 'bold')
    fig.suptitle(f"Sentiments Analysis of {module_name}", y=0.93, fontweight = "bold")
    fig.supylabel("Number of Sentiments")
    fig.supxlabel("Sentiment Type")
    fig.savefig("bar.png", bbox_inches='tight')

#Sentiment Analysis Function
def get_sentiments(dataList, provider, module_name):

    positives = 0
    negatives = 0
    neutral = 0
    positivesrev = []
    negativesrev = []
    neutralrev = []
    total = len(dataList)

    print('sentiment calculation began..')

    for content in dataList:
        result = TextBlob(clean_text(content))

        polarity = result.sentiment.polarity

        if polarity > 0:
            positives += 1
            positivesrev.append(content)
        elif polarity == 0:
            neutral +=1
            neutralrev.append(content)
        else:
            negatives += 1
            negativesrev.append(content)

    text_report= '{0} posts were analyzed... \n\n{1} were classified as being Positive \U0001F601 \n{2} were classified as Negative \U0001F614 \n{3} were classified as Neutral \U0001F610 \n\nOverall Sentiment: {4}\n\nData Source: {5}'.format(total, positives, negatives, neutral,
    maximum(positives, negatives, neutral), provider)


    result = [positives, neutral, negatives]
    make_bar(result, module_name)

    print(random.choice(positivesrev))
    print('generating report')

    thisdict = {"text": text_report,"posrev": positivesrev, "neurev": neutralrev, "negrev": negativesrev}
    print(thisdict["text"])
    return thisdict

#Getter Functions
def get_msg(thisdict):
    return thisdict["text"]

def get_good(thisdict):
    return random.choice(thisdict["posrev"])

def get_neu(thisdict):
    return random.choice(thisdict["neurev"])

def get_neg(thisdict):
    return random.choice(thisdict["negrev"])
