import re

"""

The get_confidence_score() function takes in a csv column name and column values 
passed in as a list and returns a confidence score by taking an average
on how likely each item in the column is a name.

input: string, string list
output: double

"""
def get_confidence_score(col_name, col_vals):
    col_name_check = ("name" in col_name.lower())

    scores = []
    col_vals = remove_lead_trail_space(col_vals)
    col_vals = remove_null(col_vals)

    for c in col_vals:
        scores.append(get_elem_score(col_name_check, c))

    scores = remove_outliers(scores)
    return sum(scores) / len(scores)


"""
The get_elem_score() function takes in a boolean denoting
whether 'name' was found in the column name and 
one element from the column list and returns a confidence score on
how the element is a name.

input: bool, string
output: double

"""
def get_elem_score(col_name_check, elem):
    name_formats = ["first last", "last, first", "first middle last", "last, first middle", "first m. last"]

    if col_name_check:
        score_multiplier = 1.0
    else:
        score_multiplier = 0.5

    name = elem.strip().lower()
    for format in name_formats:
        if re.match("^" + format.replace(".", "\.") + "$", name):
            return 100.0 * score_multiplier

    return 0.0


"""
The remove_null() function removes any null elements that may be in the column list.

input: string list
output: string list

"""
def remove_null(col_vals):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    col_vals = [elem for elem in col_vals if elem is not None] # remove None values
    col_vals = [elem for elem in col_vals if elem not in null_strings] # remove any strings denoting null values
    return col_vals


"""
The remove_lead_trail_space() function removes any leading and trailing spaces that may be in the strings of the column list.

input: string list
output: string list

"""
def remove_lead_trail_space(col_vals):
    col_vals = [elem.strip() for elem in col_vals] # remove leading and trailing spaces
    return col_vals


"""
The remove_outliers() function removes any elements that could be skewing the average
(elements that are 2 standard deviations away from the mean).

input: double list
output: double list

"""
def remove_outliers(scores):
    outliers = set()
    avg = sum(scores) / len(scores)
    standard_deviation = (sum([(s - avg)**2 for s in scores]) / len(scores))**(1/2)

    for s in scores:
        if (s < (avg - (standard_deviation*2)) or s > ((standard_deviation*2) + avg)):
            outliers.add(s)

    scores = [s for s in scores if s not in outliers]
    return scores
