import os
import sys
import json
import time
import shutil
import sqlite3
import numpy as np
import pandas as pd
import pprint as pp
import datetime as dt
from sqlalchemy import create_engine
import flat_table


def title():
    the_title = """
dP                       dP                    dP   .d888888                                           dP           
88                       88                    88  d8'    88                                           88           
88       .d8888b..d8888b.88  .dP .d8888b..d888b88  88aaaaa88a.d8888b..d8888b..d8888b.dP    dP88d888b.d8888P.d8888b. 
88       88ooood888'  `8888888"  88ooood888'  `88  88     88 88'  `""88'  `""88'  `8888    8888'  `88  88  Y8ooooo. 
88       88.  ...88.  .8888  `8b.88.  ...88.  .88  88     88 88.  ...88.  ...88.  .8888.  .8888    88  88        88 
88888888P`88888P'`88888P8dP   `YP`88888P'`88888P8  88     88 `88888P'`88888P'`88888P'`88888P'dP    dP  dP  `88888P' 
                                                                                                                    
                                                                                                                   
    """
    print(the_title)



# additional help
def usage():
    msg = "Place dehashed API responses into the 'query_results' folder for program to read. Each database will have its own self-titled directory where all relevant files will be stored.\n Usage example: 'python3 -n dehashed_results.json -db company_name'"
    print(msg)

PROG_HOME = os.getcwd()
db_dir = 'databases'
raw_dir = 'query_results'


# Get OS to determine how to construct object paths
def get_file_arch():
    if os.name == 'nt':
        sep = '\\'
    else:
        sep = '/'
    return sep


sep = get_file_arch()
db_dir_path = PROG_HOME + sep + db_dir
raw_dir_path = PROG_HOME + sep + raw_dir


# check if directory exists
def check_dir(dir_name):
    return os.path.isdir(dir_name)


# check if file exists
def check_file(file_name):
    return os.path.isfile(file_name)

# make necessary folders
# databases
if check_dir(db_dir) == False:
    os.mkdir(db_dir)

# query results
if check_dir(raw_dir) == False:
    os.mkdir(raw_dir)


def db_path(dir_name):
    return db_dir_path + sep + dir_name


def add_date_column(df):
    today = str(dt.datetime.now())
    df['DateAdded'] = ''


# write pandas dataframe to a file
def df_to_file(in_df, filename):
    with open(filename, 'w') as f:
        dfAsString = in_df.to_string(header=True, index=True)
        f.write(dfAsString)


# write dataframe to csv file
def df2csv(df, filename):
    df.to_csv(filename, index=False, header=True)


# write dataframne to json
def df_to_json(in_df, filename):
    df_temp = in_df.to_json(orient='records', indent=4)
    with open(filename, 'w') as f:
        f.write(df_temp)


# create database and table
def create_database(db_name, df_name):
    conn = sqlite3.connect(db_name)
    df_name.to_sql('leaked_accounts', con=conn,
                      if_exists='replace', index=False)
    conn.commit()
    conn.close()


# load database into a dataframe
def read_table_alchemy(database_file):
    cnx = create_engine(f'sqlite:///{database_file}').connect()
    df = pd.read_sql_table('leaked_accounts', cnx)
    return df


# look @ def name
def create_backup(__file__):
    sep = get_file_arch()
    bak_filename = __file__ + '.bak'
    target_dir = os.path.abspath(os.getcwd())
    og = target_dir + sep + __file__
    new = target_dir + sep + bak_filename
    shutil.copyfile(og, new)


def exit_msg(dirname):
    print('Program successfully executed!')
    time.sleep(1)
    print(f'All files and reports:  {dirname}')
