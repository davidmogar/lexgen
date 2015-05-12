lexgen
======

Lexgen is a Python tool to generate valid lexicons for `twixer <https://github.com/davidmogar/twixer>`_.

Usage
-----

The tool can be used from the command line. These are all available options:
::
  
  usage: __main__.py [-h] [--faces] [--confidence N] [--lexicon-percentage N]
                   [--surnames] [--remove-outliers] dataset

positional arguments:
  dataset               file with JSON objects to be processed

optional arguments:
  -h, --help            show this help message and exit
  --faces               apply facial recognition over profile images
  --confidence N        minimal confidence for a valid recognition
                        (default=0.75)
  --lexicon-percentage N
                        Percentage of words to get from the generated lexicon
  --surnames            require fullnames (at least one surname)
  --remove-outliers     remove outliers before generate training and test
                        datasets

