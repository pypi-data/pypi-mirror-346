import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.component.em.em_stock_info_api as em_stock_info_api
from loguru import logger
import time
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_scheduler.extraIncome.a_stock.one_minute.common.db_create_index as db_create_index
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.alpha_vantage_api as alpha_vantage_api
import pandas as pd
from functools import lru_cache

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)
from datetime import datetime


def sync_us_stock_one_minute(now_year, now_month):
    real_time_quotes_all_us = em_stock_info_api.get_us_stock_info()
    real_time_quotes_all_us_stocks = real_time_quotes_all_us.loc[real_time_quotes_all_us['flow_mv'] != 0]
    real_time_quotes_all_us_stocks = real_time_quotes_all_us_stocks.sort_values(by=['amount'], ascending=False)

    #  todo 改集合名字
    col_name = extra_income_db_name.US_STOCK_MINUTE_K_LINE_BFQ
    col_name = col_name + '_' + str(now_year)
    # 创建索引
    db_create_index.create_index(mongodb_util_27017, col_name)

    for stock_one in real_time_quotes_all_us_stocks.itertuples():

        symbol = stock_one.symbol
        # simple_symbol = int(stock_one.simple_symbol)
        # code = str(simple_symbol) + '.' + symbol
        list_date = str(stock_one.list_date)
        list_date_year = int(list_date[0:4])
        if list_date_year > now_year:
            continue
        try:

            now_date = datetime.now()
            if net_work_check(now_date):
                # 休眠 6分钟
                time.sleep(5 * 60)

            df = alpha_vantage_api.sync_one_minute_data(symbol, now_month)
            df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['str_day'] = df['time'].str.slice(0, 10)
            df['minute'] = df['time'].str.slice(11, 19)
            df['_id'] = symbol + "_" + df['time']
            df['symbol'] = symbol
            df_export_df = df.copy()
            export_original_data(df_export_df, symbol, now_year, now_month)
            handle_pan_qian_or_hou_data(df, symbol, col_name)

        except BaseException as e:
            time.sleep(1)
            fail_dict = {
                '_id': symbol + '_' + now_month,
                'symbol': symbol,
                'now_year': now_year,
                'now_month': now_month
            }
            fail_df = pd.DataFrame(fail_dict, index=[1])

            mongodb_util_27017.insert_mongo(fail_df, 'us_stock_one_minute_k_line_bfq_fail')
            logger.error("同步股票分钟数据出现异常:,{},{},{}", e, symbol, now_month)
        logger.info("同步股票分钟票数据完成:{},{}", stock_one.symbol, stock_one.name)


def handle_pan_qian_or_hou_data(df, symbol, col_name):
    hand_pan_hou_data(df.copy(), symbol, col_name)
    hand_pan_qian_data(df.copy(), col_name)
    handle_middle_data(df.copy(), col_name)


def handle_middle_data(df_copy, col_name):
    df = df_copy.copy()
    df = df.loc[df['minute'] < '16:00:00']
    df = df.loc[df['minute'] > '09:30:00']
    mongodb_util_27017.insert_mongo(df, col_name)


def hand_pan_qian_data(df_copy, col_name):
    df = df_copy.copy()
    df_pan_qian_init = df.loc[df['minute'] == '09:30:00']
    del df_pan_qian_init['volume']
    pan_qian_data = df.loc[df['minute'] <= '09:30:00']
    pan_qian_data_group_df = pan_qian_data.groupby('str_day')['volume'].sum().reset_index()

    pan_qian_data_group_df = pan_qian_data_group_df.set_index(['str_day'], drop=True)
    df_pan_qian_init = df_pan_qian_init.set_index(['str_day'], drop=False)

    df_pan_qian_init = pd.merge(pan_qian_data_group_df, df_pan_qian_init,
                                how='outer',
                                left_index=True, right_index=True)

    mongodb_util_27017.insert_mongo(df_pan_qian_init, col_name)


def hand_pan_hou_data(df_copy, symbol, col_name):
    df = df_copy.copy()
    df_pan_hou_init = df.loc[df['minute'] == '16:00:00']
    k_line_trade_df = query_k_line(symbol)
    trade_date_list = list(df_pan_hou_init['str_day'])

    k_line_trade_df = k_line_trade_df.loc[k_line_trade_df['date'].isin(trade_date_list)]

    k_line_trade_df = k_line_trade_df.rename(columns={'volume': "k_line_volume"})

    # 收盘前的
    df = df.loc[df['minute'] < '16:00:00']
    total_volume_df = df.groupby('str_day')['volume'].sum().reset_index()
    total_volume_df = total_volume_df.rename(columns={'volume': "total_volume"})

    total_volume_df = total_volume_df.set_index(['str_day'], drop=False)

    k_line_trade_df = k_line_trade_df.set_index(['date'], drop=True)

    pan_hou_diff_df = pd.merge(total_volume_df, k_line_trade_df,
                               how='outer',
                               left_index=True, right_index=True)

    pan_hou_diff_df['volume'] = pan_hou_diff_df['k_line_volume'] - pan_hou_diff_df['total_volume']

    del df_pan_hou_init['volume']

    pan_hou_diff_df = pan_hou_diff_df.set_index(['str_day'], drop=True)
    del pan_hou_diff_df['k_line_volume']
    del pan_hou_diff_df['total_volume']

    df_pan_hou_init = df_pan_hou_init.set_index(['str_day'], drop=False)

    df_pan_hou_result = pd.merge(pan_hou_diff_df, df_pan_hou_init,
                                 how='outer',
                                 left_index=True, right_index=True)
    mongodb_util_27017.insert_mongo(df_pan_hou_result, col_name)


def export_original_data(df, symbol, year, now_month):
    path = r'H:\us_stock\one_minute\{}'.format(year)
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + '\{}'.format(now_month)
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = path + '\{}.csv'.format(symbol)
    if data_frame_util.is_not_empty(df):
        del df['str_day']
        del df['minute']
        del df['_id']
        del df['symbol']
    df.to_csv(file_name, index=False, encoding='utf-8')


@lru_cache()
def query_k_line(symbol):
    query = {'symbol': symbol}
    query_field = {"volume": 1, 'date': 1, '_id': 0}
    return mongodbUtilV2_27019.find_query_data_choose_field(extra_income_db_name.US_STOCK_DAILY_QFQ_K_LINE, query,
                                                            query_field)


def net_work_check(now_date):
    hour = now_date.hour
    minute = now_date.minute
    if hour == 7 and minute == 34:
        return True
    elif hour == 9 and minute == 59:
        return True
    elif hour == 10 and minute == 29:
        return True
    elif hour == 10 and minute == 59:
        return True
    elif hour == 12 and minute == 49:
        return True
    elif hour == 13 and minute == 28:
        return True
    elif hour == 13 and minute == 58:
        return True
    elif hour == 14 and minute == 28:
        return True
    elif hour == 15 and minute == 1:
        return True
    else:
        return False


def sync_by_year(begin_year):
    begin_month = 12
    while begin_month > 0:
        if begin_month < 10:
            str_month = '0' + str(begin_month)
        else:
            str_month = str(begin_month)
        str_month = str(begin_year) + '-' + str_month
        sync_us_stock_one_minute(begin_year, str_month)
        begin_month = begin_month - 1
        logger.error("同步完成月份:{}", str_month)


if __name__ == '__main__':
    # k_line_df = query_k_line('TSLA')
    sync_by_year(2024)
