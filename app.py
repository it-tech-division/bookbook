from flask import Flask, render_template, request, url_for
from data import Books
from book import BookInfo	

app = Flask(__name__)


book_list = Books()

@app.route('/')
def index():
	book_list=BookInfo.Search_DB("%","title")
	new_list=[]
	for item in book_list:
		item['image'] = item['image'].split('?')[0]
		new_list.append(item)	
	return render_template('home.html', books=new_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/books')
def books():
    return render_template('books.html', books=book_list)

@app.route('/book/<string:id>')
def book(id):
    return render_template('book.html', id=id)
	
@app.route('/scan')
def scan():
	return render_template('scan.html')
	
@app.route('/holder')
def print_holder():
    return render_template('holder.js')

@app.route('/regist')
def regist_book():
    return render_template('registBook.html')
	
#@app.route('/search/<string:query>')
@app.route('/search', methods=['POST','GET'])
def search():
	query = request.form['query'].lower()
	result_list=BookInfo.Search_DB(query,"title")
	new_list = []
	for item in result_list:
		item['image'] = item['image'].split('?')[0]
		new_list.append(item)	
	return render_template('home.html', books=new_list)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
