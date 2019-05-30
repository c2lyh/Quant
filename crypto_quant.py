import tushare as ts





class crypto_basic:
    def __init__(self):
        pass


    def crawit(self):
        pass





if __name__=='__main__':

    pass




'0d643fc24dda440daebd8f87c6afd646ef16f3dcb7261f3c190a5ccf' #Tushare Token


'''
Notes:
pro=ts.pro_api('0d643fc24dda440daebd8f87c6afd646ef16f3dcb7261f3c190a5ccf')  #Create connection with token


-------------------------------------
df = pro.coinlist(start_date='20170101', end_date='20171231') # 获取日期内的币种

      coin                         en_name  cn_name issue_date        amount
0    PYLNT                           Pylon     None   20171231  6.338580e+05
1      hlc                      HalalChain    绿色食品链   20171230  1.000000e+09
2      qlc                           Qlink     None   20171230  6.000000e+08
3       XP               Experience Points     None   20171230  2.683600e+11




--------------------------------------
df = pro.coincap(trade_date='20180806')   #获取特定日期市值排列

 trade_date   coin  ...       vol24          create_time
0      20180806    BTC  ...  3701598619  2018-08-06 11:10:28
1      20180806    ETH  ...  1385316875  2018-08-06 11:10:28
2      20180806    XRP  ...   188205795  2018-08-06 11:10:28
3      20180806    BCH  ...   312904933  2018-08-06 11:10:28
4      20180806    EOS  ...   489455314  2018-08-06 11:10:28

--------------------------------------
#搞得好，要每日行情还要积分 我日 
df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='1min', start_date='20180801', end_date='20180802')
#加入高级用户QQ群（群号：658562506）905322493




--------------------------------------
df = pro.btc_pricevol(start_date='20180101', end_date='20180801') #获取比特币量价信息

        date         price        volume
0    20180801   7579.056837  5.759918e+08
1    20180731   7915.267761  7.305237e+08
2    20180730   8128.549310  6.716885e+08
3    20180729   8193.888653  2.656748e+08


--------------------------------------

df = pro.jinse(start_date='2018-08-17 16:00:00', end_date='2018-08-17 18:00:00', \  
                fields='title, type, datetime')                 #获取咨询，eg 金色财经
                
                                           title type             datetime
0                    币客将于8月19日开启存币生息功能   公告  2018-08-17 17:57:27
1                 FOMO智能合约使以太坊交易费用大幅增加   动态  2018-08-17 17:49:21
2              币威美国 CSO：钱包是下一个区块链千万级社群   声音  2018-08-17 17:35:06
3   OKCoin大量币种上涨YOYO的24H涨幅达到13,611.22%   行情  2018-08-17 17:29:22






    
                
                
                
                
--------------------------------------

'''