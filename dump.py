#!/usr/bin/python

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


def insert_book(query):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = "INSERT INTO book_info(title,isbn,author,image,link,register,register_email,created_date) values(%s,%s,%s,%s,%s,%s,%s,CURDATE())"
	query['name'] = '홍길동'
	query['email'] = 'aa@hyundai.com'
#	print (query['title'],query['isbn'],query['author'],query['image'],query['link'],query['name'],query['email'])
	cur.execute(sql,(query['title'],query['isbn'],query['author'],query['image'].split('?')[0],query['link'],query['name'],query['email']))
	conn.commit()
	conn.close()

def search_book(string, type):
	conn = pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	sql = 'SELECT * FROM book_info where title like \'%'+string+'%\''
	cur.execute(sql)
	rows = cur.fetchall()
	return rows


if __name__ == '__main__':
	for no, book in enumerate(get_bookinfo(sys.argv[1], int(sys.argv[2]))):
		print('=' * 30)
		print('''
title : %(title)s
isbn : %(isbn)s
author : %(author)s
image : %(image)s
link : %(link)s
''' % book)
		insert_book(book)
