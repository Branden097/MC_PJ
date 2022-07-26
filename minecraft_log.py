import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials as sac
import re
import gzip

auth_json = 'minecraft-357407-fbea91beb3ee.json'

gs_scopes = ['https://spreadsheets.google.com/feeds']

cr = sac.from_json_keyfile_name(auth_json, gs_scopes)

gc = gspread.authorize(cr)

gsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rCPCPSuPYjyDg4jfGbMVZmh-cOli4xoPIca5nwfvam4/edit#gid=0')

wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rCPCPSuPYjyDg4jfGbMVZmh-cOli4xoPIca5nwfvam4/').worksheet("工作表2")

def un_gz_rt_gs(file_name):
    f_name = file_name.replace(".gz", "")
    g_file = gzip.GzipFile(file_name)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()

    date = f_name[0:10]

    result = []
    # Open File
    f = open(f_name, 'r', encoding="utf-8")
    for log in iter(f):
        if 'was slain by' in log:
            time = (log[1:9],)
            fight = re.findall(r"(\w*) was slain by (\w*)", log)[0]
            # Add new ROW
            result += [time + fight]

    df = pd.DataFrame(result, columns = ['time', 'loser', 'winner'])

    for n in range(len(df)):
        df.iloc[n]['time'] = str(date) +' '+df.iloc[n][time] 

    f.close()

    fmt = cellFormat( horizontalAlignment = 'CENTER' )
    format_cell_range(wks, 'A:C', fmt)

    set_with_dataframe(wks, df)

un_gz_rt_gs('2022-07-23-1.log.gz') 
