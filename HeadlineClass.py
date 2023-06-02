#!/usr/bin/env python3
from flask import Flask, render_template, request
from datetime import datetime, timedelta, date
import random
import json

app = Flask(__name__)

class HeadlineLoader:
    def __init__(self, json_file):
        self.headlines = []
        self.last_headline = None
        with open(json_file) as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data["category"] in ["POLITICS", "QUEER VOICES", "BLACK VOICES", "TECH", "BUSINESS"]:
                        headline = {
                            "id": -1,
                            "link": data["link"],
                            "headline": data["headline"],
                            "date": datetime.strptime(data["date"], "%Y-%m-%d").date()
                        }

                        self.headlines.append(headline)
                except ValueError:
                    pass

    def get_random_headline(self):
        if self.headlines:
            i = random.randrange(0,len(self.headlines))
            self.headlines[i]['id'] = i
            self.last_headline = self.headlines[i]
            return self.last_headline
        else:
            return None
    def get_last_headline(self):
        if self.last_headline == None:
            return None
        else:
            return self.last_headline
    def get_headline_by_headline(self, headline):
        for item in self.headlines:
            if item["headline"] == headline:
                return item
            return None
        
    def get_headline_by_id(self, id):
        for item in self.headlines:
            #print("should match at some point", item.get('id'), id)
            if item.get('id') == id:
                print("found Item")
                return item
        print("Failed to find headline")
        return self.last_headline
json_file = "News_Category_Dataset_v3.json"
headline_loader = HeadlineLoader(json_file)

@app.route('/')
def index():
    random_headline = headline_loader.get_random_headline()
    return render_template('index.html', headline=random_headline)

@app.route('/guess', methods=['POST'])
def guess():
    guess_date = request.form.get('date')
    headline = request.form.get('headline')
    actual_date = request.form.get('actual_date')
   
    try:
        actual_date = datetime.strptime(actual_date, "%Y-%m-%d").date()
        guess_date = datetime.strptime(guess_date, "%Y-%m-%d").date()
    except:
        guess_date = date(2002, 12, 31)
        actual_date = date(2022, 12, 31)
    
    days_off = abs((guess_date - actual_date).days)
    return render_template('result.html', headline=headline, actual_date=actual_date, guess_date=guess_date, days_off=days_off)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
