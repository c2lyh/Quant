#  -*- coding: utf-8 -*-

import urllib3
import tushare as ts
import json, traceback
from pymongo import MongoClient, ASCENDING, UpdateOne

class FinanceReportCrawler:
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

    def crawl_report(self):
        url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?'\
                'type={1}&token=70f12f2f4f091e459a279469fe49eca5&'\
                'st=reportdate&sr=-1&p=1&ps=80&'\
                'js={"pages":(tp),"data":%20(x)}&'\
                'filter=(scode=%27{2}%27)&rt=51140869'\

        # report_types = ['CWBB_ZCFZB', 'CWBB_XJLLB', 'CWBB_LRB']
        report_types = ['CWBB_LRB']

        #all_codes = get_all_codes()
        all_codes = ['000001']

        conn_pool = urllib3.PoolManager()

        for report_type in report_types:
            for code in all_codes:
                response = conn_pool.request(
                    'GET',
                    url=url.replace('{1}', report_type).replace('{2}', code))

                result = json.loads(response.data.decode('utf-8'))

                update_requests = []
                for report in result['data']:
                    report['announced_date'] = report['noticedate'][0:10]
                    del report['noticedate']
                    report['report_date'] = report['reportdate'][0:10]
                    del report['reportdate']
                    report['code'] = report['scode']
                    del report['scode']

                    update_requests.append(
                        UpdateOne(
                            {'code': report['code'], 'report_date': report['report_date']},
                            {'$set': report},
                            upsert=True
                        ))

                if len(update_requests) > 0:
                    update_result = self.db[report_type].bulk_write(update_requests, ordered=False)
                    print('获取财务报告，股票：%s，类型：%10s, 插入：%4d, 更新：%4d' %
                          (code, report_type, update_result.upserted_count, update_result.modified_count),
                          flush=True)


    def crawl_yjbb(self):
        url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface' \
              '/api/js/get?type=YJBB20_YJBB&token=70f12f2f4f091e4' \
              '59a279469fe49eca5&st=reportdate&sr=-1&filter=(scode={1})&' \
              'p=1&ps=100&js={"pages":(tp),"data":(x)}'

        codes = ['000001']

        conn_pool = urllib3.PoolManager()
        for code in codes:
            try:
                response = conn_pool.request('GET',
                                             url.replace('{1}', code))

                # # 解析抓取结果
                result = json.loads(response.data.decode('UTF-8'))

                reports = result['data']

                update_requests = []
                for report in reports:
                    doc = {
                        'code': report['scode'],
                        'name': report['sname'],
                        'basic_eps': report['basiceps'],
                        'report_date': report['reportdate'][0:10],
                        'announced_date': report['latestnoticedate'][0:10]
                    }

                    update_requests.append(
                        UpdateOne(
                            {'code': doc['code'], 'report_date': doc['report_date']},
                            {'$set': doc},
                            upsert=True
                        ))

                if len(update_requests) > 0:
                    update_result = self.db['yjbb'].bulk_write(update_requests, ordered=False)
                    print('获取财务报告，股票：%s，类型：业绩报表, 插入：%4d, 更新：%4d' %
                          (code, update_result.upserted_count, update_result.modified_count),
                          flush=True)
            except:
                print('获取业绩报表时，发生错误：%s' % code, flush=True)
                # traceback.print_exc()




if __name__ == '__main__':
    frc = FinanceReportCrawler()
    frc.crawl_report()


"""
# 资产负债表
http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?
type=CWBB_ZCFZB&token=70f12f2f4f091e459a279469fe49eca5&
st=reportdate&sr=-1&p=1&ps=50&
js=var%20hFQXajHj={pages:(tp),data:%20(x)}&
filter=(scode=%27601577%27)&rt=51140869
# 利润表
http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?
type=CWBB_LRB&token=70f12f2f4f091e459a279469fe49eca5&
st=reportdate&sr=-1&p=1&ps=50&
js=var%20hFQXajHj={pages:(tp),data:%20(x)}&
filter=(scode=%27601577%27)&rt=51140869
# 现金流量表
http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?
type={1}&token=70f12f2f4f091e459a279469fe49eca5&
st=reportdate&sr=-1&p=1&ps=80&
js={"pages":(tp),"data":%20(x)}&
filter=(scode=%27{2}%27)&rt=51140869

{1} = ['CWBB_ZCFZB', 'CWBB_XJLLB', 'CWBB_LRB']
{2} = code
"""

