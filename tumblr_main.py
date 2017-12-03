import oauth2
import pytumblr
import time

client = pytumblr.TumblrRestClient(
	'zQYemGVerUvczk9HCM7kmjBlX3EWL5b7Va1Wi0hEbNCJMKglqZ',
	'HP9wWfkXTnvGOpkwEW7xPtIsEIIQr2V23R448DfFEkfCDIdlJv',
	'4veWODwU9G2BNUYGC41uGHcLZvTzAMooIm7rMTqoL92MCIsCIk',
	'yZv0Yj3ueXTkZJMxUGSzcgbsHarjcXd9yiqHrDrREN714QYYHR'
)


def convert_timestamp (x):
	return time.strftime('%A %Y-%m-%d %I:%M %p', time.localtime(x))

# Make the request



def tum_likes():
	tum_likes_data = client.likes(limit = 50)['liked_posts']
	for x in tum_likes_data:
		like_time = (convert_timestamp(x['liked_timestamp']))
		like_data_tup = (x['id'], like_time, x['summary'].strip())
		print (like_data_tup)
	

# print(client.posts('nicole-is-rad.tumblr.com', limit=50))

def main():
	tum_likes()
	
main()