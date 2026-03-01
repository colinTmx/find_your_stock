#!/usr/bin/env python3
"""
东方财富人气热门股票工具
支持：人气榜、上涨榜
"""
import akshare as ak
import pandas as pd
from datetime import datetime


def get_dongfang_popular_stocks(limit: int = 50) -> pd.DataFrame:
    """
    东方财富股票人气榜
    https://guba.eastmoney.com/rank/
    """
    try:
        df = ak.stock_hot_rank_em()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['排名'] = df.get('当前排名', range(1, len(df)+1))
        result['代码'] = df.get('代码', '')
        result['名称'] = df.get('股票名称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['榜单类型'] = '人气榜'
        return result
    except Exception as e:
        print(f"❌ 人气榜获取失败：{e}")
        return pd.DataFrame()


def get_dongfang_hot_up(limit: int = 50) -> pd.DataFrame:
    """
    东方财富热门上涨榜
    """
    try:
        df = ak.stock_hot_up_em()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['排名'] = range(1, len(df)+1)
        result['代码'] = df.get('代码', '')
        result['名称'] = df.get('股票名称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['榜单类型'] = '上涨榜'
        return result
    except Exception as e:
        print(f"❌ 上涨榜获取失败：{e}")
        return pd.DataFrame()


def merge_all_popular(limit_per_board: int = 50) -> pd.DataFrame:
    """
    整合东方财富热门股票数据
    """
    all_dfs = []
    
    print("📊 获取东方财富人气榜...")
    df = get_dongfang_popular_stocks(limit_per_board)
    if not df.empty:
        all_dfs.append(df)
    
    print("📈 获取东方财富上涨榜...")
    df = get_dongfang_hot_up(limit_per_board)
    if not df.empty:
        all_dfs.append(df)
    
    if all_dfs:
        result = pd.concat(all_dfs, ignore_index=True)
        result['更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return result
    else:
        return pd.DataFrame()


def find_cross_board_stocks(df: pd.DataFrame) -> pd.DataFrame:
    """
    找出在两个榜单都热门的股票
    """
    if df.empty:
        return pd.DataFrame()
    
    stock_counts = df.groupby(['代码', '名称']).agg({
        '排名': 'min',
        '最新价': 'first',
        '涨跌幅': 'first',
        '榜单类型': lambda x: '、'.join(sorted(set(x)))
    }).reset_index()
    
    stock_counts['榜单数量'] = stock_counts['榜单类型'].apply(lambda x: len(x.split('、')))
    
    cross_board = stock_counts[stock_counts['榜单数量'] >= 2].sort_values(
        by=['榜单数量', '排名'],
        ascending=[False, True]
    )
    
    return cross_board


def print_summary(df: pd.DataFrame):
    """打印数据统计"""
    if df.empty:
        return
    
    print("\n📊 数据统计:")
    print(f"   总记录数：{len(df)}")
    
    type_counts = df['榜单类型'].value_counts()
    print("\n   按榜单类型:")
    for dtype, count in type_counts.items():
        print(f"   - {dtype}: {count} 条")


if __name__ == "__main__":
    print("=" * 60)
    print("🔥 东方财富热门股票工具")
    print("=" * 60)
    
    df = merge_all_popular(limit_per_board=50)
    
    if not df.empty:
        print(f"\n✅ 共获取 {len(df)} 条热门股票数据")
        print_summary(df)
        
        print("\n📋 人气榜 TOP10:")
        popular = df[df['榜单类型'] == '人气榜'].head(10)
        print(popular[['排名', '代码', '名称', '最新价', '涨跌幅']].to_string())
        
        print("\n📋 上涨榜 TOP10:")
        hot_up = df[df['榜单类型'] == '上涨榜'].head(10)
        print(hot_up[['排名', '代码', '名称', '最新价', '涨跌幅']].to_string())
        
        print("\n" + "=" * 60)
        print("🎯 双榜热门股票 (同时出现在人气榜和上涨榜)")
        print("=" * 60)
        cross = find_cross_board_stocks(df)
        if not cross.empty:
            print(f"\n找到 {len(cross)} 只双榜热门股票:\n")
            print(cross[['代码', '名称', '最新价', '涨跌幅', '榜单类型']].to_string())
        else:
            print("暂无双榜热门股票")
    else:
        print("❌ 未能获取到任何数据")
