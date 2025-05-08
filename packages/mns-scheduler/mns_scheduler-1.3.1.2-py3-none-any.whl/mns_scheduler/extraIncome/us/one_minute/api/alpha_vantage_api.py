import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from alpha_vantage.timeseries import TimeSeries

# 初始化TimeSeries对象
ts = TimeSeries(key='PP23H4H1059FTUK7', output_format='pandas')


# 开始月份 2000-01
def sync_one_minute_data(symbol, month):
    # 获取分钟数据（以苹果公司股票为例，60分钟间隔）
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full', month=month,
                                      extended_hours='true', adjusted='false')

    data['time'] = data.index
    data.columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "time",
    ]

    return data


if __name__ == '__main__':
    sync_one_minute_data('IBM', '2000-01')
