import argparse
import collections
import csv
import datetime
import operator
import os

from normalizr import Normalizr
from .classifier import ChickSexer
from .trimmer import Trimmer
from .utils import remove_twitter_mentions, rootLogLikelihoodRatio


BASE_DIR = os.path.dirname(__file__)
MIN_CONFIDENCE = 0.75

normalizr = Normalizr()
exclusions = set([u'\N{LATIN CAPITAL LETTER N WITH TILDE}', u'\N{LATIN SMALL LETTER N WITH TILDE}',
                                  u'\N{LATIN CAPITAL LETTER C WITH CEDILLA}', u'\N{LATIN SMALL LETTER C WITH CEDILLA}'])
normalizations = [
    ('replace_urls', {'replacement': ' '}),
    'remove_stop_words',
    'remove_accent_marks',
    ('replace_emojis', {'replacement': ' '}),
    ('replace_symbols', {'excluded': exclusions, 'replacement': ' '}),
    ('replace_punctuation', {'replacement': ' '}),
    'remove_extra_whitespaces',
]

def create_results_path(args):
    """
    Create a directory to store all files.

    Params:
        args (argparse.Namespace): Execution arguments.

    Return:
        Path of the created directory.
    """
    path = '../data/'
    path += 'f' if args.faces else 'nf'
    path += '-s' if args.surnames else '-ns'
    path += '-c' + str(args.confidence)
    path += '-ro' if args.remove_outliers else '-nro'
    path = os.path.join(BASE_DIR, path, str(datetime.datetime.now().timestamp()))

    os.makedirs(path)

    return path


def filter_lexicon(lexicon, percentage):
    print('Filtering lexicon')
    filtered_lexicon = {}
    female_words, male_words = 0, 0

    for word in lexicon:
        if lexicon[word] > 0:
            female_words += 1
        else:
            male_words += 1

    female_words_limit = female_words - (female_words * percentage)
    male_words_limit = male_words * percentage
    grabbed, ignored = 0, 0
    for word, llr in sorted(lexicon.items(), key=operator.itemgetter(1)):
        if grabbed < male_words_limit:
            grabbed += 1
            filtered_lexicon[word] = llr
        else:
            if llr >= 0:
                if ignored > female_words_limit:
                    filtered_lexicon[word] = llr
                else:
                    ignored += 1

    return filtered_lexicon


def generate_lexicon(results_path, percentage):
    print('Generating lexicon')
    females_words_freq, total_female_words = get_word_frequencies(os.path.join(results_path, 'females-training.tsv'))
    males_words_freq, total_male_words = get_word_frequencies(os.path.join(results_path, 'males-training.tsv'))

    words = set(females_words_freq.keys())
    words.update(set(males_words_freq.keys()))

    lexicon = {}
    for word in words:
        lexicon[word] = rootLogLikelihoodRatio(females_words_freq[word], males_words_freq[word], total_female_words, total_male_words)

    return filter_lexicon(lexicon, percentage)


def get_word_frequencies(dataset):
    word_frequencies = collections.defaultdict(int)

    total_words = 0
    with open(dataset, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.split('\t')
            if len(fields) == 3:
                for word in normalizr.normalize(fields[2], normalizations).split():
                    total_words += 1
                    word_frequencies[word.lower()] += 1

    return word_frequencies, total_words


def parse_arguments():
    """
    Parse input arguments and store them in a global variable.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Generates a lexicon for gender recognition.')
    parser.add_argument('dataset', help='file with JSON objects to be processed')
    parser.add_argument('--faces', action='store_true', help='apply facial recognition over profile images')
    parser.add_argument('--confidence', metavar='N', type=float, default=0.75,
                        help="minimal confidence for a valid recognition (default=0.75)")
    parser.add_argument('--surnames', action='store_true', help='require fullnames (at least one surname)')
    parser.add_argument('--remove-outliers', action='store_true',
                        help='remove outliers before generate training and test datasets')

    return parser.parse_args()


def persist_lexicon(path, lexicon):
    print('Persisting lexicon')
    with open(os.path.join(path, 'lexicon.tsv'), 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for word, llr in sorted(lexicon.items(), key=operator.itemgetter(1)):
            writer.writerow([word, llr])


def test_lexicon(dataset, lexicon):
    female_tweets, male_tweets, unclassified = 0, 0, 0

    with open(dataset, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.split('\t')
            if len(fields) == 3:
                female_words, male_words = 0, 0
                for word in normalizr.normalize(fields[2], normalizations).split():
                    if word in lexicon:
                        if lexicon[word] > 0:
                            female_words += 1
                        else:
                            male_words += 1

                if female_words == male_words:
                    unclassified += 1
                elif female_words > male_words:
                    female_tweets += 1
                else:
                    male_tweets += 1

    print('precision', male_tweets / (female_tweets + male_tweets))
    print('exhaustivity', (female_tweets + male_tweets) / (female_tweets + male_tweets + unclassified))


def validate(args):
    """
    Validate environment to check if the execution can continue.

    Returns:
        True if all is valid, False otherwise.
    """
    if not os.access(BASE_DIR, os.W_OK):
        print('ERROR: Base directory is not writable')
        return False
    if not os.path.isfile(args.dataset):
        print('ERROR: Given dataset doesn\'t exists')
        return False

    return True


def main():
    args = parse_arguments()

    if not validate(args):
        exit()

    results_path = create_results_path(args)

    classifier = ChickSexer()
    classifier.classify(args.dataset, results_path, args.faces, args.confidence, args.surnames)

    trimmer = Trimmer(results_path)
    if args.remove_outliers:
        trimmer.remove_outliers()

    trimmer.split_datasets(0.8)

    lexicon = generate_lexicon(results_path, 0.25)
    persist_lexicon(results_path, lexicon)
    test_lexicon(os.path.join(results_path, 'males-test.tsv'), lexicon)


