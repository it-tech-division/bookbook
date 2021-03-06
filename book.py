import urllib.request
import json, sys
import pymysql
import re
import smtplib
from email.mime.text import MIMEText

CLIENT_ID = "ENRbt0kUz4t8IFpMUrXP"
CLIENT_SECRET = "rH72o8liHs"
HOST="localhost"
DB_USER="root"
DB_PWD="b00kbook"
DB_NAME="hyundai_book"


def get_api(bookname, count):
	url = "https://openapi.naver.com/v1/search/book?query=%s&display=%d&sort=count" % (bookname, count)

	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id", CLIENT_ID)
	request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
	response = urllib.request.urlopen(request)
	return response

def get_bookinfo(query):
	response = get_api(query, 3)

	if response.getcode() == 200:
		json_result = response.read().decode('utf-8')
		result = json.loads(json_result)

		for book in result['items']:
			# modify image link to improve image quality.
			#print(book)
			book['image'] = book['image'].split('?')[0]
			book['title'] = re.sub('<[^>]*>', '', book['title'])
			book['description'] = re.sub('<[^>]*>', '', book['description'])
			book['title'] = book['title'][:99]
			book['isbn'] = book['isbn'].split()[1]
			print(book)
			return book

def insert_book(query):
	print("왔다아아아아아")
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	print(query)
	sql = "INSERT INTO book_info(title,isbn,author,image,link,register,register_email,created_date) values(%s,%s,%s,%s,%s,%s,%s,CURDATE())"
	#print (query['title'],query['inputISBN'],query['author'],query['image'],query['link'],query['name'],query['email'])
	cur.execute(sql,(query['title'],query['inputISBN'],query['author'],query['image'].split('?')[0],query['link'],query['name'],query['email']))
	conn.commit()
	conn.close()

def search_book(string, type, start="0", end="30"):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'SELECT * FROM book_info where title like \'%'+string+'%\' ORDER BY avalability ASC, BOOK_NO DESC LIMIT '+start+','+end
	cur.execute(sql)
	rows = cur.fetchall()
	conn.close()
	return rows

def borrow_booklog(query, book_info):
	print("왔다")
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#책 정보를 book_log 테이블에 입력
	sql = "INSERT INTO book_log(no,borrower,borrower_email,message,borrow_date) values(%s,%s,%s,%s,CURDATE())"
	cur.execute(sql,(query['book_no'],query['borrower_name'],query['borrower_email'],query['message']))
	conn.commit()
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2
	sql = "UPDATE book_info set avalability=1 where book_no=%s"
	#send_mail
	cur.execute(sql,(query['book_no']))
	conn.commit()
	sql = 'SELECT register_email,register,book_no,title FROM book_info where book_no=%s'
	cur.execute(sql,(query['book_no']))
	rows=cur.fetchall()
#	print('rows 1 : ', rows)
	rows[0].update(query)
#	print('rows 2 : ', rows)
	send_mail("borrow", rows[0], book_info)
	conn.close()

