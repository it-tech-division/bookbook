import urllib.request
import json, sys
import pymysql

CLIENT_ID = "ENRbt0kUz4t8IFpMUrXP"
CLIENT_SECRET = "rH72o8liHs"
HOST="localhost"
DB_USER="root"
DB_PWD="b00kbook"
DB_NAME="hyundai_book"

class BookInfo():
	def get_bookname():
		try:
			return urllib.parse.quote(sys.argv[1])
		except:
			return urllib.parse.quote(input('Book Name : '))

	def get_count():
		try:
			return int(sys.argv[2])
		except:
			return 3 # default value is 3

	def get_api(bookname, count):
		url = "https://openapi.naver.com/v1/search/book?query=%s&display=%d&sort=count" % (bookname, count)

		request = urllib.request.Request(url)
		request.add_header("X-Naver-Client-Id", CLIENT_ID)
		request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
		response = urllib.request.urlopen(request)
		return response

	def Get_BookInfo(query):
		data = BookInfo.get_api(query, 3)
		if data.getcode() == 200:
			json_result = data.read().decode('utf-8')
			result = json.loads(json_result)
			for i in result['items']:
				print (i['title'])
				return i
				
	def Insert_DB(query):
		conn=pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
		cur = conn.cursor(pymysql.cursors.DictCursor)
		sql='INSERT INTO book_info(title,isbn,author,image,link,created_date) values(%s,%s,%s,%s,%s,CURDATE())'
		#print (query['title'],query['isbn'],query['author'],query['image'],query['link'])
		cur.execute(sql,(query['title'],query['isbn'],query['author'],query['image'],query['link']))
		conn.close()

	def Search_DB(string,type):
		conn=pymysql.connect(host=HOST, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')
		cur = conn.cursor(pymysql.cursors.DictCursor)
		sql='SELECT * FROM book_info where title like \'%'+string+'%\''
		cur.execute(sql)
		rows=cur.fetchall()
		return rows


#if __name__ == '__main__':
#	print (BookInfo.Search_DB("스물", "title"))
#	BookInfo.Insert_DB(BookInfo.Get_BookInfo(BookInfo.get_bookname()))
#	response = get_api(get_bookname(), get_count())

#	if response.getcode() == 200:
#		json_result = response.read().decode('utf-8')
#		result = json.loads(json_result)
#		for i in result['items']:
#			print('=' * 100)
#			print('Title : ', i['title'])
#			print('Author : ', i['author'])
#			print('Image : ', i['image'])
#			print('Link : ', i['link'])
#			print('Description : ', i['description'][:50])

			
	#else:
		#print("Error Code:" + response.getcode())
