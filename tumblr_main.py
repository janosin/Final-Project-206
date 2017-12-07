import oauth2
import pytumblr
import time
import json
import sqlite3

client = pytumblr.TumblrRestClient(
	'zQYemGVerUvczk9HCM7kmjBlX3EWL5b7Va1Wi0hEbNCJMKglqZ',
	'HP9wWfkXTnvGOpkwEW7xPtIsEIIQr2V23R448DfFEkfCDIdlJv',
	'4veWODwU9G2BNUYGC41uGHcLZvTzAMooIm7rMTqoL92MCIsCIk',
	'yZv0Yj3ueXTkZJMxUGSzcgbsHarjcXd9yiqHrDrREN714QYYHR'
)

CACHE_FNAME = "206_Final_Project.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


def convert_timestamp (x):
	return time.strftime('%A %Y-%m-%d %I:%M %p', time.localtime(x))

# Make the request



def tum_posts(blog):
	 
	
	
	if blog in CACHE_DICTION:
		
		#print("Tumblr data was in the cache")
		tum_results = CACHE_DICTION[blog] #uses data already in cache
		return tum_results
	
	else:
		
		#print("fetching tumblr data")
		tum_posts_results = list()

		for x in client.posts(blog, limit=100, offset = 0)['posts']:
			tum_posts_results.append(x)
		
		for x in client.posts(blog, limit=100, offset = 21)['posts']:
			tum_posts_results.append(x)

		for x in client.posts(blog, limit=100, offset = 42)['posts']:
			tum_posts_results.append(x)

		for x in client.posts(blog, limit=100, offset = 63)['posts']:
			tum_posts_results.append(x)

		for x in client.posts(blog, limit=100, offset = 84)['posts']:
			tum_posts_results.append(x)
		
		CACHE_DICTION[blog] = tum_posts_results
		cache_file = open(CACHE_FNAME, 'w') #then writes it to cache file
		cache_file.write(json.dumps(CACHE_DICTION)+ "\n")
		cache_file.close()
		tum_results = tum_posts_results
		return tum_results
	

def main():

	tum_data = tum_posts('nicole-is-rad.tumblr.com')
	
	conn = sqlite3.connect("206FinalProject.sqlite")
	cur = conn.cursor()

	cur.execute('DROP TABLE IF EXISTS Tumblr')
	cur.execute('CREATE TABLE Tumblr (post_id NUMBER UNIQUE, day_of_week TEXT, time TEXT)')
	
	for x in tum_data:
		
		tum_id = (x['id'])
		tum_date = convert_timestamp(x['timestamp']).split()
		tum_day = tum_date[0]
		tum_time = tum_date[2]+ " " + tum_date[3]
		tum_tup = (tum_id, tum_day, tum_time)
		
		cur.execute('INSERT INTO Tumblr (post_id, day_of_week, time) VALUES (?,?,?)', tum_tup)
	
	conn.commit()		
	
	
	
	
	
	conn.close()
main()