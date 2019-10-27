from flask import render_template, request, jsonify
from Main import app
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
        print('This is URL:',url)
        #insert beautiful soup work here
        #Return Statements will be changed
        return jsonify({'Season':Season, 'Series': Series})
    return jsonify({'Error':'Missing Data' })
