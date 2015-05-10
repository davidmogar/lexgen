import collections
import csv
import datetime
import genderator
import json
import os

from .faces import Faces

BASE_DIR = os.path.dirname(__file__)


class ChickSexer:

    def __init__(self):
        self._faces = Faces('14593ac430ff440a9fdc92e361efea71', 'RPzUPKrotSUztSW8QRk0SfIT5CPbXX5C')
        self._genderator = genderator.Parser()

        self.females = collections.defaultdict(int)
        self.males = collections.defaultdict(int)
        self.stats = collections.defaultdict(int)

        self._millis_elapsed = 0
        self._last_measured_time = 0

    def classify(self, dataset, path, detect_faces=False, min_confidence=0.75, tweets_until_stats=1000):
        self._validate_file(dataset)
        self._prepare_result_files(path)
        self._millis_elapsed = 0
        self._last_measured_time = datetime.datetime.now()

        tweets_processed = 0

        print('Starting dataset classification')
        with open(dataset, encoding='utf-8') as file:
            for tweet in self._get_tweets_objects(file):
                tweets_processed += 1
                prediction = self._genderator.guess_gender(tweet['user']['name'])

                if prediction is not None:
                    confidence = prediction['confidence']
                    gender = prediction['gender']

                    if detect_faces and (confidence < min_confidence or not prediction['surnames']):
                        confidence = self._apply_face_recognition(gender, confidence, tweet)

                    if confidence >= min_confidence:
                        self._classify_tweet(tweet['user']['screen_name'], tweet['text'], gender, confidence)

                if tweets_processed > 1 and tweets_processed % tweets_until_stats == 0:
                    self._show_remaining_time(tweets_processed)

        self.stats['tweets_processed'] = tweets_processed
        self._females_file.close()
        self._males_file.close()

    def show_stats(self):
        females = self.stats['females'] = len(self.females)
        males = self.stats['males'] = len(self.males)
        self.stats['users'] = females + males

        print(self.stats)

    def _classify_tweet(self, user_screen_name, text, gender, confidence):
        fields = [user_screen_name, confidence, text]

        if gender == 'Female':
            self.females[user_screen_name] += 1
            self.stats['female_tweets'] += 1
            self._females_writer.writerow(fields)
        else:
            self.males[user_screen_name] += 1
            self.stats['male_tweets'] += 1
            self._males_writer.writerow(fields)

        self.stats['tweets_classified'] += 1

    def _apply_face_recognition(self, gender, confidence, tweet):
        """
        Apply facial recognition over the profile image of tweet's author.

        If the gender match and the new confidence is higher, the confidence value is updated.

        Params:
            gender: Original gender detected.
            confidence: Original confidence.
            tweet: Tweet being processed.

        Returns:
            New confidence if altered and the original one if not.
        """
        profile_image = tweet['user']['profile_image_url'].replace('_normal', '')
        answer = self._faces.get_gender_and_confidence(profile_image)
        if answer is not None:
            face_gender, face_confidence = answer
            if face_gender == gender and face_confidence > confidence:
                confidence = face_confidence
        return confidence

    def _validate_file(self, dataset):
        print('Validating dataset')
        tweets_counter = 0
        with open(dataset, encoding='utf-8') as file:
            for line in file:
                try:
                    json.loads(line)
                except ValueError:
                    raise ValueError('The specified dataset contains invalid JSON objects')

                tweets_counter += 1
        self.stats['tweets'] = tweets_counter

    def _get_tweets_objects(self, file):
        for line in file:
            try:
                yield json.loads(line)
            except ValueError:
                self.stats['invalid_lines'] += 1

    def _prepare_result_files(self, path):
        """
        Create the given path (concatenating current date if already exists) and two files to
        store classification results on TSV format.

        Params:
            directory (string): Directory where to save results.
        """
        print('Preparing result files')
        self._females_file = open(os.path.join(path, 'females.tsv'), 'w+', encoding='utf-8')
        self._males_file = open(os.path.join(path, 'males.tsv'), 'w+', encoding='utf-8')
        self._females_writer = csv.writer(self._females_file, delimiter='\t')
        self._males_writer = csv.writer(self._males_file, delimiter='\t')

    def _show_remaining_time(self, tweets_processed):
        self._millis_elapsed += (datetime.datetime.now() - self._last_measured_time).total_seconds() * 1000
        millis_to_finish = (self._millis_elapsed / tweets_processed) * (self.stats['tweets'] - tweets_processed)
        self._last_measured_time = datetime.datetime.now()
        print(tweets_processed, 'processed. Estimated seconds to finish:', millis_to_finish / 1000,
              '(' + str(self._last_measured_time + datetime.timedelta(milliseconds=millis_to_finish)) + ')', end='\r')