import argparse
import collections
import csv
import datetime
import json
import operator
import os

from normalizr import Normalizr
from .classifier import ChickSexer
from .trimmer import Trimmer
from .utils import rootLogLikelihoodRatio


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
    path += '-lp' + str(args.lexicon_percentage)
    path = os.path.join(BASE_DIR, path, str(datetime.datetime.now().timestamp()))

    os.makedirs(path)

    return path


def filter_lexicon(lexicon, percentage):
    """
    Filters the lexicon received as parameter deleting values outside of the given percentage.

    Params:
        lexicon (dict): Lexicon to filter.
        percentage (float): Percentage of words to grab from each gender.

    Returns:
        The filtered lexicon.
    """
    print('Filtering lexicon')
    filtered_lexicon = {}
    female_words, male_words = 0, 0

    # Get female and male words count.
    for word in lexicon:
        if lexicon[word] > 0:
            female_words += 1
        else:
            male_words += 1

    # Calculate limits (number of words to ignore and grab from each set)
    ignore = female_words - (female_words * percentage)
    grab = male_words * percentage
    for word, llr in sorted(lexicon.items(), key=operator.itemgetter(1)):
        if grab >= 0:
            grab -= 1
            filtered_lexicon[word] = llr
        else:
            if llr >= 0:
                if ignore >= 0:
                    ignore -= 1
                else:
                    filtered_lexicon[word] = llr

    return filtered_lexicon


def generate_lexicon(results_path):
    """
    Generates a lexicon from the training datasets.

    Return:
        The generated lexicon as a dictionary with words and llr value for each one.
    """
    print('Generating lexicon')
    females_words_freq, total_female_words = get_word_frequencies(os.path.join(results_path, 'females-training.tsv'))
    males_words_freq, total_male_words = get_word_frequencies(os.path.join(results_path, 'males-training.tsv'))

    words = set(females_words_freq.keys())
    words.update(set(males_words_freq.keys()))

    lexicon = {}
    for word in words:
        lexicon[word] = rootLogLikelihoodRatio(females_words_freq[word], males_words_freq[word], total_female_words, total_male_words)

    return lexicon


def get_word_frequencies(dataset):
    """
    Get text from tweets in the given dataset, normalize them and generates a compute its words frequency.

    Params:
        dataset (string): Path to the dataset to process.

    Returns:
        A dictionary with word frequencies in the given dataset and a the number of words found.
    """
    word_frequencies = collections.defaultdict(int)

    total_words = 0
    with open(dataset, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.split('\t')
            if len(fields) == 3:
                for word in normalizr.normalize(fields[2].lower(), normalizations).split():
                    total_words += 1
                    word_frequencies[word] += 1

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
    parser.add_argument('--lexicon-percentage', metavar='N', type=float, default=0.5,
                        help="Percentage of words to get from the generated lexicon")
    parser.add_argument('--surnames', action='store_true', help='require fullnames (at least one surname)')
    parser.add_argument('--remove-outliers', action='store_true',
                        help='remove outliers before generate training and test datasets')

    return parser.parse_args()


def persist_lexicon(path, lexicon):
    """
    Persist the given lexicon to the path received as parameter.

    Params:
        path (string): Path where to save the lexicon.
        lexicon (dict): Lexicon to persist.
    """
    print('Persisting lexicon')
    with open(os.path.join(path, 'lexicon.tsv'), 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for word, llr in sorted(lexicon.items(), key=operator.itemgetter(1)):
            writer.writerow([word, llr])


def persist_test_results(path, females_pr, females_ex, males_pr, males_ex):
    """
    Store tests results in tests file.

    Path:
        path (string): Path to results directory.
        females_pr (float): Calculated female recognition precision.
        females_ex (float): Calculated female recognition exhaustiveness.
        males_pr (float): Calculated male recognition precision.
        males_ex (float): Calculated male recognition exhaustiveness.
    """
    print('Persisting test results')
    results = collections.OrderedDict()
    results['females_precision'] = females_pr
    results['females_exhaustiveness'] = females_ex
    results['males_precision'] = males_pr
    results['males_exhaustiveness'] = males_ex

    with open(os.path.join(path, '../..', 'tests.tsv'), 'a+', encoding='utf-8') as file:
        file.write(path[path.rfind('/') + 1:] + '\t' + json.dumps(results) + '\n')


def test_lexicon(dataset, lexicon, expected_female):
    """
    Test a lexicon against the given dataset calculating its precision and exhaustiveness.

    Params:
        dataset (string): Path to the dataset to use on this test.
        lexicon (dict): Lexicon to test.
        expected_female (boolean): A boolean value indicating if female tweets are expected.

    Returns:
        The precision and exhaustiveness of this lexicon against the given dataset.
    """
    female_tweets, male_tweets, unclassified = 0, 0, 0

    with open(dataset, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.split('\t')
            if len(fields) == 3:
                female_words, male_words = 0, 0
                for word in normalizr.normalize(fields[2].lower(), normalizations).split():
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

    classified = female_tweets + male_tweets
    precision = (female_tweets if expected_female else male_tweets) / classified
    exhaustiveness = classified / (classified + unclassified)

    return precision, exhaustiveness


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

    lexicon = generate_lexicon(results_path)
    lexicon = filter_lexicon(lexicon, args.lexicon_percentage)
    persist_lexicon(results_path, lexicon)
    females_pr, females_ex = test_lexicon(os.path.join(results_path, 'females-test.tsv'), lexicon, True)
    males_pr, males_ex = test_lexicon(os.path.join(results_path, 'males-test.tsv'), lexicon, False)
    persist_test_results(results_path, females_pr, females_ex, males_pr, males_ex)


