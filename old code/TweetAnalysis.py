import json
import pandas as pd
import matplotlib.pyplot as plt
import re


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def main():
    # Reading Tweets
    print('Reading Tweets\n')
    tweets_data_path = "C:/Users/prono/.spyder-py3/twitter_data.txt"

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue


            # Structuring Tweets
    print('Structuring Tweets\n')
    tweets = pd.DataFrame()
    tweets['text'] = list([tweet.get('text','') for tweet in tweets_data])
    tweets['lang'] = list([tweet.get('lang','') for tweet in tweets_data])
    tweets['country'] = list([tweet.get('location','') for tweet in tweets_data])
    #tweets['country'] = list([tweet.get('place','').get('country','') if tweet.get('place','') != None else None for tweet in tweets_data])


    # Analyzing Tweets by Language
    print('Analyzing tweets by language\n')
    tweets_by_lang = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_lang', format='png')


    # Analyzing Tweets by Country
    print('Analyzing tweets by country\n')
    tweets_by_country = tweets['country'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
    plt.savefig('tweet_by_country', format='png')


    # Adding president columns to the tweets DataFrame
    print('Adding president tags to the data\n')
    tweets['trump'] = tweets['text'].apply(lambda tweet: word_in_text('trump', tweet))
    tweets['modi'] = tweets['text'].apply(lambda tweet: word_in_text('modi', tweet))
    tweets['putin'] = tweets['text'].apply(lambda tweet: word_in_text('putin', tweet))


    # Analyzing Tweets by president: First attempt
    print('Analyzing tweets by president: First attempt\n')
    prg_langs = ['trump', 'modi', 'putin']
    tweets_by_prg_lang = [tweets['trump'].value_counts()[True], tweets['modi'].value_counts()[True],
                          tweets['putin'].value_counts()[True]]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Ranking: trump vs. modi vs. putin (Raw data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    plt.savefig('tweet_by_president_1', format='png')


    # Targeting relevant tweets
    print('Targeting relevant tweets\n')
    tweets['president'] = tweets['text'].apply(lambda tweet: word_in_text('president', tweet))
    tweets['best'] = tweets['text'].apply(lambda tweet: word_in_text('best', tweet))
    tweets['relevant'] = tweets['text'].apply(
        lambda tweet: word_in_text('president', tweet) or word_in_text('best', tweet))


    # Analyzing Tweets by president: Second attempt
    print('Analyzing tweets by president: First attempt\n')

    import IPython
    IPython.embed()

    def get_value_counts(tweets, language):
         try:
             return tweets[tweets['relevant'] == True][language].value_counts()[True]
         except KeyError:
             return 0

    tweets_by_prg_lang = [get_value_counts(tweets, 'trump'),
                          get_value_counts(tweets, 'modi'),
                          get_value_counts(tweets, 'putin')]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Ranking: trump vs. modi vs. putin (Relevant data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    plt.savefig('tweet_by_president_2', format='png')


    # Extracting Links
    tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))
    tweets_relevant = tweets[tweets['relevant'] == True]
    tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

    print('\nBelow are some Python links that we extracted\n')
    print(tweets_relevant_with_link[tweets_relevant_with_link['trump'] == True]['link'].head())



if __name__ == '__main__':
    main()
