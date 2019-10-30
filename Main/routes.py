from flask import render_template, request, jsonify
from Main import app
from web_scraper import WebScraper
from text_extraction import TextExtractor

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('popup.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Season = request.form['Season']
        Series = request.form['Series']
        Series = str(Series)
        Series.replace(" ", "_")
        url = 'https://en.wikipedia.org/wiki/'+Series+'_(season_'+Season+')'
        print('This is URL:', url)

        #web scraping
        scraper = WebScraper()
        text = scraper.web_scraper(url)

        #text mining
        miner = TextExtractor()
        keywords = miner.text_extractor(text)

        #Return Statements will be changed
        return jsonify({'keywords':keywords})
    return jsonify({'Error':'Missing Data' })
