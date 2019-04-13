import tushare as ts
from pymongo import MongoClient,UpdateOne


class DataCrawler:
    def __init__(self):
        #use mongodb to store data
        self.db = MongoClient('mongodb://127.0.0.1:27017')['my_quant']



    def crawl_index(self,begin_date=None, end_date = None):
        codes = ['000001','000300','399001','399005','399006']
        #codes = ['000001']
        for code in codes:
            df_daily = ts.get_k_data(code,index=True, start = begin_date,end = end_date)


            updates_requests = []

            for index in df_daily.index:
                doc = dict(df_daily.loc[index])
                doc['index'] = True
                doc['code'] = code
                print(doc,flush=True)

                #save every records to database
                #Updateone for updating repeated records
                updates_requests.append(
                    UpdateOne({'code':doc['code'],'date':doc['date'],'index':True},
                              {'$set':doc},upsert=True))

                if len(updates_requests) >0:
                    updates_result = self.db['daily'].bulk_write(updates_requests,ordered=False)
                    #%s = String, %4d = number (space for 4)
                    print('Saved index daily, code: %s, inserted: %4d, modified:%4d'
                          %(code,updates_result.upserted_count,updates_result.modified_count),flush=True)






    def crawl_stock(self,autype =None, begin_date = None,end_date = None):
        df_stock= ts.get_stock_basics()
        codes = list(df_stock.index)

        for code in codes:
            df_daily = ts.get_k_data(code,autype = autype,
                                         start = begin_date,end = end_date)


            updates_requests = []

            for index in df_daily.index:
                doc = dict(df_daily.loc[index])
                doc['index'] = True
                doc['code'] = code
                print(doc,flush=True)

                #save every records to database
                #Updateone for updating repeated records
                updates_requests.append(
                    UpdateOne({'code':doc['code'],'date':doc['date'],'index':False},
                              {'$set':doc},upsert=True))

                #based on hfq or qfq(daily)
                if len(updates_requests) >0:
                    collection_name = 'daily_hfq' if autype == 'hfq' else 'daily'

                    updates_result = self.db[collection_name].bulk_write(updates_requests,ordered=False)
                    #%s = String, %4d = number (space for 4)
                    print('Saved index daily, code: %s, inserted: %4d, modified:%4d'
                          %(code,updates_result.upserted_count,updates_result.modified_count),flush=True)




if __name__ == "__main__":
    dc = DataCrawler()
    #dc.crawl_index(begin_date='2019-03-08',end_date='2019-03-09')
    dc.crawl_stock(begin_date='2015-01-01', end_date='2015-01-31')
    dc.crawl_stock(autype='hfq', begin_date='2015-01-01', end_date='2015-01-31')