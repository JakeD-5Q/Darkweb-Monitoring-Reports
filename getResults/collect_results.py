import argparse
import json
import pandas as pd
import numpy as np
import JSONfunctions
import seaborn as sns
import pprint as pp

help_text = "This program is designed to keep track of Dehashed API query results and to make it easier to view and share when there are new entries. To run this program, an argument must be supplied giving the path to the most recent query results (in JSON format) so that it can be compared to the database of past query results. First time use will create the database and store all entries into it."


parser = argparse.ArgumentParser(description='Keep track of company related accounts that have had their \
    credentials spotted on the darkweb')


# parser.add_argument('--compare',
#                     nargs=2,
#                     type=argparse.FileType('r')
#                     help='Enter the path to the two JSON files you want to compare')

# may do nargs, will have to check how many args provided
# if more than one, then will perform compare functions
parser.add_argument('-n', '--newfile',
                    help='path to new file',
                    required=True)

# parser.add_argument('-p', '--past',
#                     help='path to old results, compare to this file',
#                     )

parser.add_argument('-o', '--output',
                    nargs='?', type=argparse.FileType('w'), default='out.json',
                    help='output file, in JSON format')

args = parser.parse_args()
infile = args.newfile
out_file = args.output


df = pd.read_json(infile)
# notdataframe = df.to_string()

# print(notdataframe)

# 'balance'
# num = str(df.at[0, 'balance'])
status = str(df.at[0, 'success'])
duration = str(df.at[0, 'took'])
total = str(df.at[0, 'total'])

print(f"Query success: {status}")
print(f'Total results: {total}')
print(f"Took {duration}")

# 'entries'
Entry_fields = ["id", "email", "ip_address", \
    "username", "password", "hashed_password", \
    "name", "vin", "address", "phone", "database_name"]

# split field into results fiels?
df_entries = pd.DataFrame(df['entries'].values.tolist(), index=df.index)
print(df_entries)
# print(type(df_entries))

entries_file = "entries_file3.txt"
JSONfunctions.df_to_file(df_entries, entries_file)

entries_dict = df_entries.to_dict(orient='index')
# print(entries_dict)

