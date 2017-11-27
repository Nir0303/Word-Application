import json
import urllib.request

def get_word_definition(word):

    url="https://api.pearson.com/v2/dictionaries/lasde/entries?headword={}&apikey=44895c72-54c4-49ab-9c49-4e6a8ce5b12a".format(word)
    page=urllib.request.urlopen(url)
    x=page.read().decode("utf8")
    t=json.loads(x)
    try:
        x=t["results"][0]["senses"][0]["definition"][0]
    except:
        x=None
    return x