def approve_booklog(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2 반납대기:avalability=3
	sql = "UPDATE book_info set avalability=2 where book_no=%s"
	#send_mail
	cur.execute(sql,(query['book_no']))
	conn.commit()
	conn.close()

def return_booksearch(query, book_info):
	print(query['book_no'])
	print('1234')
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "UPDATE book_info set avalability=0 where book_no=%s"
	#send_mail
	cur.execute(sql,(query['book_no']))
	conn.commit()
	sql = "UPDATE book_log set return_date=CURDATE() where no=%s and borrower_email=%s"
	#send_mail
	cur.execute(sql,(query['book_no'],query['borrower_email']))
	conn.commit()

	print("반납하기 메일 테스트")
	send_mail("return", query, book_info)
	conn.close()

def request_book_return(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2 반납대기:avalability=3
	sql = "UPDATE book_info set avalability=3 where book_no=%s"
	cur.execute(sql,(query['book_no']))
	#sql = "UPDATE book_log set return_date=CURDATE() where no=%s and borrower=%s and borrower_email=%s and borrow_date=%s"
	#print(sql%(query['book_no'],query['name'],query['email'],query['borrow_date']))
	#cur.execute(sql,(query['book_no'],query['name'],query['email'],query['borrow_date']))
	conn.commit()
	conn.close()

def confirm_book_return(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2 반납대기:avalability=3
	sql = "UPDATE book_info set avalability=0 where book_no=%s"
	cur.execute(sql,(query['book_no']))
	conn.commit
	sql = "UPDATE book_log set return_date=CURDATE() where no=%s and borrower=%s and borrower_email=%s and borrow_date=%s"
	print(sql%(query['book_no'],query['name'],query['email'],query['borrow_date']))
	cur.execute(sql,(query['book_no'],query['name'],query['email'],query['borrow_date']))
	conn.commit()
	conn.close()

def send_mail(status, data, book_info=None):
	smtp = smtplib.SMTP('localhost')
	#smtp.ehlo()      # say Hello
	#smtp.starttls()  # TLS 사용시 필요

	if status == "borrow":
		print("대여하기 메일 발송 :")
		f=open('static/borrow-mail.html','r')
		mail_text=f.read()
		print(data['borrower_name'])
		mail_text=re.sub('borrow_name_input',data['borrower_name'],mail_text)
		mail_text=re.sub('borrow_email_input',data['borrower_email'],mail_text)
		mail_text=re.sub('borrow_request_input',data['message'],mail_text)
		mail_text=re.sub('title_input',book_info['title'],mail_text)
#		print(mail_text)
		print('대여자 :', data)
		print('book_info : ', book_info )
		msg = MIMEText(mail_text,'html')
		msg['Subject'] = '[BookBook]책 대여 요청'
		msg['To'] = book_info['register_email'] 
		smtp.sendmail('bookbook@kia.com', book_info['register_email'], msg.as_string())

	elif status == "return":
		print("반납하기 메일 발송 :")

		f=open('static/return-request.html','r')
		mail_text=f.read()
		print('data :', data)
		print(data['borrower_name'])
		mail_text=re.sub('borrow_name_input',data['borrower_name'],mail_text)
		mail_text=re.sub('borrow_email_input',data['borrower_email'],mail_text)
		mail_text=re.sub('title_input',book_info['title'],mail_text)
		print('*' * 50)

		msg = MIMEText(mail_text,'html')
		msg['Subject'] = '[BookBook]책 반납 요청'
		msg['To'] = book_info['register_email'] 
		smtp.sendmail('bookbook@kia.com', book_info['register_email'], msg.as_string())
		
	elif status == "bug":
		print("버그신고 메일 발송 :")
		msg = MIMEText(data['problem_detail'])
		msg['Subject'] = '[BookBook] 버그 전달'
#		print(msg)
		msg['To'] = 'yeonji1122@kia.com' 
		smtp.sendmail('bookbook@kia.com', 'yeonji1122@kia.com', msg.as_string())
		
	smtp.quit()

def login_process(email, password):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#sql = "INSERT INTO user_info(name,email,password) values(%s,%s,%s)"
	cur.execute("SELECT COUNT(1) FROM user_info WHERE email = %s", email)
	rows=cur.fetchone()
	if rows['COUNT(1)']:
		cur.execute("SELECT password FROM user_info WHERE email = %s;", email)
		for row in cur.fetchall():
			if password==row['password']:
				return "success"
			else:
				return "fail"
	else:
		return "fail"
		
		
def insert_user(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "INSERT INTO user_info(name,email,password) values(%s,%s,%s)"
	print (query['name'],query['email'],query['password'])
	cur.execute(sql,(query['name'],query['email'],query['password']))
	conn.commit()
	conn.close()
	
def check_email(email):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select * from user_info where email=%s"
	cur.execute(sql, email)
	emailCheck = cur.fetchone()
	conn.commit()
	conn.close()
	return emailCheck

	
def myPage_book(string):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	print("book.py : "+string)
	#sql = 'SELECT * FROM book_info, book_log where book_info.book_no=book_log.no and (register_email=%s or borrower_email= %s)'
	#sql = 'SELECT *,"regit" FROM book_info, book_log where book_info.book_no=book_log.no and register_email=%s union SELECT *,"borrow" FROM book_info, book_log where book_info.book_no=book_log.no and borrower_email=%s;'
	sql = 'SELECT *, "regit" FROM book_info where register_email=%s UNION SELECT *, "borrow" FROM book_info WHERE book_no IN (SELECT no FROM book_log WHERE borrower_email=%s and return_date IS NULL);'
	cur.execute(sql, (string, string))
	rows = cur.fetchall()
	conn.close()
	return rows

def delete_book(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	print(query)
	sql = "delete from book_info where book_no=%s"
	cur.execute(sql,query)
	conn.commit()
	conn.close()
	
def get_name(email):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	print(email)
	sql = "select email, name from user_info where email=%s"
	cur.execute(sql,email)
	register = cur.fetchone()
	conn.commit()
	conn.close()
	return register


def get_book_info(book_no):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select title,isbn,register,register_email from book_info where book_no=%s"
	cur.execute(sql, book_no)
	result = cur.fetchone()
	conn.commit()
	conn.close()
	print("==> Result : %s, Book_no :  %s" % (result, book_no))
	return result
