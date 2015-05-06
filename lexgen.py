import codecs
import csv
import datetime
import json
import operator
import os

import genderator


MINIMAL_CONFIDENCE = 0.75

path = os.path.dirname(__file__)
guesser = genderator.Parser()

females_file = codecs.open(os.path.join(path, 'data/females.tsv'), 'w', 'UTF-8')
males_file = codecs.open(os.path.join(path, 'data/males.tsv'), 'w', 'UTF-8')
females_writer = csv.writer(females_file, delimiter='\t')
males_writer = csv.writer(males_file, delimiter='\t')

female_tweets = 0
male_tweets = 0
tweets_processed = 0
tweets_classified = 0

female_users = {}
male_users = {}


def classify_tweet(user_screen_name, text, gender, confidence):
    global female_tweets, male_tweets, tweets_classified

    fields = [user_screen_name, confidence, text]

    if gender == 'Female':
        if user_screen_name in female_users:
            female_users[user_screen_name] += 1
        else:
            female_users[user_screen_name] = 1
        females_writer.writerow(fields)
        female_tweets += 1
    else:
        if user_screen_name in male_users:
            male_users[user_screen_name] += 1
        else:
            male_users[user_screen_name] = 1
        males_writer.writerow(fields)
        male_tweets += 1

    tweets_classified += 1


def classify_tweets():
    print('Classifying tweets')

    global tweets_processed
    millis_elapsed = 0

    # Count lines
    total_tweets = 0
    with open(os.path.join(path, 'data/geolocated-asturias.json'), 'r') as file:
        for line in file:
            total_tweets += 1
    file.close()

    print(total_tweets, 'tweets found')

    time = datetime.datetime.now()
    with open(os.path.join(path, 'data/geolocated-asturias.json'), 'r') as file:
        for line in file:
            tweets_processed += 1
            tweet = json.loads(line)
            user_name = tweet['user']['name']
            user_screen_name = tweet['user']['screen_name']

            prediction = guesser.guess_gender(user_name)

            if prediction is not None and prediction['surnames']:
                confidence = prediction['confidence']
                gender = prediction['gender']

                if confidence >= MINIMAL_CONFIDENCE:
                    classify_tweet(user_screen_name, tweet['text'], gender, confidence)

            if tweets_processed > 1 and tweets_processed % 50000 == 0:
                millis_elapsed += (datetime.datetime.now() - time).total_seconds() * 1000
                millis_to_finish = (millis_elapsed / tweets_processed) * (total_tweets - tweets_processed)
                time = datetime.datetime.now()
                print(tweets_processed, 'processed. Estimated seconds to finish:', millis_to_finish / 1000,
                      '(' + str(time + datetime.timedelta(milliseconds=millis_to_finish)) + ')')

    file.close()
    females_file.close()
    males_file.close()


def generate_top_files():
    print('\nGenerating top files\n')

    with codecs.open(os.path.join(path, 'data/top_females.tsv'), 'w', 'UTF-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for (screen_name, count) in sorted(female_users.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow([screen_name, count])
    file.close()

    with codecs.open(os.path.join(path, 'data/top_males.tsv'), 'w', 'UTF-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for (screen_name, count) in sorted(male_users.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow([screen_name, count])
    file.close()


classify_tweets()
generate_top_files()

print(tweets_classified, 'tweets classified')
print(female_tweets, 'tweets from females')
print(male_tweets, 'tweets from males')
print(len(female_users), 'female users')
print(len(male_users), 'male users')