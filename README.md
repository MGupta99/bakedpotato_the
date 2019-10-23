# Creative AI Project

- The Baked Potato
- Gabriel Garfinkel; ggarfink
- Manas Vemuri;
- Milan Gupta; milagu
- Liam Corriston; liamcorr

All Downloaded Python Libraries used:
Tweepy
urllib
random
codecs
unicodedata
csv
spacy
sys

For our reach, we generated a twitterbot that takes as input tweets from "The Onion" and outputs new tweets similar to them. Using our code and the twitter API, we can tweet without actually opening twitter. Additionally, our code uses the words in each tweet to find a relevant image to the tweet and attaches it if possible.

1. We had to filter out URLs from the initial dataset of tweets, as we did not want to tweet these. We searched each tweet for words that had both a '.' and a '/', and we removed all parts of the tweet after that point (hence also removing hashtags).
2. We used Spacy to make sure no tweet ended in a conjunction or a determiner (a, an, the).
3. We limited tweets to 280 characters in our code.
4. Running through each word in a generated tweet, we compared the words to a large database of tagged images, and attached the image whose tag matched the most words.

For our showmanship, we used tweepy to develop a twitterbot and created a twitter
handle (@bakedpotato_the) to publish our generated tweets. Using urllib to put
pictures with the tweet, we were able to tweet a randomly-generated headline using
a database of 2,800 previous tweets from The Onion (filtering out retweets, urls,
etc.).

New files:
Images folder - contains databse of image tags and URLs that we used to find images
generateTweet.py - contains code that actually generates tweets
tweet.py - contains tweet class
getHeadlines.py - contains code that scraped headlines from twitter and did some preprocessing

To see our project at work, run generate.py and then go to @bakedpotato_the on
twitter to view the result. 

