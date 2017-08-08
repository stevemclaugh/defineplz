import twitter
import time
import urllib3
import certifi


posts=[]

infile=open("/Users/mclaughs/Dropbox/twoemoji/current_bot_v2/twoemoji_set.txt")

for line in infile:
	posts.append(line.strip("\n"))

infile.close()

for post in posts:
	api = twitter.Api(consumer_key='XXX', consumer_secret='XXX', access_token_key='XXX', access_token_secret='XXX')
	try:
		status = api.PostUpdate(post)
		#print status
		print "Just posted this great emoji pair: "+post
	except:
		print "Oops! This pair failed to post: "+post
	time.sleep(1460.0)





































#####
