import tushare as ts

ts.set_token('c5349cb065260c815388dedc8f12968e4e9556f5ee9c919ca8985b16')    #set token for API


pro = ts.pro_api()
df = pro.coinlist(start_date='20170101', end_date='20171231')

'''df
coin                         en_name  cn_name issue_date        amount
0    PYLNT                           Pylon     None   20171231  6.338580e+05
1      hlc                      HalalChain    绿色食品链   20171230  1.000000e+09
2      qlc                           Qlink     None   20171230  6.000000e+08
3       XP               Experience Points     None   20171230  2.683600e+11
4      CHT                   CoinHot Token       热币   20171230  3.692800e+08
5      DBC                 DeepBrain Chain      深脑链   20171229  1.000000e+10
6     HTML                        HTMLCoin     None   20171229  9.404459e+10
7      mot                    Olympus Labs     奥林巴斯   20171229  1.00000
'''


#Notes: the tusahrepro has whitepaper to directly download






###get exchange information


df = pro.coinexchanges(area_code='us')

#按交易对数量排序
df = df.sort('pairs', ascending=False)
df = pro.query('coinexchanges', area_code='us')

'''
       exchange          name  pairs area_code coin_trade fut_trade oct_trade
0         bit-z         Bit-Z    183        us          Y         N         N
1       bittrex            B网    280        us          Y         Y         N
2     btc-alpha     BTC Alpha     67        us          Y         N         N
3     cobinhood           柯宾汉    114        us          Y         N         N
4   coinbasepro  Coinbase Pro     15        us          Y         N         N
5     cryptogro     CryptoGro      0        us          Y         N         N
6           dew           DEW     12        us          Y         Y         N
7        f8coin         F8交易所      5        us          Y         N         N
8        fatbtc           胖比特     28        us          Y         N         N
9        gemini           双子星      6        us          Y         N         N
10        golix      Golix.io     63        us          Y         N         N
11        itbit         itBit      1        us          Y         N         N
12      keepbtc           持币网     23        us          Y         N         Y
13       kraken            K网     52        us          Y         N         N
14       kucoin           库币网    359        us          Y         N         N
15         okex          OKEX    585        us          Y         Y         Y
16     poloniex            P网     91        us          Y         N         N
17        prdae         PRDAE     16        us          Y         N         Y
18       usadae        USADAE     17        us          Y         N         N

'''