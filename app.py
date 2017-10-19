from flask import Flask, render_template, request, url_for
from book import *

app = Flask(__name__)

@app.route('/')
def index():
	book_list = search_book("%","title")

	# modify image link to improve image quality.
	for book in book_list:
		book['image'] = book['image'].split('?')[0]

	return render_template('home.html', books=book_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/scan')
def scan():
	return render_template('scan.html')

@app.route('/scroll')
def scroll():
    return render_template('scroll.html')

@app.route('/regist')
def regist_book():
    return render_template('registBook.html')

@app.route('/search', methods=['POST','GET'])
def search():
	query = request.form['query'].lower()
	book_list = search_book(query, "title")
	for book in book_list:
		book['image'] = book['image'].split('?')[0]

	return render_template('home.html', books=book_list)


#@app.route('/books')
#def books():
#    return render_template('books.html', books=book_list)

#@app.route('/book/<string:id>')
#def book(id):
#    return render_template('book.html', id=id)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)
