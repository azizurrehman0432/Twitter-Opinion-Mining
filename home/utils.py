import pandas as pd

import twint
from twint.twint import storage
from twint.twint.storage import panda
import sys
import json
from .views import *
import schedule
import time
from datetime import datetime

ad = datetime.now()


class automates:

    def __init__(self, hashtag_search, fromD, toD, Dlimit):
        self.a = self.scrap(hashtag_search, fromD, toD, Dlimit)

    def scrap(self, hashtag_search, fromD, toD, Dlimit):
        global df
        df = None
        global list12
        list12 = []
        print(fromD)
        print(toD)
        print(hashtag_search)
        strdate1 = fromD
        strdate2 = toD
        datetimeobj1 = datetime.strptime(strdate1, "%Y-%m-%d")
        datetimeobj2 = datetime.strptime(strdate2, "%Y-%m-%d")
        no_days = (datetimeobj2 - datetimeobj1).days
        year = fromD.split('-')
        month = fromD.split('-')
        month_f = month[1]
        m=int(month_f)
        year_f = year[0]
        y = int(year_f)
        temp=0
        daya=1
        print(year_f + "-" + str(m) + "-")
        print("total Days", no_days)
        for i in range(1, no_days):
            temp=temp+1
            
            if i % 30 == 0:
                m = m+1
                temp = 1
                print("Tweets Fetching Started")

                
                c = twint.twint.Config()
                c.Search = hashtag_search
                c.Lang = 'en'
                c.Until = str(year_f + "-" + str(m) + "-" + str(temp))
                c.Limit = 50
                c.Show_cashtags = True
                c.Show_hashtags = True
                c.Stats = True
                c.Retweets = True
                c.Pandas = True
                c.Store_csv = True
                c.Store_json = True
                c.Output = hashtag_search + ".csv"
                c.Output = hashtag_search + ".JSON"
                twint.twint.run.Search(c)
                
            else:
                print("Fetching Tweets")
                c = twint.twint.Config()
                c.Search = hashtag_search
                c.Lang = 'en'
                c.Until = str(year_f + "-" + str(m) + "-" + str(temp))
                c.Limit = 50
                c.Show_cashtags = True
                c.Show_hashtags = True
                c.Stats = True
                #c.Resume = 'cursors.txt'
                c.Retweets = True
                c.Pandas = True
                c.Store_csv = True
                #c.Store_json = True
                c.Output = hashtag_search + ".csv"
                #c.Output = hashtag_search + ".JSON"
                twint.twint.run.Search(c)        
            
        return list12

        
