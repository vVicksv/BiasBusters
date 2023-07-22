from typing import Text
import re
import random
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
import ssl
import pickle
from create_mongodb import get_database
from crawler import crawl
from io import BytesIO
from wordcloud import WordCloud

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('punkt')

def tokenize(reviews):
    stopword = stopwords.words('english')
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = []
    for review in reviews:
        # lowercase
        review = review.lower()
        # remove links
        review = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', ' ', review)
        # remove module code
        review = re.sub('^[A-Za-z]{2,4}[0-9]{4,4}[A-Za-z]{0,1}$', ' ', review)
        # remove all stopwords
        review = " ".join(word.lower() for word in str(review).split() if word not in stopword)
        # remove every character and symbols except letters
        review = re.sub('[^A-Za-z]+',' ',review)
        review = re.sub(r'\s+[a-zA-Z]\s+', ' ', review)
        review = re.sub(r'\s+', ' ', review)
        review = " ".join([lemmatizer.lemmatize(x) for x in tokenizer.tokenize(review)])
        tokens.append(review)
    return tokens
        
#get_sentiments Helper Functions
def preprocess(reviews):
    processed = tokenize(reviews)
    with open('tfidf_pkl', 'rb') as file:
        vectorizer = pickle.load(file)
    vectorised_reviews = vectorizer.transform(processed)
    return vectorised_reviews

def maximum(pos, neg):
    if pos >= neg:
        return 'Positive \U0001F601'
    else:
        return 'Negative \U0001F614'

def make_bar(y_axis, module_name):
    x_axis = ["Positive", "Negative"]
    fig = Figure()
    ax = fig.subplots()
    ax.bar(x_axis, y_axis, color=['green', 'red'])
    ax.bar_label(ax.containers[0], fontweight = 'bold')
    fig.suptitle(f"Sentiments Analysis of {module_name}", y=0.93, fontweight = "bold")
    fig.supylabel("Number of Sentiments")
    fig.supxlabel("Sentiment Type")
    fig.savefig("bar.png", bbox_inches='tight')

# checks if mod is in database
def mod_exist(db, name):
    mod = db['modules_coll'].find_one({'name':name})
    return mod is not None

# return list of positive and negative reviews
# if module in database
def retrieve_sentiments(db, name):

    mod = db['modules_coll'].find_one({'name':name})
    
    # retrieve reviews & sentiments from database
    print("fetching records from our database...")
    positivesrev = mod['pos']
    negativesrev = mod['neg']

    return positivesrev, negativesrev

# insert module info into database
def insert_info(db, name, info):
    db['modules_coll'].insert_one({'name':name, 'pos':info['pos'], 'neg':info['neg']})

# if module not in database
def get_sentiments(data, module_name):

    db = get_database()
        
    print('sentiment calculation began..')

    with open('sentiment_analysis_pkl', 'rb') as file:
        model = pickle.load(file)

    processed_reviews = preprocess(data)
    positivesrev, negativesrev = [], []
    counter = 0
    for vec_review in processed_reviews:
        review = data[counter]
        sentiment = model.predict(vec_review)[0]
        counter += 1

        if sentiment == 1:
            positivesrev.append(review)
        elif sentiment == 0:
            negativesrev.append(review)
        
    # insert new module reviews sentiments into database
    info = {'pos': positivesrev, 'neg':negativesrev}
    insert_info(db, module_name, info)

    return positivesrev, negativesrev

def generate_result(positivesrev, negativesrev, module_name, provider):
    
    positives = len(positivesrev)
    negatives = len(negativesrev)
    total = positives + negatives

    text_report= '{0} posts were analyzed... \n\n{1} were classified as being Positive \U0001F601 \n{2} were classified as Negative \U0001F614 \n\nOverall Sentiment: {3}\n\nData Source: {4}'.format(total, positives, negatives,
    maximum(positives, negatives), provider)

    result = [positives, negatives]
    make_bar(result, module_name)

    # print(random.choice(positivesrev))
    print('generating report')

    thisdict = {"text": text_report,"posrev": positivesrev, "negrev": negativesrev}
    print(thisdict["text"])
    return thisdict

#eliminate common words present in both positive & negative wordcloud
def eliminate_shared_words(thisdict):
    pos_tokens = " ".join(thisdict['posrev']).split()
    neg_tokens = " ".join(thisdict['negrev']).split()
    common_words = [word for word in pos_tokens if word in neg_tokens]
    return common_words

#wordcloud generator
def wordcloud(reviews, thisdict):
    # preprocess the reviews and join into one string
    common_words = eliminate_shared_words(thisdict)
    words = " ".join(reviews).split()
    string = " ".join([word for word in words if word not in common_words])
    wordcloud = WordCloud(width=800, height=400).generate(string)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    #plot to image
    image = BytesIO()
    plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    image.seek(0)
    return image

#Getter Functions
def get_msg(thisdict):
    return thisdict["text"]

def get_good(thisdict):
    return random.choice(thisdict["posrev"])

def get_neg(thisdict):
    return random.choice(thisdict["negrev"])