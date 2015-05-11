import collections
import os
import random

from .utils import filter_dict_by_iqr


BASE_DIR = os.path.dirname(__file__)


class Trimmer:
    def __init__(self, path):
        self._datasets_path = path
        self._females = collections.defaultdict(int)
        self._males = collections.defaultdict(int)
        self._load_users_stats()

    def remove_outliers(self):
        """
        Remove outlier users (users with too many or few tweets).
        """
        print('Removing outliers')
        self._females = filter_dict_by_iqr(self._females)
        self._males = filter_dict_by_iqr(self._males)

    def split_datasets(self, training_set_percentage):
        """
        Splits both datasets (females.tsv and males.tsv) into training and test datasets.

        Params:
            training_set_percentage (float): Percentage of tweets that should go to training dataset.
        """
        print('Trimming datasets')
        self._split_dataset(self._females, os.path.join(self._datasets_path, 'females.tsv'), training_set_percentage)
        self._split_dataset(self._males, os.path.join(self._datasets_path, 'males.tsv'), training_set_percentage)

    def _split_dataset(self, users, dataset, training_set_percentage):
        """
        Split a dataset into training and test datasets.

        Params:
            users (dict): Valid users for the dataset with tweets count as values.
            dataset (string): Path to dataset to split.
            training_set_percentage (float): Percentage of tweets that should go to training dataset.
        """
        total_tweets = sum(list(users.values()))
        training_indexes = set(random.sample(range(total_tweets), int(total_tweets * training_set_percentage)))

        valid_tweets_processed = 0
        with open(dataset, 'r', encoding='utf-8') as file,\
                open(dataset.replace('.tsv', '-training.tsv'), 'w+', encoding='utf-8') as training_file,\
                open(dataset.replace('.tsv', '-test.tsv'), 'w+', encoding='utf-8') as test_file:
            for line in file:
                if line.split('\t')[0] in users:
                    if valid_tweets_processed in training_indexes:
                        training_file.write(line)
                    else:
                        test_file.write(line)
                    valid_tweets_processed += 1

    def _load_users_stats(self):
        """
        Load user stats from generated datasets.
        """
        with open(os.path.join(self._datasets_path, 'females.tsv'), 'r', encoding='utf-8') as file:
            for line in file:
                self._females[line.split('\t')[0]] += 1

        with open(os.path.join(self._datasets_path, 'males.tsv'), 'r', encoding='utf-8') as file:
            for line in file:
                self._males[line.split('\t')[0]] += 1
