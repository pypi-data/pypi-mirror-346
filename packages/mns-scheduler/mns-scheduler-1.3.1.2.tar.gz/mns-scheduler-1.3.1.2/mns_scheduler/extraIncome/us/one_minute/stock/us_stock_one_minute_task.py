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
import mns_scheduler.extraIncome.a_stock.one_minute.common.symbol_handle_util as symbol_handle_util
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_scheduler.extraIncome.a_stock.one_minute.common.db_create_index as db_create_index
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.alpha_vantage_api as alpha_vantage_api
import pandas as pd
from functools import lru_cache

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)
def sync_us_stock_one_minute(now_year, now_month, begin_year):
    real_time_quotes_all_us = em_stock_info_api.get_us_stock_info()
    real_time_quotes_all_us_stocks = real_time_quotes_all_us.loc[real_time_quotes_all_us['flow_mv'] != 0]
    real_time_quotes_all_us_stocks = real_time_quotes_all_us_stocks.sort_values(by=['amount'], ascending=False)