import tweepy
import unicodedata
import codecs

from generateTweet import *

con_key = 'D3B8vkfi2H3Wrqd2CXdZ7C3bE'
con_sec = 'UPOdLz2fzfPpkGQHxD3LqoQmXeuuJVjCCMeWSVQoYFLtiypeaB'
acc_tok = '983521193797013507-kNcs4WhO3ZyIZHBl9uii18iTpdmrvZn'
acc_sec = 'a55tXEHYc1hzSXPgE2kDzeQskDX4IkXL5IqyeImPsBUhg'

authorization = tweepy.OAuthHandler(con_key, con_sec)
authorization.set_access_token(acc_tok, acc_sec)

api = tweepy.API(authorization)

'''
Below is the code for gathering headlines. We have the database so it is no
longer necessary.

writer = codecs.open('headlines.txt', 'w', 'utf-8')
headlines = api.user_timeline(id = 'TheOnion', count = 200)

count1 = 0
lowid = headlines[0].id

for i in range(20):
    for j in range(200):
        if ('RT' not in headlines[j].text):
            print headlines[j].text
            writer.write(headlines[j].text)
            writer.write('\n')
            lowid = headlines[j].id - 1
    headlines = api.user_timeline(id = 'TheOnion', max_id = lowid, count = 200)
writer.close()

'''

reader = open('headlines.txt')
arr_headlines = reader.readlines()
reader.close()

for pos, headline in enumerate(arr_headlines):
    arr_headlines[pos] = removeURL(headline)

writer = open('tweets.txt', 'w')
for headline in arr_headlines:
    if headline != 'Did You Know? ' and headline != 'From the Archives: ' and headline != 'National News Highlights ' and headline != 'Visit ' and headline.count(' ') < 20:
        writer.write(headline)
        writer.write('\n')
writer.close()
