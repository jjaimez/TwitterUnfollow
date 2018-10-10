import tweepy
import time

#Configs
FOLLOW_LIMIT = 1000
UNFOLLOW_LIMIT = 10000
USER_NAME = ''

def limit_handled(cursor):
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			time.sleep(15 * 60)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True) 

followers = []
friends = []

print "beginning..."

followers.extend(limit_handled(tweepy.Cursor(api.followers_ids, USER_NAME).items()))
friends.extend(limit_handled(tweepy.Cursor(api.friends_ids, USER_NAME).items()))

print "followers: " + str(len(followers))
print "friends: " + str(len(friends))

followersSet = set(followers)
friendsSet = set(friends)

toAdd = list(followersSet - friendsSet)
toDelete = list(friendsSet - followersSet)

print "those that you don't follow: " + str(len(toAdd))
print "those that don't follow you: " + str(len(toDelete))

print "starting to follow."

i = 0
for e in toAdd:
	i += 1
	try:
		api.create_friendship(e)
	except tweepy.TweepError:
		pass
	if i == FOLLOW_LIMIT: 
		break

print "created friendships: "+str(i)

print "starting to unfollow"

i = 0
for e in toDelete:
	i += 1
	try:
		api.destroy_friendship(e)
	except tweepy.TweepError:
		pass
	if i == UNFOLLOW_LIMIT:
		break

print "destroyed friendships: "+str(i)

print "Done - if it was useful please leave a star on github :)"




