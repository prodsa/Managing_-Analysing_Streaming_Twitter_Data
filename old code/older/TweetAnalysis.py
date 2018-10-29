import json
import pandas as pd
import matplotlib.pyplot as plt

#path where twitter_data.txt is stored
tweets_data_path="C:/Users/prono/.spyder-py3/twitter_data.txt"

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print(len(tweets_data))

tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

"""
#3. Mining the tweets
import re

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

tweets['trump'] = tweets['text'].apply(lambda tweet: word_in_text('trump', tweet))
tweets['modi'] = tweets['text'].apply(lambda tweet: word_in_text('modi', tweet))
tweets['putin'] = tweets['text'].apply(lambda tweet: word_in_text('putin', tweet))

#We can calculate the number of tweets for each programming language as follows:
print(tweets['trump'].value_counts()[True])
print(tweets['modi'].value_counts()[True])
print(tweets['putin'].value_counts()[True])

prg_langs = ['trump', 'modi', 'putin']
tweets_by_prg_lang = [tweets['trump'].value_counts()[True], tweets['modi'].value_counts()[True], tweets['putin'].value_counts()[True]]

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: trump vs. modi vs. putin (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()

#targeting relevant tweets
tweets['president'] = tweets['text'].apply(lambda tweet: word_in_text('president', tweet))
tweets['best'] = tweets['text'].apply(lambda tweet: word_in_text('best', tweet))

tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('president', tweet) or word_in_text('best', tweet))

print(tweets['president'].value_counts()[True])
print(tweets['best'].value_counts()[True])
print(tweets['relevant'].value_counts()[True])

print(tweets[tweets['relevant'] == True]['trump'].value_counts()[True])
print(tweets[tweets['relevant'] == True]['modi'].value_counts()[True])
print(tweets[tweets['relevant'] == True]['putin'].value_counts()[True])

tweets_by_prg_lang = [tweets[tweets['relevant'] == True]['trump'].value_counts()[True], 
                      tweets[tweets['relevant'] == True]['modi'].value_counts()[True], 
                      tweets[tweets['relevant'] == True]['putin'].value_counts()[True]]
x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width,alpha=1,color='g')
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: trump vs. modi vs. putin (Relevant data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()

def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

tweets_relevant = tweets[tweets['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

print(tweets_relevant_with_link[tweets_relevant_with_link['trump'] == True]['link'])
print(tweets_relevant_with_link[tweets_relevant_with_link['modi'] == True]['link'])
print(tweets_relevant_with_link[tweets_relevant_with_link['putin'] == True]['link'])
"""