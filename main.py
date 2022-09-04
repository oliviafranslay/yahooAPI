import time
from datetime import date
import datetime
import pandas as pd
import csv
import requests
import json

BASE_URL = 'http://localhost:8080'
ticker = []

with open('ticker.csv', 'r') as csvf:
    csvReader = csv.reader(csvf, delimiter=',')
    for row in csvReader:
        row = "".join(row)
        ticker.append(row)

period1 = int(time.mktime(date.today().timetuple()))
# period1 = int(time.mktime(datetime.datetime(2022, 6, 7, 23, 59).timetuple()))
# period2 = int(time.mktime(datetime.datetime(2022, 6, 25, 23, 59).timetuple()))
period2 = int(time.mktime(date.today().timetuple()))
interval = '1d' # 1d, 1m

frames = []
for i in ticker:
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{i}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    df = pd.read_csv(query_string)
    dfnew = df.rename(columns={'Date':'date', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close', 'Volume':'volume'})
    del dfnew['Adj Close']
    new_string = ''.join(char for char in i if char.isalnum())
    dfnew['underlyingTicker'] = new_string
    frames.append(dfnew)

result = pd.concat(frames)

result.to_csv('data.csv', index=False)

jsonArray = []
with open('data.csv') as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        jsonArray.append(row)

    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/marketdata", data=json.dumps(jsonArray), headers=headers)


















# dfnew.to_sql('marketdata', con=conn, if_exists='append', index=False)
# conn = psycopg2.connect(conn_string)
# conn.autocommit = True
# cursor = conn.cursor()
#
# sql1 = '''select * from data;'''
# cursor.execute(sql1)
# for i in cursor.fetchall():
#     print(i)
#
# # conn.commit()
# conn.close()


