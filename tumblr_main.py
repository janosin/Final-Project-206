import oauth2
import pytumblr
import time
import json
import sqlite3
from operator import itemgetter
from collections import OrderedDict
import plotly
import plotly.graph_objs as go
import pandas as pd

client = pytumblr.TumblrRestClient(
	'zQYemGVerUvczk9HCM7kmjBlX3EWL5b7Va1Wi0hEbNCJMKglqZ',
	'HP9wWfkXTnvGOpkwEW7xPtIsEIIQr2V23R448DfFEkfCDIdlJv',
	'4veWODwU9G2BNUYGC41uGHcLZvTzAMooIm7rMTqoL92MCIsCIk',
	'yZv0Yj3ueXTkZJMxUGSzcgbsHarjcXd9yiqHrDrREN714QYYHR'
)

blog_name = 'nicole-is-rad.tumblr.com'

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

#parameter: string with day and time ex "Sunday 11:51 PM"

def time_of_day (x):
	
	time_data = x.split()
	hour = float(time_data[1][:2])
	minute = time_data[1][-2:]
	
	time_group = ""
	
	if time_data[2] == "AM":
		
		if hour >= 1 and hour <= 5:
			time_group =  "12:00am - 5:59am"
			
		elif hour == 12:
			time_group =  "12:00am - 5:59am"
		
		elif hour >= 6 and hour <= 11:
			time_group = "6:00am - 11:59am"
			
	elif time_data[2] == "PM":
		
		if hour >= 1 and hour <= 5:
			time_group = "12:00pm - 5:59pm"
			
		elif hour == 12:
			time_group = "12:00pm - 5:59pm"
		
		elif hour >= 6 and hour <= 11:
			time_group = "6:00pm - 11:59pm"
			
	day_time = time_data[0] + " " + time_group
	
	return (day_time)
	
	
	



def tum_posts(blog):
	 
	
	
	if blog in CACHE_DICTION:
		
		print("Tumblr data for " + blog + " was in the cache\n")
		tum_results = CACHE_DICTION[blog] #uses data already in cache
		return tum_results
	
	else:
		
		print("fetching tumblr data for " + blog)
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
		cache_file.write(json.dumps(CACHE_DICTION, indent = 2)+ "\n")
		cache_file.close()
		tum_results = tum_posts_results
		return tum_results

#parameter d must be an ordered dictionary
def create_bar_graph(d):
	
	xvals = list()
	yvals = list()

	for x in d:
		xvals.append(x)

	for y in d.values():
		yvals.append(y)

	data = [go.Bar(
			x= yvals,
			y=xvals,
			text = yvals,
			textposition = 'auto',
			orientation = 'h',
			marker=dict(
			color='rgb(176,196,222)')
	    )]

	layout = go.Layout(

		title = "Number of Posts on Tumblr by Day of Week",
		titlefont = dict (size = 30),

		xaxis=dict(
		title='Number of Tumblr Posts',
		titlefont=dict(
			size=18)
			
		)
	)

	fig = go.Figure(data=data, layout=layout)

	plotly.offline.plot(fig, filename='tumblr-barchart.html')
		

def main():
	
	print ("Enter user url")

	tum_data = tum_posts(blog_name)
	
	conn = sqlite3.connect("206FinalProject.sqlite")
	cur = conn.cursor()

	cur.execute('DROP TABLE IF EXISTS Tumblr')
	cur.execute('CREATE TABLE Tumblr (post_id NUMBER UNIQUE, day_of_week TEXT, time TEXT, time_group TEXT)')
	
	for x in tum_data:
		
		tum_id = (x['id'])
		tum_date = convert_timestamp(x['timestamp']).split()
		tum_day = tum_date[0]
		tum_time = tum_date[2]+ " " + tum_date[3]
		tum_day_and_time = tum_day + " " + tum_time
		new_time_group =  time_of_day(tum_day_and_time)
		tum_tup = (tum_id, tum_day, tum_time, new_time_group)
		
		
		
		cur.execute('INSERT INTO Tumblr (post_id, day_of_week, time, time_group) VALUES (?,?,?,?)', tum_tup)
	
	conn.commit()		
	
	time_list = list()
	t_list = OrderedDict()
		
	
	day_list = ["Sunday", "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday"]
	
	day_dic = OrderedDict()
	
	for item in day_list:
		t_list[item + " 12:00am - 5:59am"] = 0
		t_list[item + " 6:00am - 11:59am"] = 0
		t_list[item + " 12:00pm - 5:59pm"] = 0
		t_list[item + " 6:00pm - 11:59pm"] = 0
		
	for item in day_list:
		day_dic[item] = 0
	
	sq = (cur.execute('SELECT time_group FROM Tumblr'))
	for item in sq:
		for x in item:
			time_list.append(x)
	
	
	for i in time_list:
		t_list[i] = t_list.get(i,0) + 1
	
	sq1 = (cur.execute('SELECT day_of_week FROM Tumblr'))
	
	day_list = list()
	
	
	for i in sq1:
		for x in i:
			day_list.append(x)
	
	for x in day_list:
		day_dic[x] = day_dic.get(x,0) + 1
		
	#create_bar_graph(day_dic)
	
	data_list = list()

	for item in t_list:
		
		new_tup = (item, t_list[item])
		data_list.append(new_tup)


	df = pd.DataFrame(data_list, columns = ["Time of Day", "# of Posts"])
	
	print (df)
	
	conn.close()
main()