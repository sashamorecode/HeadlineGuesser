from flask import Flask, render_template, request
from datetime import datetime, timedelta
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
                    headline = {
                        "link": data["link"],
                        "headline": data["headline"],
                        "date": datetime.strptime(data["date"], "%Y-%m-%d").date()
                    }
                    self.headlines.append(headline)
                except ValueError:
                    pass

    def get_random_headline(self):
        if self.headlines:
            self.last_headline = random.choice(self.headlines)
            return self.last_headline
        else:
            return None
    def get_last_headline(self):
        if self.last_headline == None:
            return None
        else:
            return self.last_headline

json_file = "News_Category_Dataset_v3.json"
headline_loader = HeadlineLoader(json_file)

@app.route('/')
def index():
    random_headline = headline_loader.get_random_headline()
    return render_template('index.html', headline=random_headline)

@app.route('/guess', methods=['POST'])
def guess():
    guess_date = request.form['date']
    guess_date = datetime.strptime(guess_date, "%Y-%m-%d").date()
    last_headline = headline_loader.get_last_headline()
    actual_date = last_headline['date']
    days_off = abs((guess_date - actual_date).days)
    return render_template('result.html', headline=last_headline, guess_date=guess_date, days_off=days_off)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
