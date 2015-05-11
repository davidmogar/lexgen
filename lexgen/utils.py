import math


def percentile(values, percent, key=lambda x: x):
    """
    Find the percentile of a list of values.

    Params:
        values (list): Sorted list of values.
        percent (float): A value from 0.0 to 1.0.
        key (function): Optional key function to compute value from each value on list.

    Returns:
        The percentile of the values.
    """
    if not values:
        return None

    k = (len(values) - 1) * percent
    floor = math.floor(k)
    ceil = math.ceil(k)
    if floor == ceil:
        return key(values[int(k)])

    d0 = key(values[int(floor)]) * (ceil - k)
    d1 = key(values[int(ceil)]) * (k - floor)

    return d0 + d1


def filter_dict_by_iqr(dictionary):
    """
    Returns a new dictionary filtering values outside of the interquartile range.

    Params:
        dictionary (dict): Dictionary  to be filtered.

    Returns:
        A new dictionary without items outside of the interquartile range.
    """
    filtered_dict = {}
    values = sorted(set(dictionary.values()))

    first_quartile = percentile(values, 0.25)
    second_quartile = percentile(values, 0.75)

    for key in dictionary:
        if first_quartile <= dictionary[key] <= second_quartile:
            filtered_dict[key] = dictionary[key]

    return filtered_dict


def rootLogLikelihoodRatio(a, b, c, d):
    """
    Calculates the root log-likelihood ratio for two events.

    This implementation is based on LLR interpretation provided in the following
    paper (see table and equations in page 7):

    Java, Akshay, et al. "Why we twitter: understanding microblogging usage and
    communities." Proceedings of the 9th WebKDD and 1st SNA-KDD 2007 workshop on
    Web mining and social network analysis. ACM, 2007.
    Available at: http://aisl.umbc.edu/resources/369.pdf

    Params:
        a (int): Frequency of token of interest in dataset A.
        b (int): Frequency of token of interest in dataset B.
        c (int): Total number of observations in dataset A.
        d (int): Total number of observations in dataset B.

    Returns:
        The root log-likelihood ratio.
    """
    e1 = c * (a + b) / (c + d)
    e2 = d * (a + b) / (c + d)

    # Avoid division zero by replacing a or b by 1 if equal to 0
    result = math.sqrt(2 * (a * math.log(a / e1 or 1) + b * math.log(b / e2 or 1)))

    if a / c < b / d:
        result = -result

    return result