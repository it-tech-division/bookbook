from flask import Flask,session, jsonify, render_template, request, url_for, redirect,flash
from flask.ext.runner import Runner
from book import *

app = Flask(__name__)
runner = Runner(app)

@app.route('/')
def index():
	book_list = search_book("%","title","0","30")
	
	if 'email' in session:
		email = session['email']
		query = get_name(email)
		print(query)
		return render_template('home.html', books=book_list, register=query)
	else:		
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
	if 'email' in session:
		email = session['email']
		query = get_name(email)
		print(query)
		return render_template('registBook.html', register=query)
	else:	
		messages="도서는 로그인 후에 등록 가능합니다."
		return render_template('loginForm.html', alert_messages=messages)

@app.route('/returns')
def returns():
	if 'email' in session:
		email = session['email']
		query = get_name(email)
		print(query)
		return render_template('returnBook.html', register=query)
	else:	
		return render_template('returnBook.html')

@app.route('/search', methods=['POST','GET'])
def search():
	query = request.form['query'].lower()
	start = request.form['start']
	end = request.form['end']
	book_list = search_book(query, "title", start, end)
	
	if 'email' in session:
		email = session['email']
		nameQuery = get_name(email)
		print(query)
		messages=""
		return render_template('home.html', books=book_list, register=nameQuery, alert_messages=messages)
	else:		
		messages="검색된 책이 없습니다."
		return render_template('home.html', books=book_list, alert_messages=messages)
	
	

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
	messages=query['title']+" 책 등록 성공"
	book_list = search_book("%","title", "0", "30")
	
	if 'email' in session:
		email = session['email']
		nameQuery = get_name(email)
		return render_template('home.html', books=book_list, register=nameQuery, alert_messages=messages)
	else:		
		messages="검색된 책이 없습니다."
		return render_template('home.html', books=book_list, alert_messages=messages)

@app.route('/borrow_book', methods=['POST','GET'])
def borrow_book():
	query=request.form
	print(query)
	borrow_booklog(query)
	messages=query['title']+" 대여 신청 완료"
	book_list = search_book("%","title", "0", "30")
	return render_template('home.html', books=book_list,alert_messages=messages)

@app.route('/approve_book', methods=['GET'])
def approve_book():
	query=request.args
	approve_booklog(query)
	return redirect(url_for('index'))

@app.route('/return_book', methods=['POST','GET'])
def return_book():
	query = request.form
	print(query)
	borrow_bookinfo=return_booksearch(query)
	#print (borrow_bookinfo)
	
	if 'email' in session:
		email = session['email']
		nameQuery = get_name(email)
		return render_template("returnBook.html",books=borrow_bookinfo, register=nameQuery)
	else:				
		return render_template("returnBook.html",books=borrow_bookinfo)

@app.route('/return_book_procees1', methods=['POST','GET'])
def return_book_procees1():
	query = request.form
	return_booklog(query)
	messages=query['title']+" 반납신청 완료"
	book_list = search_book("%","title")
	return render_template('home.html', books=book_list,alert_messages=messages)

# 회원가입
@app.route('/regist_user', methods=['POST','GET'])
def regist_user():
	query=request.form
	print(query)
	insert_user(query)
	session['email'] = request.form['email']
	email = session['email']
	nameQuery = get_name(email)
	print(nameQuery)
	messages=request.form['email']+"님 환영합니다."
	book_list = search_book("%","title","0","30")
	return render_template('home.html', books=book_list,alert_messages=messages, register=nameQuery)
	
	return render_template('home.html')	
	
@app.route('/checkEmail', methods=['POST'])
def check_email():
	email=request.form
	print(email)
	num=check_email(email)
	if num :
		messages="이미 사용중인 아이디입니다."
	else : 
		messages="사용 가능한 아이디입니다."
	
	return render_template('registUser.html', alert_messages=messages)	
	
	
# test
@app.route('/mailform')
def mailform():
    return render_template('mailForm.html')


@app.route('/loginform', methods=['POST','GET'])
def loginform():
	if 'email' in session:
		messages="이미 로그인 되어 있습니다. "
		book_list = search_book("%","title")
		return render_template('home.html', books=book_list,alert_messages=messages)
	if request.method == 'POST':
		result=login_process(request.form['email'],request.form['password'])
		if result=="success":
			session['email'] = request.form['email']
			email = session['email']
			nameQuery = get_name(email)
			print(nameQuery)
			messages=request.form['email']+"님 환영합니다."
			book_list = search_book("%","title","0","9")
			return render_template('home.html', books=book_list,alert_messages=messages, register=nameQuery)
		else:
			messages="아이디, 패스워드를 확인해 주세요."
	return render_template('loginForm.html')
	
@app.route('/logout', methods=['POST','GET'])
def logout():
	if 'email' in session:
		session.clear()
		messages="안전하게 로그아웃 되셨습니다."
		return render_template('loginForm.html', alert_messages=messages)	
	

@app.route('/registUser')
def regist_user_form():
    return render_template('registUser.html')
	
@app.route('/findIdPw')
def findIdPw():
    return render_template('findIdPw.html')
	
@app.route('/myPage')
def myPage():
	string = session['email']
	print(string)
	book_list = myPage_book(string)
	query = get_name(string)
	return render_template('myPage.html', books=book_list, register=query)
	
@app.route('/deleteBook')
def delete_book():
	print("삭제하러 왔지")
	string = session['email']
	query=request.args['delete_no']
	print(query)
	delete_book(query)
	book_list = myPage_book(string)
	nameQuery=get_name(string)
	messages="도서 삭제가 완료되었습니다."
	return render_template('myPage.html', books=book_list, register=nameQuery, alert_messages=messages)
	
	
if __name__ == '__main__':
	app.secret_key = 'sample_secreat_key'
	#runner.debug=True
	runner.run()
	#	app.run(debug=True)
