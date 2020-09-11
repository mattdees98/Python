import tweepy
import tkinter
import datetime

consumer_key = 'g7sQ9PuS1oAuvQFuHcbszN4jz'
consumer_secret = 'APNWcdSTx1Zug269K353hQPlGpfKUlB82aWa70XeuCuvDoE4oK'
access_token = '1244029937142640640-upNZAITMnSCPq55UstBQ1DX4dJ6mQI'
access_token_secret = 'N4kSKzlxI2Wo80mPLQF9hFkWCI2khZIvNab5G4MD7Eq8q'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

now = datetime.datetime.now()
now = now.strftime("%A")

def publictweet():
    if now == 'Monday':
        tweettopublish = 'Today is Monday. Pat Hurley is just starting his week of simping.'
    if now == 'Tuesday':
        tweettopublish = 'Today is Tuesday. Pat Hurley is still a simp.'
    if now == 'Wednesday':
        tweettopublish = 'Today is Wednesday. Hump day! Pat Hurley is out there simping.'
    if now == 'Thursday':
        tweettopublish = 'Today is Thursday. Pat Hurley is a simp.'
    if now == 'Friday':
        tweettopublish = 'Today is Friday. Pat Hurley is beginning his weekend of simping.'
    if now == 'Saturday':
        tweettopublish = 'Today is Saturday. Pat Hurley is again, a simp.'
    if now == 'Sunday':
        tweettopublish = 'Today is Sunday. Pat Hurley is tired after a long week of being the simp lord. '
    
    api.update_status(tweettopublish)

publictweet()

