import pandas as pd

def make_pandas(fname):
    """Makes a pandas dataset from the given csv file name. Changes data-types of numeric columns

    Arguments:
        fname {string} -- the csv files with CAPE data
    """
    assert fname == 'engineering.txt' or 'humanities.txt' or 'socialSciences.txt' or 'ucsd.txt', "Not a correct input file"
    colNames = ['Course Name', 'Summer?', 'Term', 'Enrolled', 'Evals Made', 'Recommend Class %', 'Recommend Prof %', 'Hrs/Week', 'GPA Expected', 'GPA Recieved']
    data = pd.read_csv(fname, names = colNames)
    data.apply(pd.to_numeric, errors='ignore')
    return data

def average_GPA(data, summer = True, year = 'all', expected = False):
    """Returns the average GPA either from all summer or non-summer courses. Can be cumulative or only courses from a certain year.
    Example: average_GPA(data, False, '09', True) will return the average expected GPA of all non-summer courses from 2009

    Arguments:
        data {DataFrame} -- DataFrame of CAPE data

    Keyword Arguments:
        summer {bool} -- True if average from summer courses, False if non-summer courses (default: {True})
        year {str} -- Year of GPA average desired (default: {'all'})
        expected {bool} -- True if expected GPA, False if recieved GPA (default: {False})
    """

    temp = df_trim_term(data, summer, year)
    if expected:
        return temp["GPA Expected"].mean()
    return temp["GPA Recieved"].mean()

def average_enrollment(data, summer = True, year = 'all'):
    """Returns the average enrollment number from all summer or non-summer courses. Can be cumulative or only courses from a certain year.
    Example: average_enrollment(data, True, '10') will return the average enrollment of all summer courses from 2010

    Arguments:
        data {DataFrame} -- DataFrame of CAPE data

    Keyword Arguments:
        summer {bool} -- True if average from summer courses, False if non-summer courses (default: {True})
        year {str} -- Year of average enrollment desired (default: {'all'})
    """

    temp = df_trim_term(data, summer, year)
    return temp['Enrolled'].mean()


def df_trim_term(data, summer, year):
    """Returns a DataFrame with only courses determined by the given parameters

    Arguments:
        data {DataFrame} -- DataFrame of CAPE data
        summer {bool} -- True if summer courses, False if non-summer courses
        year {str} -- Year desired
    """
    assert year == 'all' or '11' or '12' or '13' or '14' or '15' or '16' or '17', "Possible Years: 11-17"
    assert isinstance(data, pd.DataFrame), 'Given Data is not a Pandas DataFrame'
    assert isinstance(summer, bool), 'Incorrect Parameter (Boolean): Determines summer or non-summer courses'
    if year == 'all' and summer:
        temp = data[(data['Summer?'] == 'S')]
    elif year == 'all':
        temp = data[(data['Summer?'] == 'NS')]
    elif summer:
        temp = data[(data['Term'].str.contains(year)) & (data['Summer?'] == 'S')]
    else:
        temp = data[(data['Term'].str.contains(year)) & (data['Summer?'] == 'NS')]
    return temp