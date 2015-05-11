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