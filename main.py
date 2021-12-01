import argparse
import pandas as pd
import numpy as np
import os
import time
import sqlite3
import pprint as pp
import program_functions as pf


# reports for the first run of this propgram
def make_database_report():
    # input file (newfile)
    pf.df_to_file(df_entries, 'first_import.txt')
    pf.df_to_json(df_entries, 'first_import.json')
    pf.df2csv(df_entries, 'first_import.csv')


# reports when database has already been created
def make_updated_reports():
    # new records (newfile - database)
    pf.df_to_file(df_diff, 'different_records.txt')
    pf.df_to_json(df_diff, 'different_records.json')
    pf.df2csv(df_diff, 'different_records.csv')


# ask if backup is wanted
def create_db_backup():
    # create backup
    ans = input("\n\nWant to create a backup of the database? (Y/n)\t")
    if ans == 'y' or ans == 'Y':
        pf.create_backup(db_name)
        print('\nBackup has been created.')
        time.sleep(1)
    else:
        print('Warning: no backup file created.\n')
        time.sleep(1)


help_text = "This program is designed to keep track of Dehashed API query results and to make it easier to view and share when there are new entries. To run this program, an argument must be supplied giving the path to the most recent query results (in JSON format) so that it can be compared to the database of past query results. First time use will create the database and store all entries into it.\
    ONLY FILES PLACED IN THE QUERY RESULTS FOLDER WILL BE READ!"

if __name__ == '__main__':
    pf.title()

    parser = argparse.ArgumentParser(description='Keep track of company related accounts that have had their \
        credentials spotted on the darkweb')

    parser.add_argument('-n', '--newfile',
                        help='path to new file',
                        required=True)

    parser.add_argument('-db', '--database',
                        help='path to database file',
                        required=True)

    # parsin'
    args = parser.parse_args()
    in_file = args.newfile
    db_dir = args.database 

    # constructing entity and location names
    out_dir = pf.db_path(db_dir)
    db_name = db_dir + '.db'
    in_file_path = 'query_results' + pf.get_file_arch() + in_file
    reports_dir = out_dir + pf.get_file_arch() + 'reports'

    # create folders for database and reports
    if pf.check_dir(out_dir) == False:
        os.mkdir(out_dir)
        os.mkdir(reports_dir)

    # load data into dataframe
    df = pd.read_json(in_file_path)
    # edit dataframe to only include leaked accounts
    df_entries = pd.DataFrame(df['entries'].values.tolist(), index=df.index)
    # df_date = pf.add_date_column(df_entries)
    # print(df_date.head())

    # cd into database file
    os.chdir(out_dir)

    # determine if database exists, if not create
    if pf.check_file(db_name) == True: # database exists and has records
        # get dataframe from database
        df_db = pf.read_table_alchemy(db_name)

        # separate new entires
        df_diff = pd.concat([df_db, df_entries]).drop_duplicates(keep=False)

        # append df_diff to database
        print('Comparing new entries with those already in the database...')
        pf.create_database(db_name, df_diff)
        time.sleep(2)
        print("Completed.")

        ans = input('\nSee preview? (Y/n)\t')
        if ans == 'y' or ans == 'Y':
            pp.pprint(df_diff.head())
        
        # make backup
        create_db_backup()

        # generate reports
        print("Generating reports...")
        time.sleep(1.5)
        os.chdir('reports')
        make_updated_reports()
   

        pf.exit_msg(reports_dir)
        
    else:
        print("Initializing and populating database...")
        time.sleep(2)
        pf.create_database(db_name, df_entries)
        print("Completed")

        ans = input('\nSee preview? (Y/n)\t')
        if ans == 'y' or ans == 'Y':
            pp.pprint(df_entries.head())

        # ask for backup
        create_db_backup()

        # generate report
        print("Generating reports...")
        time.sleep(1.5)
        os.chdir('reports')
        make_database_report()

        pf.exit_msg(reports_dir)

        







