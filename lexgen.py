import codecs
import csv
import datetime
import facepp
import json
import genderator
import os

MINIMAL_CONFIDENCE = 0.75

path = os.path.dirname(__file__)

guesser = genderator.Parser()

females = codecs.open(os.path.join(path, 'data/females.tsv'), 'w', 'UTF-8')
males = codecs.open(os.path.join(path, 'data/males.tsv'), 'w', 'UTF-8')

females_writer = csv.writer(females, delimiter='\t')
males_writer = csv.writer(males, delimiter='\t')

not_enough_confidence = 0
tweets_count = 0
females_count = 0
males_count = 0

api = facepp.API('14593ac430ff440a9fdc92e361efea71', 'RPzUPKrotSUztSW8QRk0SfIT5CPbXX5C', 'http://api.us.faceplusplus.com/')

users = {}

time = datetime.datetime.now()
with codecs.open(os.path.join(path, 'data/geolocated-asturias.json'), 'r', 'UTF-8') as file:
    for line in file:
        tweets_count += 1
        tweet = json.loads(line)
        if tweet['user']['screen_name'] in users:
            data = users[tweet['user']['screen_name']][:]
            data.append(tweet['text'])
            if users[tweet['user']['screen_name']][2] == 'Male':
                males_writer.writerow(data)
                males_count += 1
            else:
                females_writer.writerow(data)
                females_count += 1
        else:
            prediction = guesser.guess_gender(tweet['user']['name'])
            if prediction is not None and prediction['surnames']:
                gender = prediction['gender']
                confidence = prediction['confidence']

                # if confidence < MINIMAL_CONFIDENCE or not prediction['surnames']:
                #     answer = api.detection.detect(url=tweet['user']['profile_image_url'].replace('_normal', ''))
                #     if len(answer['face']) == 1:
                #         temp_gender = answer['face'][0]['attribute']['gender']['value']
                #         temp_confidence = answer['face'][0]['attribute']['gender']['confidence']
                #         if gender == temp_gender and temp_confidence >= MINIMAL_CONFIDENCE:
                #             gender = temp_gender
                #             confidence = temp_confidence

                if confidence >= MINIMAL_CONFIDENCE:
                    classification_line = [tweet['user']['name'], tweet['user']['screen_name'], confidence, tweet['text']]
                    users[tweet['user']['screen_name']] = [tweet['user']['name'], tweet['user']['screen_name'], gender, confidence]
                    if gender == 'Male':
                        males_writer.writerow(classification_line)
                        males_count += 1
                    else:
                        females_writer.writerow(classification_line)
                        females_count += 1
        if tweets_count % 1000 == 0:
            print(tweets_count, 'processed. Time employed:', datetime.datetime.now() - time)
            time = datetime.datetime.now()

females.close()
males.close()
print(len(users))
print(tweets_count, 'tweets parsed')
print(females_count, 'tweets from females')
print(males_count, 'tweets from males')
print(not_enough_confidence, 'with not enough confidence')
