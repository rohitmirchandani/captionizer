from contextlib import nullcontext
import cv2
from imageai.Detection import ObjectDetection
import numpy
import matplotlib

# import cvlib as cv

# import matplotlib.pyplot as plt
from nltk.corpus import wordnet
import nltk
import requests

def init():
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    global detector
    detector = ObjectDetection()
    model_path = "yolo-tiny.h5"
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel(detection_speed = "faster")


def captionize():
    
    img = cv2.imread('temp.jpg')
    # print(img)
    img = cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    img = cv2.resize(img, (200, int((len(img)/len(img[0])*200))))
    img = numpy.pad(img, ((100,100),(100,100),(0,0)))

    # objects = set(cv.detect_common_objects(img)[1])
    
    objects = set()
    output = detector.detectObjectsFromImage(input_image=img, input_type="array", minimum_percentage_probability = 10 ,output_type = "array")[1]
    for i in output:
        objects.add(i['name'])
    print(objects)
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
        unique = set()
        response = requests.request("GET", url)
        results = response.json()["results"]
        # print(results)
        for result in results:
            key = result["content"] + " " + result["author"]
            if key not in unique:
                quotes.append(result["content"])
                authors.append(result["author"])
                unique.add(key)
            
    
    return [authors, quotes]



