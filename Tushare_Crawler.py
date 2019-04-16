import tushare as ts
from pymongo import MongoClient,UpdateOne


class DataCrawler:

    def __init__(self):
        self.db = MongoClient('mongodb://127.0.0.1:27017')['quant'] #quant is the name of database



    def crawl_index(self,begin_date = None, end_date = None):

        #codes = ['000001','000300','399001','399005','399006']
        codes = ['000001']

        for code in codes:
            df_daily = ts.get_k_data(code,index=True,start = begin_date,end = end_date)

            updates_requests = []
            for index in df_daily.index:
                # df_daily.loc is to locate record by index eg:58 59
                # then change it to dict type(MongoDB) as below
                '''
                {'date': '2019-04-02', 'open': 3183.27, 'close': 3176.82, 'high': 3193.27, 
                'low': 3164.91, 'volume': 447068981.0, 'code': 'sh000001'}
                '''
                doc = dict(df_daily.loc[index])

                #change index = True, and change sh000001 to 000001
                doc['index'] = True
                doc['code'] = code


                #print(doc, flush=True)

                #update into database
                updates_requests.append(
                    UpdateOne(
                        {'code':doc['code'],'date':doc['date'],'index':True},
                        {'$set':doc},
                        upsert=True)
                )

                """
                [UpdateOne({'code': '000001', 'date': '2019-04-01', 'index': True}, {'$set:doc'}, True, None, None), 
                """


            if len(updates_requests) > 0 :


                # write to database
                updates_results = self.db['daily'].bulk_write(updates_requests,ordered = False)

                #upsearted_count: new records
                #modified: new changed records
                print('Saving daily index data, inserted: ',
                      updates_results.upserted_count, 'code: ', code, 'modified: ',updates_results.modified_count)

                '''
                { "_id" : ObjectId("5cb37e8f72694a6060a7abef"), "code" : "000001", "date" : "2019-04-01",
                 "index" : true, "close" : 3170.36, "high" : 3176.62, "low" : 3111.66, "open" : 3111.66, 
                 "volume" : 466124693 }
                 ....
                 
                '''


    def crawl_stock(self, autype = None, begin_date = None, end_date = None):
        '''
        df_stock = ts.get_stock_basics()
        codes = list(df_stock.index)
        '''
        codes = ['000001','600000']
        for code in codes:
            df_daily = ts.get_k_data(code, autype = autype,
                                     start = begin_date,end = end_date)

            updates_requests = []
            for index in df_daily.index:
                # df_daily.loc is to locate record by index eg:58 59
                # then change it to dict type(MongoDB) as below
                '''
                {'date': '2019-04-02', 'open': 3183.27, 'close': 3176.82, 'high': 3193.27, 
                'low': 3164.91, 'volume': 447068981.0, 'code': 'sh000001'}
                '''
                doc = dict(df_daily.loc[index])

                #change index = True, and change sh000001 to 000001
                doc['index'] = False
                doc['code'] = code


                #print(doc, flush=True)

                #update into database
                updates_requests.append(
                    UpdateOne(
                        {'code':doc['code'],'date':doc['date'],'index':False},
                        {'$set':doc},
                        upsert=True)
                )

                """
                [UpdateOne({'code': '000001', 'date': '2019-04-01', 'index': True}, {'$set:doc'}, True, None, None), 
                """
                print(updates_requests)

            if len(updates_requests) > 0 :
                colletion_name = 'daily_hfq' if autype == 'hfq' else 'daily'
                # write to database
                updates_results = self.db[colletion_name].bulk_write(updates_requests,ordered = False)

                #upsearted_count: new records
                #modified: new changed records
                print('Saving daily index data, inserted: ',
                      updates_results.upserted_count, 'code: ', code, 'modified: ',updates_results.modified_count)








if __name__ == '__main__':
    dc = DataCrawler()
    #dc.crawl_index(begin_date='2019-04-01', end_date='2019-04-07')
    dc.crawl_stock(begin_date='2019-04-01', end_date='2019-04-07')
    dc.crawl_stock(autype = 'hfq',begin_date='2019-04-01', end_date='2019-04-07')
