
from pymongo import MongoClient
import json
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "993861826910785536-SRwlwm6u1QnlMB8efcPYWURlniZi3o6"
access_token_secret = "YaxmO5FV7cVaLtb5xxxBMGtRr3HECFQSE7rAPrSwY3DSO"
consumer_key = "YGxg6Pv3b5DNIB4O9vIxhO8it"
consumer_secret = "dzqEyOncIN3TQ2ViOooPpEdKMxUz90Ub368RJw15vUXiIQamdi"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        client = MongoClient('localhost', 27017)
        db = client['twitter_db']
        collection = db['twitter_collection']
        tweet = json.loads(data)
 
        collection.insert(tweet)
        
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['trump', 'modi', 'putin'])
    
