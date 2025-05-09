# -*- coding: utf-8 -*-
"""
本模块功能：另类证券市场指数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2025年5月8日
最新修订日期：
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')

from siat.common import *
#==============================================================================


def other_index_translate(index_code):
    """
    ===========================================================================
    功能：另类证券市场指数代码
    参数：
    index_code: 指数代码，非标准，来自东方财富和新浪。
    返回值：是否找到，基于语言环境为中文或英文解释。
    语言环境判断为check_language()
    
    数据结构：['指数代码','指数符号','指数名称中文','指数名称英文','数据来源']
    """
    
    import pandas as pd
    trans_dict=pd.DataFrame([
        
        ['INDEXCF','俄罗斯MICEX指数','俄罗斯MICEX指数','MICEX Index','sina'],
        ['RTS','俄罗斯RTS指数','俄罗斯RTS指数','RTS Index','sina'],
        ['CASE','埃及CASE 30指数','埃及CASE30指数','CASE30 Index','sina'],
        ['VNINDEX','越南胡志明','越南胡志明指数','Ho Chi-Ming Index','em'],
        ['HSCEI','国企指数','港股国企指数','HK H-share Index','em'],
        ['HSCCI','红筹指数','港股红筹指数','HK Red-share Index','em'],
        ['CSEALL','斯里兰卡科伦坡','斯里兰卡科伦坡全指','Colombo Index','em'],
        ['UDI','美元指数','美元指数','US Dollar Index','em'],
        ['CRB','路透CRB商品指数','路透CRB商品指数','Reuters CRB Index','em'],
        ['BDI','波罗的海BDI指数','波罗的海BDI指数','Baltic Dry Index','em'],
        ['KSE100','巴基斯坦卡拉奇','巴基斯坦卡拉奇指数','KSE100 Index','em'],
        
        
        ], columns=['code','symbol','name_cn','name_en','source'])

    found=False; symbol=index_code
    try:
        dict_word=trans_dict[trans_dict['code']==index_code]
        found=True
    except:
        #未查到翻译词汇，返回原词
        pass
    
    if dict_word is None:
        found=False    
    elif len(dict_word) == 0:
        found=False
    
    source=''; name=''
    if found:
        symbol=dict_word['symbol'].values[0]
        
        lang=check_language()
        if lang == 'Chinese':
            name=dict_word['name_cn'].values[0]
        else:
            name=dict_word['name_en'].values[0]
            
        source=dict_word['source'].values[0]
            
    return symbol,name,source

if __name__=='__main__': 
    index_code='KSE100'
    index_code='CASE'
    index_code='XYZ'
    
    set_language('Chinese')
    set_language('English')
    other_index_translate(index_code)

#==============================================================================
def get_other_index_em(index_code,start,end):
    """
    功能：获取另类指数历史行情，东方财富
    参数：
    index_code：指数代码
    start,end：开始/结束日期
    """
    symbol,name,source=other_index_translate(index_code)
    if symbol == index_code:
        return None
    
    import akshare as ak
    dft = ak.index_global_hist_em(symbol=symbol)
    dft.rename(columns={'日期':'Date','代码':'ticker','名称':'Name','今开':'Open', \
                        '最新价':'Close','最高':'High','最低':'Low','振幅':'Change'}, \
               inplace=True)
    dft['Change']=dft['Change']/100.00
    dft['Adj Close']=dft['Close']
    dft['source']=source
    dft['Volume']=0
    dft['Name']=name
    
    import pandas as pd
    dft['date']=dft['Date'].apply(lambda x: pd.to_datetime(x))
    dft.set_index('date',inplace=True)
    
    startpd=pd.to_datetime(start); endpd=pd.to_datetime(end)
    df=dft[(dft.index >= startpd) & (dft.index <= endpd)]
    
    return df

if __name__=='__main__': 
    index_code='KSE100'
    start='2025-2-1'; end='2025-3-31'
    get_other_index_em(index_code,start,end)
#==============================================================================
def get_other_index_sina(index_code,start,end):
    """
    功能：获取另类指数历史行情，新浪财经
    参数：
    index_code：指数代码
    start,end：开始/结束日期
    """
    symbol,name,source=other_index_translate(index_code)
    if symbol == index_code:
        return None
    
    import akshare as ak
    dft = ak.index_global_hist_sina(symbol=symbol)
    dft.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close', \
                        'volume':'Volume'},inplace=True)
    dft['ticker']=index_code; dft['Name']=name; dft['Date']=dft['date']
    dft['Adj Close']=dft['Close']
    dft['source']=source
    
    import pandas as pd
    dft['date']=dft['Date'].apply(lambda x: pd.to_datetime(x))
    dft.set_index('date',inplace=True)
    
    startpd=pd.to_datetime(start); endpd=pd.to_datetime(end)
    df=dft[(dft.index >= startpd) & (dft.index <= endpd)]
    
    return df

if __name__=='__main__': 
    index_code='CASE'
    start='2025-2-1'; end='2025-3-31'
    get_other_index_sina(index_code,start,end)
#==============================================================================
def get_other_index_ak(index_code,start,end):
    """
    功能：获取另类指数历史行情，新浪财经或东方财富
    参数：
    index_code：指数代码
    start,end：开始/结束日期
    """
    symbol,name,source=other_index_translate(index_code)
    if symbol == index_code:
        return None
    
    if source == 'em':
        df=get_other_index_em(index_code,start,end)
    elif source == 'sina':
        df=get_other_index_sina(index_code,start,end)
    else:
        df=None
        
    return df

if __name__=='__main__': 
    index_code='CASE'
    index_code='KSE100'
    index_code='VNINDEX'
    start='2025-2-1'; end='2025-3-31'
    get_other_index(index_code,start,end)
#==============================================================================
#==============================================================================
#==============================================================================


