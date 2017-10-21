import urllib.request
import json, sys
import pymysql

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
		for i in result['items']:
			#print (i['title'])
			return i

def insert_book(query):
	print("123123")
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'INSERT INTO book_info(title,isbn,author,image,link,created_date) values(%s,%s,%s,%s,%s,CURDATE())'
	print (query['title'],query['inputISBN'],query['author'],query['image'],query['link'])
	cur.execute(sql,(query['title'],query['inputISBN'],query['author'],query['image'],query['link']))
	conn.close()

def search_book(string, type):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'SELECT * FROM book_info where title like \'%'+string+'%\' ORDER BY BOOK_NO desc'
	cur.execute(sql)
	rows = cur.fetchall()
	return rows


