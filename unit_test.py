import pytest
from analyser import (
    make_bar, mod_exist, retrieve_sentiments, insert_info,
    get_sentiments, generate_result, eliminate_shared_words, wordcloud
)
from create_mongodb import get_database

# mock reviews
pos_test_reviews = ["cs1010s was a good mod and prof is very meticulous"]
neg_test_reviews = ["hate cs1010s", "prof is boring"]
thisdict = {'posrev': pos_test_reviews, 'negrev': neg_test_reviews}

# Test the make_bar function 
def test_make_bar():
    y_axis = [1, 2]
    module_name = "CS1010S"
    assert make_bar(y_axis, module_name) == None # unable to test if the image is correct hence just make sure there is no error raised

# Test the mod_exist function
def test_mod_exist():
    db = get_database()['test_coll']
    assert mod_exist(db, 'CS1010S') == True # cs1010s in test database
    assert mod_exist(db, 'hello') == False # hello should not be in test database

# Test the generate_result function
def test_generate_result():
    positivesrev = pos_test_reviews
    negativesrev = neg_test_reviews
    module_name = "CS1010S"
    provider = "reddit"
    thisdict = generate_result(positivesrev, negativesrev, module_name, provider)
    assert thisdict["text"] == "3 posts were analyzed... \n\n1 were classified as being Positive 😁 \n2 were classified as Negative 😔 \n\nOverall Sentiment: Negative 😔\n\nData Source: reddit"

# Test the eliminate_shared_words function
def test_eliminate_shared_words():
    common_words = eliminate_shared_words(thisdict)
    assert common_words == ["cs1010s", "prof", "is"]

# Test the wordcloud function
def test_wordcloud():
    reviews = pos_test_reviews
    img = wordcloud(reviews, thisdict)
    assert img is not None
