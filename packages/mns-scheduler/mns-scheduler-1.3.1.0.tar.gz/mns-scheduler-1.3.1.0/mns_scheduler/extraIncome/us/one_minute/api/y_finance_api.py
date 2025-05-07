import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

proxy = 'http://127.0.0.1:7890'

os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

import yfinance as yf


def get_us_one_minute(symbol, start_time, end_time):
    yf_ticker = yf.Ticker(symbol)
    df = yf_ticker.history(period='5d', interval='1m',
                           start=start_time, end=end_time, prepost=True)
    df = df[[
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]]
    df['time'] = df.index
    df.columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "time",
    ]
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['str_day'] = df['time'].str.slice(0, 10)
    df['minute'] = df['time'].str.slice(11, 19)
    return df
    # df_test = df.loc[df['str_day'] == '2025-04-30']
    # print(sum(df_test['volume']))
    # sum(df.loc[(df['str_day'] == '2025-04-30') & (df['time'] > '16:00:00')]['volume'])


if __name__ == '__main__':
    get_us_one_minute('QQQ', '2025-05-01', '2025-05-07')
