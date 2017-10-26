from flask import Flask, jsonify, render_template, request, url_for
from flask.ext.runner import Runner
from book import *

app = Flask(__name__)
runner = Runner(app)

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
def regist():
	#query = request.form['query'].lower
	#bookinfo = get_bookinfo(query)
	return render_template('registBook.html')

@app.route('/search', methods=['POST','GET'])
def search():
	query = request.form['query'].lower()
	book_list = search_book(query, "title")
	for book in book_list:
		book['image'] = book['image'].split('?')[0]

	return render_template('home.html', books=book_list)

@app.route('/_get_book')
def get_book():
	ISBN = request.args.get('ISBN', 0, type=int)
	#print (ISBN)
	bookinfo = get_bookinfo(ISBN)
	return jsonify(bookinfo)
	
@app.route('/regist_book', methods=['POST','GET'])
def regist_book():
	query=request.form
	print(query)
	insert_book(query)
	book_list = search_book("%","title")

	# modify image link to improve image quality.
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
    runner.run()
    #	app.run(debug=True)

