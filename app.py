from flask import Flask, jsonify, render_template, request, url_for, redirect,flash
from flask.ext.runner import Runner
from book import *

app = Flask(__name__)
runner = Runner(app)

@app.route('/')
def index():
	book_list = search_book("%","title")
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
	if book_list:
		messages=""
	else:
		messages="검색된 책이 없습니다."
	return render_template('home.html', books=book_list,alert_messages=messages)

@app.route('/_get_book')
def get_book():
	ISBN = request.args.get('ISBN', 0, type=int)
	#print (ISBN)
	bookinfo = get_bookinfo(ISBN)
	return jsonify(bookinfo)
	
@app.route('/regist_book', methods=['POST','GET'])
def regist_book():
	query=request.form
	#print(query)
	insert_book(query)
	messages=query['title']+" 책 등록 성공"
	book_list = search_book("%","title")
	return render_template('home.html', books=book_list,alert_messages=messages)

@app.route('/borrow_book', methods=['POST','GET'])
def borrow_book():
	query=request.form
	#print(query)
	borrow_booklog(query)
	messages=query['title']+" 대여 신청 완료"
	book_list = search_book("%","title")
	return render_template('home.html', books=book_list,alert_messages=messages)
	
@app.route('/approve_book', methods=['GET'])		
def approve_book():
	query=request.args
	approve_booklog(query)
	return redirect(url_for('index'))
	
#@app.route('/books')
#def books():
#    return render_template('books.html', books=book_list)

#@app.route('/book/<string:id>')
#def book(id):
#    return render_template('book.html', id=id)



if __name__ == '__main__':
    runner.run()
    #	app.run(debug=True)

