from pymongo import MongoClient, ASCENDING, UpdateOne
import tushare as ts
from util.database import DB_CONN
from util.quant_util import get_all_codes, get_all_dates


class DailyFixing:
    def __init__(self):
        self.db = MongoClient('mongodb://127.0.0.1:27017')['quanttushare']

    def get_dates(self,begin_date,end_date):
        date_cursor = self.db.daily.find(
            {
                'code':'000001',
                'index':True

            },
            sort = [('date',ASCENDING)],
            projection={'date':True}
        )

        dates = [x['date'] for x in date_cursor]

        #print(dates,flush=True)
        return dates

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
                update_result = DB_CONN[collection_name].bulk_write(update_requests, ordered=False)
                print('Update is_trading, date: %s, inserted: %4d, modified: %4d'
                      % (date, update_result.upserted_count, update_result.modified_count),
                      flush=True)
 #更新周期内停牌日
    def fill_suspension_dailies(self, autype=None, begin_date=None, end_date=None):
        #df_stock = ts.get_stock_basics()
        codes = ['000001']
        dates = self.get_dates(begin_date, end_date)
        #codes = get_all_codes()
        #dates = get_all_dates(begin_date, end_date)

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

if __name__ == '__main__':
    df = DailyFixing()
   #df.get_dates(begin_date='2015-01-06', end_date='2015-01-29')
    #df.fill_is_trading(begin_date='2015-01-01', end_date='2015-01-31')
    df.fill_suspension_dailies(begin_date='2015-01-01', end_date='2015-01-31')