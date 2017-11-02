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
			return book

def insert_book(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "INSERT INTO book_info(title,isbn,author,image,link,register,register_email,created_date) values(%s,%s,%s,%s,%s,%s,%s,CURDATE())"
	#print (query['title'],query['inputISBN'],query['author'],query['image'],query['link'],query['name'],query['email'])
	cur.execute(sql,(query['title'],query['inputISBN'],query['author'],query['image'].split('?')[0],query['link'],query['name'],query['email']))
	conn.commit()
	conn.close()

def search_book(string, type):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'SELECT * FROM book_info where title like \'%'+string+'%\' ORDER BY BOOK_NO desc'
	cur.execute(sql)
	rows = cur.fetchall()
	conn.close()
	return rows
	
def borrow_booklog(query):
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
	sql = 'SELECT register_email,register,book_no FROM book_info where book_no=%s'	
	cur.execute(sql,(query['book_no']))
	rows=cur.fetchall()
	#print(rows)
	send_mail("borrow", rows)
	conn.close()

def approve_booklog(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2
	sql = "UPDATE book_info set avalability=2 where book_no=%s"
	#send_mail
	cur.execute(sql,(query['book_no']))
	conn.commit()
	conn.close()

def return_booksearch(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "SELECT * FROM book_info JOIN book_log ON book_info.book_no=book_log.no where borrower=%s and borrower_email=%s"
	#print(sql)
	cur.execute(sql,(query['name'],query['email']))
	rows=cur.fetchall()
	conn.close
	#print(rows)
	return rows	

def return_booklog(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "UPDATE book_log set return_date=CURDATE() where book_no=%s and borrower=%s, borrower_email=%s, borower_date=%s"
	cur.execute(sql,(query['book_no'],query['name'],query['email'],query['return_date']))
	conn.commit()
	
	#빌린 책 상태를 대여중으로 변경 대여가능:avalability=0 대여대기:avalability=1 대여중:avalability=2
	sql = "UPDATE book_info set avalability=0 where book_no=%s"
	#send_mail
	cur.execute(sql,(query['book_no']))
	conn.commit()
	conn.close()

	
def send_mail(status, data):
	import smtplib
	from email.mime.text import MIMEText
	smtp = smtplib.SMTP('localhost')
	smtp.ehlo()      # say Hello
	#smtp.starttls()  # TLS 사용시 필요
	
	if status=="borrow":
		msg = MIMEText('본문 테스트 메시지')
		msg['Subject'] = '[BookBook]책 대여 요청'
		
	if status=="return":
		msg = MIMEText('본문 테스트 메시지')
		msg['Subject'] = '[BookBook]책 반납 요청'
	
	msg['To'] = 'yh.kim@kia.com'
	smtp.sendmail('bookbook@kia.com', 'yh.kim@kia.com', msg.as_string())
	 
	smtp.quit()

