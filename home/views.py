import pandas as pd
from django.shortcuts import render
import requests
from subprocess import run, PIPE
import sys
from dateutil import parser
import sys
import json
from home.utils import *
from django.http import HttpResponse
from transformers import AutoTokenizer
import preprocessor as p
import torch
from django.http import JsonResponse
import time
pd.options.mode.chained_assignment = None
model = pd.read_pickle(r'model_pkl')
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
from django.template.response import TemplateResponse

def preprocess(text):
    text = p.clean(text)
    return text


def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def getanalysis(score):
    if score == 1 or score == 2:
        return 'Negative'
    elif score == 3:
        return 'Neutral'
    elif score == 4 or score == 5:
        return 'Positive'
    else:
        return 'Not Predicted'


def index(request):
    return render(request, "index.html")


def search(request):
    global start
    start = None

    global searchkey
    global fromDATE
    global toDATE
    global datalimit
    searchkey = None
    fromDATE = None
    toDATE = None
    datalimit = ""
    if request.method == 'POST':
        searchkey = request.POST.get('a')
        fromDATE = request.POST.get('b')
        toDATE = request.POST.get('c')
        #datalimit = request.POST.get('d')
        print(searchkey)
        print(fromDATE)
        print(toDATE)
        #print(datalimit)
        return render(request, 'index.html')
    return render(request, 'search.html')


# Create your views here.
def cards(request):
    print("Time started")
    request.start_time = time.time()
    keywordfetch = searchkey
    fromD = fromDATE
    toD = toDATE
    Dlimit = datalimit
    print("in cards func")
    print(keywordfetch)
    print(fromD)
    print(toD)
    print(Dlimit)
    automatic = automates(keywordfetch, fromD, toD, Dlimit)
    df1 = pd.read_csv(keywordfetch+'.csv')
    print("final csv")
    print(df1)
    df1 = df1.drop_duplicates(subset=['id'])
    print("duplicates removed")
    df1['preprocess_tweet'] = df1['tweet'].iloc[:].apply(preprocess)
    print("preprocessing done")
    df1['score'] = df1['preprocess_tweet'].iloc[:].apply(sentiment_score)
    print("sentiment analysis done")
    end = time.time()
    df1['sentiment'] = df1['score'].apply(getanalysis)
    print("score done")

    df2=df1

    def dateConversion(d):
        c = parser.parse(d)
        datef = c.date()
        return datef

    df2['date'] = df2['date'].apply(lambda x: dateConversion(x))
    df2['date'] = df2['date'].astype(str)
    print("date conversion done")
    ptweets = df2[df2.sentiment == 'Positive']
    ptweets = ptweets[['date', 'sentiment']]
    ptweets['Counts'] = ptweets.groupby(['sentiment'])['date'].transform('count')
    ptweets["Counts by date"] = ptweets.groupby(['date', 'sentiment']).transform('count')
    ptweets.drop("Counts", axis=1, inplace=True)
    ptweets = ptweets.drop_duplicates('date', keep='last')
    ptweets.rename(columns={'date': 'label'}, inplace=True)
    ptweets.rename(columns={'Counts by date': 'value'}, inplace=True)
    print(ptweets)
    p = ptweets.to_dict('records')
    pdata = p

    ntweets = df2[df2.sentiment == 'Negative']
    ntweets = ntweets[['date', 'sentiment']]
    ntweets['Counts'] = ntweets.groupby(['sentiment'])['date'].transform('count')
    ntweets["Counts by date"] = ntweets.groupby(['date', 'sentiment']).transform('count')
    ntweets.drop("Counts", axis=1, inplace=True)
    ntweets = ntweets.drop_duplicates('date', keep='last')
    ntweets.rename(columns={'date': 'label'}, inplace=True)
    ntweets.rename(columns={'Counts by date': 'value'}, inplace=True)
    print(ntweets)
    n = ntweets.to_dict('records')
    ndata = n

    neutweets = df2[df2.sentiment == 'Neutral']
    neutweets = neutweets[['date', 'sentiment']]
    neutweets['Counts'] = neutweets.groupby(['sentiment'])['date'].transform('count')
    neutweets["Counts by date"] = neutweets.groupby(['date', 'sentiment']).transform('count')
    neutweets.drop("Counts", axis=1, inplace=True)
    neutweets = neutweets.drop_duplicates('date', keep='last')
    neutweets.rename(columns={'date': 'label'}, inplace=True)
    neutweets.rename(columns={'Counts by date': 'value'}, inplace=True)
    print(neutweets)
    neu = neutweets.to_dict('records')
    neudata = neu
    card = df1.to_dict('records')
    data5 = card
    total = time.time() - request.start_time
    print("Total Time isssssssssss")
    print(total)
    json_time = json.dumps(json.loads(json.dumps(total), parse_float=lambda x: round(float(x), 2)))
    print("json converted Timeeeee")
    print(json_time)

    return JsonResponse({'cards': json.dumps(data5), 'positive': json.dumps(pdata),'negative': json.dumps(ndata), 'neutral': json.dumps(neudata), "time": json_time})