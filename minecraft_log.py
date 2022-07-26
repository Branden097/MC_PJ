# ! pip install gspread gspread-dataframe oauth2client gspread-formatting
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials as sac
import re
import gzip

# Set api key
auth_json = 'minecraft-357407-fbea91beb3ee.json'

# Set scopes
gs_scopes = ['https://spreadsheets.google.com/feeds']

# 以金鑰及操作範圍設定憑證資料
cr = sac.from_json_keyfile_name(auth_json, gs_scopes)

# 取得操作憑證
gc = gspread.authorize(cr)

# 以 url 開啟試算表
gsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rCPCPSuPYjyDg4jfGbMVZmh-cOli4xoPIca5nwfvam4/edit#gid=0')

# 選擇工作表1
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

    # uses DEFAULT_FORMATTER
    fmt = cellFormat( horizontalAlignment = 'CENTER' )
    format_cell_range(wks, 'A:C', fmt)

    # 寫入 Google Sheet
    set_with_dataframe(wks, df)

un_gz_rt_gs('2022-07-23-1.log.gz') 