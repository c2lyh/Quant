from pymongo import MongoClient, ASCENDING, UpdateOne
import tushare as ts
from util.database import DB_CONN
from util.quant_util import get_all_codes, get_all_dates


class DailyFixing:
    def __init__(self):
        self.db = MongoClient('mongodb://127.0.0.1:27017')['quanttushare']

    #获取区间内交易日的list
    def get_dates(self,begin_date,end_date):
        date_cursor = self.db.daily.find(
            {
                'code':'000001',
                'index':True

                #'date':{'%gte':begin_date,'%lte':end_date}
            },
            sort = [('date',ASCENDING)],
            projection={'date':True}
        )

        dates = [x['date'] for x in date_cursor]

        #print(dates)
        return dates



    #添加is_trading字段
    def fill_is_trading(self, autype=None, begin_date=None, end_date=None):
        dates = self.get_dates(begin_date, end_date)

        collection_name = 'daily_hfq' if autype == 'hfq' else 'daily'

        for date in dates:
            daily_cursor = self.db[collection_name].find(
                {'date': date},
                projection={'code': True, 'volume': True, 'index': True})

            update_requests = []
            for daily in daily_cursor:
                update_requests.append(
                    UpdateOne(
                        {'code': daily['code'], 'date': date, 'index': daily['index']},
                        {'$set': {'is_trading': (daily['volume'] > 0)}}
                    ))

            if len(update_requests) > 0:
                update_result = self.db[collection_name].bulk_write(update_requests, ordered=False)
                print('Update is_trading, date: %s, inserted: %4d, modified: %4d'
                      % (date, update_result.upserted_count, update_result.modified_count),
                      flush=True)

    #更新周期内停牌日
    def fill_suspension_dailies(self, autype=None, begin_date=None, end_date=None):
        # df_stock = ts.get_stock_basics()
        codes = ['000001']
        dates = self.get_dates(begin_date, end_date)
        # codes = get_all_codes()
        # dates = get_all_dates(begin_date, end_date)

        collection_name = 'daily_hfq' if autype == 'hfq' else 'daily'

        for code in codes:
            daily_cursor = self.db[collection_name].find(
                {'code': code, 'date': {'$gte': begin_date, '$lte': end_date}, 'index': False},
                sort=[('date', ASCENDING)],
                projection={'date': True, 'close': True}
            )

            date_daily_dict = dict([(daily['date'], daily) for daily in daily_cursor])

            last_daily = None

            update_requests = []
            for date in dates:
                if date in date_daily_dict:
                    last_daily = date_daily_dict[date]
                else:
                    if last_daily is not None:
                        suspension_daily = {
                            'code': code,
                            'date': date,
                            'is_trading': False,
                            'index': False,
                            'volume': 0,
                            'open': last_daily['close'],
                            'close': last_daily['close'],
                            'high': last_daily['close'],
                            'low': last_daily['close']
                        }

                        update_requests.append(
                            UpdateOne(
                                {'code': code, 'date': date, 'index': False},
                                {'$set': suspension_daily},
                                upsert=True
                            ))

            if len(update_requests) > 0:
                update_result = self.db[collection_name].bulk_write(update_requests, ordered=False)
                print('Fill suspension dailies, code: %s, inserted: %4d, modified: %4d'
                      % (code, update_result.upserted_count, update_result.modified_count),
                      flush=True)

    #补充复权因子，
    #**需要修改，不清楚如何设计持仓

    # def fill_aufactor_pre_close(self, begin_date=None, end_date=None):
    #         dates = get_all_dates(begin_date, end_date)
    #
    # for date in dates:
    #     daily_cursor = DB_CONN['daily'].find(
    #         {'date': date, 'index': False},
    #         projection={'code': True, 'close': True, '_id': False})
    #
    #     code_daily_dict = dict([(daily['code'], daily) for daily in daily_cursor])
    #
    #     daily_hfq_cursor = DB_CONN['daily_hfq'].find(
    #         {'date': date, 'index': False},
    #         projection={'code': True, 'close': True, '_id': False})
    #
    #     update_requests = []
    #     for daily_hfq in daily_hfq_cursor:
    #         code = daily_hfq['code']
    #
    #         if code in code_daily_dict:
    #             aufactor = daily_hfq['close'] / code_daily_dict[code]['close']
    #             aufactor = round(aufactor, 3)
    #
    #             update_requests.append(
    #                 UpdateOne(
    #                     {'code': code, 'date': date, 'index': False},
    #                     {'$set': {'aufactor': aufactor}}))
    #
    #     if len(update_requests) > 0:
    #         update_result = DB_CONN['daily'].bulk_write(update_requests, ordered=False)
    #         print('Fill aufactor, date: %s, modified: %4d'
    #               % (date, update_result.modified_count),
    #               flush=True)
    #
    # codes = get_all_codes()
    # """
    # current_daily['aufactor'] * current_daily['pre_close'] =
    # last_daily['close'] * last_daily['aufactor']
    #
    # current_daily['volume'] * current_daily['pre_close'] =
    # last_daily['close'] * last_daily['volume']
    # """


    #需要先解决上一问题
    # def fill_high_limit_low_limit(self, begin_date=None, end_date=None):
    #     codes = get_all_codes()
    #     dates = get_all_dates(begin_date, end_date)
    #
    #     for code in codes:
    #         daily_cursor = self.db['daily'].find(
    #             {'code': code},
    #             projection={'pre_close': True, 'date': True, '_id': False})
    #
    #         for daily in daily_cursor:
    #             date = daily['date']
    #             basic = self.db['basic'].find_one(
    #                 {'code': code, 'date': daily['date']},
    #                 projection={'timeToMarket': True, 'name': True})
    #
    #             if date == basic['timeToMarket']:
    #                 # 按照新股的方法计算high_limit和Low_limit
    #                 ipo_price = DB_CONN['new_stocks'].find_one(
    #                     {'code': code})['price']
    #
    #                 high_limit = ipo_price * 1.44
    #                 low_limit = ipo_price * 0.64
    #             elif basic['name'][0:2] == 'ST' or basic['name'][0:3] == '*ST':
    #                 high_limit = daily['pre_close'] * 1.05
    #                 low_limit = daily['pre_close'] * 0.95
    #             else:
    #                 high_limit = daily['pre_close'] * 1.1
    #                 low_limit = daily['pre_close'] * 0.9
    #
    #             high_limit = round(high_limit, 2)
    #             low_limit = round(low_limit, 2)


if __name__ == '__main__':
    df = DailyFixing()
    df.fill_is_trading(begin_date='2015-01-01', end_date='2015-01-31')
    df.fill_is_trading(autype='hfq', begin_date='2005-01-01', end_date='2014-12-31')
    #df.fill_suspension_dailies(autype='hfq', begin_date='2005-01-01', end_date='2014-12-31')
    # df.fill_suspension_dailies(begin_date='2005-01-01', end_date='2014-12-31')
    # df.fill_aufactor_pre_close(begin_date='2005-01-01', end_date='2014-12-31')

