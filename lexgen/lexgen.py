import argparse
import datetime
import os

from .classifier import ChickSexer
from .trimmer import Trimmer


BASE_DIR = os.path.dirname(__file__)
MIN_CONFIDENCE = 0.75


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


