import json
import pandas as pd
import seaborn as sns
import sqlite3 as sql3

def write_to_file(in_dataframe, out_file):
    dataset = sns.load_dataset(in_dataframe)
    dataset.to_json(out_file)


# def df_to_dict(dataframe, dict_name):

def what_type(obj):
    print(type(obj))


def write_stuff_to_file(filename, dict):
    with open(filename, 'a') as f:
        for key, value in dict.items():
            a = str(key)
            b = ' : '
            c = str(value)
            inst = a+b+c+'\n'
            f.write(inst)


def df_to_file(in_df, filename):
    with open(filename, 'a') as f:
        dfAsString = in_df.to_string(header=True, index=True)
        f.write(dfAsString)


# https: // pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
# use this for database stuff
def db_conn(db_name):
    my_conn = sql3.connect(db_name)
