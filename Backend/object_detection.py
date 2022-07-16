import cv2
import cvlib as cv
import matplotlib.pyplot as plt
from nltk.corpus import wordnet
import nltk
import requests

def init():
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def captionize():
    
    img = plt.imread('temp.jpg')
    print(img)
    img = cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    # print("hello")
    objects = set(cv.detect_common_objects(img)[1])
    print("objects detected...")
    # synonyms = set()
    # for object in objects:
    #     for synset in wordnet.synsets(object):
    #         for lemma in synset.lemmas():
    #             synonyms.add(lemma.name().replace('_',' '))


    # def querise(keyword):
    #     return "query="+keyword.replace(" ","%20")

    # objects.update(synonyms)
    # objects = list(objects)
    # # print(objects)
    # queries = map(querise, objects)

    # print(queries)
    # url = "https://quotable.io/search/quotes?"+"&".join(queries)

    # # print(url)
    # print("getting queries...")
    # quotes = []
    # authors = []
    # if len(objects) != 0:
    #     response = requests.request("GET", url)
    #     results = response.json()["results"]
    #     print(results)
    #     for result in results:
    #         quotes.append(result["content"])
    #         authors.append(result["author"])
    
    # return [authors, quotes]
    return keywordize(objects)

def keywordize(objects):
    objects = set(objects)
    synonyms = set()
    for object in objects:
        for synset in wordnet.synsets(object):
            for lemma in synset.lemmas():
                synonyms.add(lemma.name().replace('_',' '))


    def querise(keyword):
        return "query="+keyword.replace(" ","%20")

    objects.update(synonyms)
    objects = list(objects)
    # print(objects)
    queries = map(querise, objects)

    # print(queries)
    url = "https://quotable.io/search/quotes?"+"&".join(queries)

    # print(url)
    # print("getting queries...")
    quotes = []
    authors = []
    if len(objects) != 0:
        response = requests.request("GET", url)
        results = response.json()["results"]
        print(results)
        for result in results:
            quotes.append(result["content"])
            authors.append(result["author"])
    
    return [authors, quotes]



