from flask import Flask, render_template, request, url_for
from data import Books


app = Flask(__name__)
#


book_list = Books()

@app.route('/')
def index():
    return render_template('home.html', books=book_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/books')
def books():
    return render_template('books.html', books=book_list)

@app.route('/book/<string:id>')
def book(id):
    return render_template('book.html', id=id)

@app.route('/holder')
def print_holder():
    return render_template('holder.js')

#@app.route('/search/<string:query>')
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].lower()
    result_list = []

    for book in book_list:
        book_title = book['title'].lower()
        if book_title.find(query) != -1:
            result_list.append(book)

    return render_template('home.html', books=result_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
##
