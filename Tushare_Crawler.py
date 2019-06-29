import tushare as ts
from pymongo import MongoClient,UpdateOne


class DataCrawler:

    def __init__(self):
        self.db = MongoClient('mongodb://127.0.0.1:27017')['quanttushare'] #name of database



    def crawl_index(self,begin_date = None, end_date = None): #抓取周期内指数数据

        codes = ['000001','000300','399001','399005','399006']
        #上证，深证，深证成指，中小板，创业板
        #codes = ['000001']

        for code in codes:
            df_daily = ts.get_k_data(code,index=True,start = begin_date,end = end_date)

            updates_requests = []
            for index in df_daily.index:
                # df_daily.loc is to locate record by index eg:58 59
                # then change it to dict type(MongoDB) as below
                '''
                {'date': '2019-04-02', 'open': 3183.27, 'close': 3176.82, 'high': 3193.27, 
                'low': 3164.91, 'volume': 447068981.0, 'code': 'sh000001'}
                                      *如果不加入index=true, 则code:'000001'
                '''
                doc = dict(df_daily.loc[index])

                doc['index'] = True       #change index = True, and change sh000001 to 000001
                doc['code'] = code      #用index来区分指数和股票，例如平安银行


                print(doc, flush=True)

                #update into database
                updates_requests.append(
                    UpdateOne(
                        {'code':doc['code'],'date':doc['date'],'index':True},
                        {'$set':doc},
                        upsert=True) #upsert：如果找到合适的才更新
                )

                """
                [UpdateOne({'code': '000001', 'date': '2019-04-01', 'index': True}, {'$set:doc'}, True, None, None), 
                """


            if len(updates_requests) > 0 :


                # write to database
                updates_results = self.db['daily'].bulk_write(updates_requests,ordered = False)

                #upsearted_count: new records
                #modified: new changed records
                print('Daily index update, code:%s,inserted:%4d, modified: %4d'
                      % (code,updates_results.upserted_count,updates_results.modified_count),flush=True)


                '''
                { "_id" : ObjectId("5cb37e8f72694a6060a7abef"), "code" : "000001", "date" : "2019-04-01",
                 "index" : true, "close" : 3170.36, "high" : 3176.62, "low" : 3111.66, "open" : 3111.66, 
                 "volume" : 466124693 }
                 ....
                 
                '''

#Things to figure out:股票数据该存后复权还是？？？

    def crawl_stock(self, autype = None, begin_date = None, end_date = None):
                        #autype=none = 不复权

#       df_stock = ts.get_stock_basics()   #获取所有股票基本代码/信息
#       codes = list(df_stock.index)       #获取所有股票代码，以list的形式
        #本地方便测试只用000001



        codes = ['000001']
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


                print(doc, flush=True)

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
                #print(updates_requests)

            if len(updates_requests) > 0 :
                colletion_name = 'daily_hfq' if autype == 'hfq' else 'daily' #处理复权数据字符
                # write to database
                updates_results = self.db[colletion_name].bulk_write(updates_requests,ordered = False)

                #upsearted_count: new records
                #modified: new changed records
                print('Daily index %s, update, code:%s,inserted:%4d, modified: %4d'
                      % (colletion_name,code, updates_results.upserted_count, updates_results.modified_count), flush=True)


if __name__ == '__main__':
    dc = DataCrawler()
    dc.crawl_index(begin_date='2015-01-01', end_date='2015-01-31')
    dc.crawl_stock(begin_date='2015-01-01', end_date='2015-01-31')
    dc.crawl_stock(autype = 'hfq',begin_date='2015-01-01', end_date='2015-01-31')






'''
MongoDB: notes


show databases
use xxxx
show collections
db.daily.find()
db.daily.count()
#查询db里股票命令
db.daily.find({code:'000001',index:false}) 

数据库加索引？？？？
db.daily.createIndex({code:1,date:1,index:1})
db.daily_hfq.createIndex({code:1,date:1,index:1})

'''

'''
Database notes:

Date       close     aufactor  后复权            前复权
2018-08-09 10        1         10 * 1 = 10       (10 * 1)/2.2 = ?
2018-08-10 5.4       2         5.4 * 2 = 10.8    (5.4*2)/ 2.2 = ?
2018-08-13 5.4       2.2       5.4 * 2 = 10.8    (5.4*2)/ 2.2 = 5.4


'''