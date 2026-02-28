#!/usr/bin/env python3
"""
股票筛选工具 - 支持 pywencai 和 akshare
"""
import pywencai
import akshare as ak
import pandas as pd
from datetime import datetime

def wencai_screen(query: str = "量比大于 1.5，涨幅 0 到 7%，非 ST"):
    """使用 pywencai 筛选股票"""
    try:
        result = pywencai.get(query=query, query_type="stock")
        if isinstance(result, dict) and 'data' in result:
            return result['data']
        return result
    except Exception as e:
        print(f"pywencai 错误：{e}")
        return None

def akshare_realtime(symbol: str = "300502"):
    """使用 akshare 获取实时行情"""
    try:
        df = ak.stock_zh_a_spot_em()
        stock = df[df['代码'] == symbol]
        if not stock.empty:
            return stock.iloc[0]
        return None
    except Exception as e:
        print(f"akshare 错误：{e}")
        return None

def get_stock_info(symbol: str = "300502"):
    """获取股票详细信息"""
    try:
        import urllib.request
        url = f"https://qt.gtimg.cn/q=sz{symbol}"
        data = urllib.request.urlopen(url).read().decode('gbk')
        return data
    except Exception as e:
        return f"错误：{e}"

if __name__ == "__main__":
    print("📊 股票筛选工具")
    print("=" * 50)
    
    print("\n🔍 pywencai 筛选结果:")
    result = wencai_screen()
    if result is not None:
        if isinstance(result, pd.DataFrame):
            print(result.head(10))
        else:
            print(result)
    
    print("\n📈 新易盛 (300502) 行情:")
    info = get_stock_info("300502")
    print(info)
