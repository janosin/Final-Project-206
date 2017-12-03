import oauth2
import pytumblr
import time

client = pytumblr.TumblrRestClient(
	'zQYemGVerUvczk9HCM7kmjBlX3EWL5b7Va1Wi0hEbNCJMKglqZ',
	'HP9wWfkXTnvGOpkwEW7xPtIsEIIQr2V23R448DfFEkfCDIdlJv',
	'4veWODwU9G2BNUYGC41uGHcLZvTzAMooIm7rMTqoL92MCIsCIk',
	'yZv0Yj3ueXTkZJMxUGSzcgbsHarjcXd9yiqHrDrREN714QYYHR'
)

# Make the request
tum_likes_data = client.likes()['liked_posts']

for x in tum_likes_data:
	print(time.strftime('%Y-%m-%d %I:%M %p', time.localtime(x['liked_timestamp'])))
