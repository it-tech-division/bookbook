import urllib.request
import json, sys

CLIENT_ID = "ENRbt0kUz4t8IFpMUrXP"
CLIENT_SECRET = "rH72o8liHs"

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


if __name__ == '__main__':
	response = get_api(get_bookname(), get_count())

	if response.getcode() == 200:
		json_result = response.read().decode('utf-8')
		result = json.loads(json_result)
		for i in result['items']:
			print('=' * 100)
			print('Title : ', i['title'])
			print('Author : ', i['author'])
			print('Image : ', i['image'])
			print('Link : ', i['link'])
			print('Description : ', i['description'][:50])
			print(i)
	else:
		print("Error Code:" + response.getcode())
