import tushare as ts



dftest = ts.get_k_data('000001',start = '2019-04-01', end = '2019-04-10')
                                                                        #Index = True

"""dftest
          date   open  close   high    low     volume    code
58  2019-04-01  12.83  13.18  13.55  12.83  1951401.0  000001
59  2019-04-02  13.28  13.36  13.48  13.23  1100384.0  000001
60  2019-04-03  13.21  13.44  13.45  13.15   792915.0  000001
61  2019-04-04  13.43  13.86  14.00  13.43  2034365.0  000001
62  2019-04-08  13.90  13.96  14.43  13.72  1743176.0  000001

"""

df_code = ts.get_stock_basics()
'''

name industry area       pe  ...   profit    gpr       npr   holders
code                                  ...                                    
300768    N迪普     软件服务   浙江    32.18  ...    30.53  70.69     28.55   77596.0
300158   振东制药      中成药   山西    72.75  ...   -74.66  64.12      2.58   20263.0
600794   保税科技     仓储物流   江苏   178.89  ...   115.68  11.39      2.60   83309.0
000607   华媒控股     广告包装   浙江    84.60  ...   -32.61  26.85      5.20   40359.0
600178   东安动力     汽车配件  黑龙江   579.92  ...   -86.97  11.35      0.43   40965.0
000862   银星能源     新型电力   宁夏   107.47  ...   129.65  38.13      4.45   82454.0
600710    苏美达     工程机械   江苏    19.77  ...    27.19   6.14      0.56   34400.0
000966   长源电力     火力发电   湖北    26.80  ...   193.83  10.78      3.59   50684.0
002210   飞马国际     仓储物流   深圳    59.72  ...   -32.20   0.50      0.30   55232.0
000410   沈阳机床     机床制造   辽宁     0.00  ...    77.58  26.60     -4.17  116387.0
300356   光一科技     电气设备   江苏   139.62  ...   249.69  32.98      8.21   22929.0
000958   东方能源     火力发电   河北    62.56  ...    29.74  13.48      4.70   76397.0
600365   通葡股份     红黄药酒   吉林   859.72  ...   -24.08  18.73      0.31   35525.0
000993   闽东电力     水力发电   福建     0.00  ... -1828.18  41.93    -69.98   33412.0
002723    金莱特     家用电器   广东     0.00  ...  -196.41   8.45     -2.11   13452.0
600081   东风科技     汽车配件   上海    29.50  ...     5.02  16.66      2.20   22349.0
603879   永悦科技     化工原料   福建    57.00  ...   -14.81  15.89      6.15    9172.0
'''
df_code.index

'''
df_code.index
Index(['300768', '300158', '600794', '000607', '600178', '000862', '600710',
       '000966', '002210', '000410',
       ...
       '603068', '600680', '600401', '300773', '300772', '300771', '300770',
       '300769', '002680', '002070'],
      dtype='object', name='code', length=3611)
'''
