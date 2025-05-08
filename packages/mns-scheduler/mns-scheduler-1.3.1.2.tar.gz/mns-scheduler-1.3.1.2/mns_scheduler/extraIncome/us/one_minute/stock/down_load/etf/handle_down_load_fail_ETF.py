import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

from loguru import logger
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.alpha_vantage_api as alpha_vantage_api

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)


def handle_fail_data():
    query = {"type": "ETF", }
    fail_df = mongodb_util_27017.find_query_data('us_stock_one_minute_down_load_fail', query)

    for stock_one in fail_df.itertuples():
        try:

            now_year = stock_one.now_year
            now_month = stock_one.now_month
            symbol = stock_one.symbol
            id_key = symbol + '_' + now_month
            path = r'F:\us_etf\one_minute\{}'.format(now_year)
            if not os.path.exists(path):
                os.makedirs(path)

            path = path + '\{}'.format(now_month)
            if not os.path.exists(path):
                os.makedirs(path)

            df = alpha_vantage_api.sync_one_minute_data(symbol, now_month)
            df = df.fillna(0)
            df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['str_day'] = df['time'].str.slice(0, 10)
            df['minute'] = df['time'].str.slice(11, 19)
            df['_id'] = symbol + "_" + df['time']
            df['symbol'] = symbol
            df_export_df = df.copy()
            export_original_data(df_export_df, symbol, path)
            logger.info("同步股票分钟票数据完成:{}", stock_one.symbol)
            query = {"_id": id_key}
            mongodb_util_27017.remove_data(query, 'us_stock_one_minute_down_load_fail')
        except BaseException as e:
            logger.error("同步股票分钟数据出现异常:,{},{},{}", e, symbol, now_month)


def export_original_data(df, symbol, path):
    file_name = path + '\{}.csv'.format(symbol)
    if data_frame_util.is_not_empty(df):
        df = df.dropna(subset=['_id'])
        del df['str_day']
        del df['minute']
        del df['_id']
        del df['symbol']
    df.to_csv(file_name, index=False, encoding='utf-8')


if __name__ == '__main__':
    handle_fail_data()
