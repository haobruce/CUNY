import pandas as pd
import os
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename


def open_csv():
    filename = askopenfilename()
    if os.path.splitext(filename)[1] != '.csv':
        print "Invalid file. Please select a .csv file."
        return None
    cars = pd.read_csv(filename, header=None)
    cars.columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    return cars


def save_csv(df):
    filename = asksaveasfilename() + '.csv'
    df.to_csv(filename)


def get_rank_dict():
    return {'low': 1, 'med': 2, 'high': 3, 'vhigh': 4}


def sort_by_safety(df, nrows=10):
    df['safety_num'] = df['safety'].map(get_rank_dict())
    # check if any NaN values appear after mapping
    if df['safety_num'].isnull().values.any():
        print "One or more rows contains unacceptable category values."
        return None
    df.sort_values(by='safety_num', inplace=True, ascending=False)
    df.drop('safety_num', inplace=True, axis=1)
    return df.head(nrows)


def sort_by_maint(df, nrows=15):
    df['maint_num'] = df['maint'].map(get_rank_dict())
    # check if any NaN values appear after mapping
    if df['maint_num'].isnull().values.any():
        print "One or more rows contains unacceptable category values."
        return None
    df.sort_values(by='maint_num', inplace=True, ascending=True)
    df.drop('maint_num', inplace=True, axis=1)
    return df.head(nrows)


def filter_sort_pandas(df):
    df = df[(df['buying'] == 'high') | (df['buying'] == 'vhigh')]
    df = df[(df['maint'] == 'high') | (df['maint'] == 'vhigh')]
    df = df[(df['safety'] == 'high') | (df['safety'] == 'vhigh')]
    df.sort_values(by='doors', inplace=True, ascending=True)
    return df


def filter_sort(df):
    filter_series = df['buying'].str.contains('high|vhigh', regex=True) & \
        df['maint'].str.contains('high|vhigh', regex=True) & \
        df['safety'].str.contains('high|vhigh', regex=True)
    df = df.loc[filter_series, ]
    df.sort_values(by='doors', inplace=True, ascending=True)
    return df


def filter_save(df):
    df = df[(df['buying'] == 'vhigh')]
    df = df[(df['maint'] == 'med')]
    df = df[(df['doors'] == '4')]
    df = df[(df['persons'] == '4')]
    save_csv(df)


if __name__ == "__main__":
    cars = open_csv()
    print sort_by_safety(cars)
    print sort_by_maint(cars)
    print filter_sort(cars)
    filter_save(cars)
