import urllib.request
import json, sys
import pymysql
import pprint, re

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

def get_bookinfo(query, count=5):
	response = get_api(query, count)

	if response.getcode() == 200:
		json_result = response.read().decode('utf-8')
		result = json.loads(json_result)
		# remove tag in book title.
		for book in result['items']:
			book['title'] = re.sub('<[^>]*>', '', book['title'])
			book['title'] = book['title'][:49]
			book['isbn'] = book['isbn'].split()[1]
		return result['items']

def insert_book(book, no):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "INSERT INTO book_info(NO,TITLE,ISBN,AUTHOR,DESCRIPTION,IMAGE,LINK,CREATEDATA) values('%s','%s','%s','%s','%s','%s','%s',CURDATE())"
#	print(sql % (no, book['title'], book['isbn'], book['author'], book['description'], book['image'], book['link']))
	cur.execute(sql % (no, book['title'], book['isbn'], book['author'], book['description'], book['image'], book['link']))
	conn.close()

#	INSERT INTO book_info(NO,TITLE,ISBN,AUTHOR,DESCRIPTION,IMAGE,LINK,CREATEDATA) values(%s,%s,%s,%s,%s,%s,%s,CURDATE()) (8, 'Python 프로그래밍 정복하기 창의적 사고를 위한', '9791185123554', '강남오|김재호', '『창의적 사고를 위한 <b>PYTHON</b> 프로그래밍 정복하기』는 처음으로 컴퓨터 프로그래밍을 학습하는 컴퓨터공학 비전공자 및 저학년의 컴퓨터공학 전공자를 위해 작성되었다. 따라서 컴퓨터 프로그래밍을 학습하는 초보자들이 반드시 알아야할 프로그래밍의 개념과 문법적 표현을 중심으로 다루었다. 뿐만 아니라... ', 'http://bookthumb.phinf.naver.net/cover/102/002/10200299.jpg?type=m1&udate=20160218', 'http://book.naver.com/bookdb/book_detail.php?bid=10200299')

def search_book(string, type):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'SELECT * FROM book_info where title like \'%'+string+'%\''
	cur.execute(sql)
	rows = cur.fetchall()
	return rows


if __name__ == '__main__':
	for no, book in enumerate(get_bookinfo('Python', 10)):
		print('=' * 30)
		print('''
title : %(title)s
isbn : %(isbn)s
author : %(author)s
image : %(image)s
link : %(link)s
''' % book)
		insert_book(book, no+1)
