from flask import render_template, request, jsonify
from Main import app
from Main.text_extraction import text_extraction
from Main.set_url import setURL
Season = ""
Series = ""
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('popup.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Season = request.form['Season']
        Series = request.form['Series']
        url = setURL(Series, Season)
        print('This is URL:',url)
        key_word = text_extraction(url, Series)
        return jsonify({'keywords':key_word})
    return jsonify({'Error':'Missing Data' })
