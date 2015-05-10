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

        self._characters_to_clean = 0

    def classify(self, dataset, path, detect_faces=False, min_confidence=0.75, require_surnames=False,
                 tweets_until_time=1000):
        """
        Classify tweets in the given dataset spliting them in two groups, females and males.

        Params:
            dataset (string): Path of the dataset to process.
            path (string): Path whwere to save results.
            detect_faces (boolean): A value indicating if facial recognition should be performed.
            min_confidence (float): Minimal confidence to consider a gender prediction valid .
            require_surnames (boolean): A value indicating whether to require surnames or not.
            tweets_until_stats: Number of tweets to process between each time report.
        """
        self._validate_file(dataset)
        self._prepare_result_files(path)
        self._millis_elapsed = 0
        self._last_measured_time = datetime.datetime.now()

        print('Starting dataset classification')
        tweets_processed = 0
        with open(dataset, encoding='utf-8') as file:
            for tweet in self._get_tweets_objects(file):
                tweets_processed += 1
                prediction = self._genderator.guess_gender(tweet['user']['name'])

                if prediction is not None and (not require_surnames or prediction['surnames']):
                    confidence = prediction['confidence']
                    gender = prediction['gender']

                    if detect_faces and (confidence < min_confidence):
                        confidence = self._apply_face_recognition(gender, confidence, tweet)

                    if confidence >= min_confidence:
                        self._classify_tweet(tweet['user']['screen_name'], tweet['text'], gender, confidence)

                if tweets_processed > 1 and tweets_processed % tweets_until_time == 0:
                    self._show_remaining_time(tweets_processed)

        self.stats['tweets_processed'] = tweets_processed
        self._females_file.close()
        self._males_file.close()

    def show_stats(self):
        """
        Show stored stats.
        """
        females = self.stats['females'] = len(self.females)
        males = self.stats['males'] = len(self.males)
        self.stats['users'] = females + males

        print(dict(self.stats))

    def _classify_tweet(self, user_screen_name, text, gender, confidence):
        """
        Classify a tweet in one of the two result datasets (females or males).

        Params:
            user_screen_name (string): User's screen name as found in JSON object.
            text (string): Tweet's text.
            gender (string): User's gender.
            confidence (string): Calculated confidence.
        """
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
        """
        Validates file to be sure that all lines are valid JSON objects and store the lines count.

        Params:
            dataset (string): Path of the dataset file.
        """
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
        """
        Filter file lines getting only valid JSON objects.

        Params:
            file (File): File to filter.
        """
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
        """
        Print remaining time to finish classification.

        Params:
            tweets_processed (int): Number of tweets processed.
        """
        self._millis_elapsed += (datetime.datetime.now() - self._last_measured_time).total_seconds() * 1000
        millis_to_finish = (self._millis_elapsed / tweets_processed) * (self.stats['tweets'] - tweets_processed)
        self._last_measured_time = datetime.datetime.now()

        seconds_to_finish = '{:.2f}'.format(millis_to_finish / 1000)
        percentage_processed = '{:.2f}'.format(tweets_processed / self.stats['tweets'] * 100)
        finishing_date = self._last_measured_time + datetime.timedelta(milliseconds=millis_to_finish)

        print(' ' * self._characters_to_clean, end='\r')
        output = percentage_processed + '% processed, ' + seconds_to_finish + ' seconds to finish (' + str(finishing_date) + ')'
        self._characters_to_clean = len(output)
        print(output, end='\r')