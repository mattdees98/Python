import tweepy
import tkinter
import datetime

consumer_key = '4twDZwmP6qCbYXxSpi89dvtAY'
consumer_secret = 'G0Nb9txBk46ah0hAdNnkZVMIVZu8NBZZoG7oeiha2I7cajl7PX'
access_token = '1244029937142640640-ARBO1QIOcXIBmsGEhPhpWcMItjVtQD'
access_token_secret = 'yW1dVgWOGvvoLQXDFea19duBTytQkZCwT6tEwaCYcrU4j'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

now = datetime.datetime.now()
now1 = datetime.datetime.now()
now = now.strftime("%A")

now1 = now1.strftime("%m-%d")

def publictweet():
	global tweettopublish
	if now1 == '12-25':
		tweettopublish = 'Merry Cuckmas! Pat Hurley is relaxing with the family sipping on some extremely soft egg nog. No simping today! Aha.'
		update_status()
		return
	if now1 == '1-1':
		tweettopublish = 'Happy New Year! New year new me! Just kidding Pat Hurley is definitely still a simp.'
		update_status()
		return
	if now == 'Monday':
	    tweettopublish = 'Today is Monday. A fresh week with lots of simping to do for Pat Hurley.'
	    update_status()
	if now == 'Tuesday':
	    tweettopublish = 'Today is Tuesday. Simp simp simp'
	    update_status()
	if now == 'Wednesday':
	    tweettopublish = 'Today is Wednesday. Pat is on his way to teach Simping 101 at Cuck University.'
	    update_status()
	if now == 'Thursday':
	    tweettopublish = 'Today is Thursday. Watch out for Pat Hurley ripping 6 sets of incline bench. Simp.'
	    update_status()
	if now == 'Friday':
	    tweettopublish = "Today is Friday. Nothing is wrong with him, he's just a simp"
	    update_status()
	if now == 'Saturday':
	    tweettopublish = 'Today is Saturday. Hide your girlfriends! Pat Hurley is desperately simping.'
	    update_status()
	if now == 'Sunday':
	    tweettopublish = 'Today is Sunday. A day of rest for the simp lord.'
	    update_status()

def update_status():
	api.update_status(tweettopublish)

publictweet()

