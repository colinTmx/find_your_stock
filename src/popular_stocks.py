#!/usr/bin/env python3
"""
人气热门股票整合工具
支持：东方财富、同花顺、雪球、开盘啦
"""
import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional


def get_dongfang_popular(limit: int = 20) -> pd.DataFrame:
    """
    东方财富人气榜
    https://guba.eastmoney.com/rank/
    """
    try:
        df = ak.stock_hot_rank_em()
        if limit and len(df) > limit:
            df = df.head(limit)
        df['平台'] = '东方财富'
        df['数据类型'] = '人气排名'
        
        # 统一列名
        result = pd.DataFrame()
        result['当前排名'] = df.get('当前排名', range(1, len(df)+1))
        result['代码'] = df.get('代码', df.get('股票代码', ''))
        result['股票名称'] = df.get('股票名称', df.get('股票简称', ''))
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '东方财富'
        result['数据类型'] = '人气排名'
        return result
    except Exception as e:
        print(f"❌ 东方财富数据获取失败：{e}")
        return pd.DataFrame()


def get_tonghuashun_popular(limit: int = 20) -> pd.DataFrame:
    """
    同花顺热门股票 - 涨速榜
    """
    try:
        df = ak.stock_rank_cxd_ths()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['当前排名'] = range(1, len(df)+1)
        result['代码'] = df.get('代码', df.get('股票代码', ''))
        result['股票名称'] = df.get('股票名称', df.get('股票简称', ''))
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '同花顺'
        result['数据类型'] = '涨速榜'
        return result
    except Exception as e:
        print(f"❌ 同花顺数据获取失败：{e}")
        return pd.DataFrame()


def get_tonghuashun_volume(limit: int = 20) -> pd.DataFrame:
    """
    同花顺成交量榜
    """
    try:
        df = ak.stock_rank_cxsl_ths()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['当前排名'] = range(1, len(df)+1)
        result['代码'] = df.get('代码', df.get('股票代码', ''))
        result['股票名称'] = df.get('股票名称', df.get('股票简称', ''))
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '同花顺'
        result['数据类型'] = '成交量榜'
        return result
    except Exception as e:
        print(f"❌ 同花顺成交量榜获取失败：{e}")
        return pd.DataFrame()


def get_xueqiu_popular(limit: int = 20) -> pd.DataFrame:
    """
    雪球热门关注
    https://xueqiu.com/hq
    """
    try:
        df = ak.stock_hot_follow_xq()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['当前排名'] = range(1, len(df)+1)
        result['代码'] = df.get('股票代码', '')
        result['股票名称'] = df.get('股票简称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = 0
        result['涨跌幅'] = 0
        result['平台'] = '雪球'
        result['数据类型'] = '热门关注'
        return result
    except Exception as e:
        print(f"❌ 雪球数据获取失败：{e}")
        return pd.DataFrame()


def get_xueqiu_hot_discuss(limit: int = 20) -> pd.DataFrame:
    """
    雪球热门讨论
    """
    try:
        df = ak.stock_hot_tweet_xq()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['当前排名'] = range(1, len(df)+1)
        result['代码'] = df.get('股票代码', '')
        result['股票名称'] = df.get('股票简称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = 0
        result['涨跌幅'] = 0
        result['平台'] = '雪球'
        result['数据类型'] = '热门讨论'
        return result
    except Exception as e:
        print(f"❌ 雪球讨论数据获取失败：{e}")
        return pd.DataFrame()


def get_dongfang_realtime_hot(limit: int = 20) -> pd.DataFrame:
    """
    东方财富实时热门股票
    """
    try:
        df = ak.stock_hot_rank_latest_em()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['当前排名'] = range(1, len(df)+1)
        result['代码'] = df.get('代码', '')
        result['股票名称'] = df.get('股票名称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = 0
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '东方财富'
        result['数据类型'] = '实时热门'
        return result
    except Exception as e:
        print(f"❌ 东方财富实时数据获取失败：{e}")
        return pd.DataFrame()


def merge_all_popular(
    dongfang: bool = True,
    tonghuashun: bool = True,
    xueqiu: bool = True,
    limit_per_platform: int = 20
) -> pd.DataFrame:
    """
    整合所有平台的人气热门股票数据
    
    Args:
        dongfang: 是否包含东方财富
        tonghuashun: 是否包含同花顺
        xueqiu: 是否包含雪球
        limit_per_platform: 每个平台获取的股票数量
    
    Returns:
        合并后的 DataFrame
    """
    all_dfs = []
    
    if dongfang:
        print("📊 获取东方财富人气榜...")
        df = get_dongfang_popular(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
        
        print("⚡ 获取东方财富实时热门...")
        df = get_dongfang_realtime_hot(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
    
    if tonghuashun:
        print("📈 获取同花顺涨速榜...")
        df = get_tonghuashun_popular(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
        
        print("📊 获取同花顺成交量榜...")
        df = get_tonghuashun_volume(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
    
    if xueqiu:
        print("🔵 获取雪球热门关注...")
        df = get_xueqiu_popular(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
        
        print("💬 获取雪球热门讨论...")
        df = get_xueqiu_hot_discuss(limit_per_platform)
        if not df.empty:
            all_dfs.append(df)
    
    if all_dfs:
        result = pd.concat(all_dfs, ignore_index=True)
        result['更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return result
    else:
        return pd.DataFrame()


def find_cross_platform_stocks(df: pd.DataFrame) -> pd.DataFrame:
    """
    找出在多个平台都热门的股票
    
    Args:
        df: 整合后的热门股票数据
    
    Returns:
        跨平台热门股票
    """
    if df.empty:
        return pd.DataFrame()
    
    # 统计每只股票出现的平台数
    stock_counts = df.groupby(['代码', '股票名称']).agg({
        '平台': lambda x: '、'.join(sorted(set(x))),
        '当前排名': 'min',
        '最新价': 'first',
        '涨跌幅': 'first',
        '数据类型': lambda x: '、'.join(sorted(set(x)))
    }).reset_index()
    
    # 计算平台数量
    stock_counts['平台数量'] = stock_counts['平台'].apply(lambda x: len(x.split('、')))
    
    # 筛选出在 2 个及以上平台都热门的股票
    cross_platform = stock_counts[stock_counts['平台数量'] >= 2].sort_values(
        by=['平台数量', '当前排名'],
        ascending=[False, True]
    )
    
    return cross_platform


def export_to_csv(df: pd.DataFrame, filename: Optional[str] = None) -> str:
    """
    导出数据到 CSV 文件
    
    Args:
        df: DataFrame
        filename: 文件名，默认自动生成
    
    Returns:
        文件路径
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'popular_stocks_{timestamp}.csv'
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename


def print_summary(df: pd.DataFrame):
    """打印数据统计摘要"""
    if df.empty:
        return
    
    print("\n📊 数据统计:")
    print(f"   总记录数：{len(df)}")
    
    # 按平台统计
    platform_counts = df['平台'].value_counts()
    print("\n   按平台分布:")
    for platform, count in platform_counts.items():
        print(f"   - {platform}: {count} 条")
    
    # 按数据类型统计
    type_counts = df['数据类型'].value_counts()
    print("\n   按数据类型:")
    for dtype, count in type_counts.items():
        print(f"   - {dtype}: {count} 条")


if __name__ == "__main__":
    print("=" * 60)
    print("🔥 人气热门股票整合工具")
    print("=" * 60)
    
    # 获取所有平台的热门股票
    df = merge_all_popular(
        dongfang=True,
        tonghuashun=True,
        xueqiu=True,
        limit_per_platform=20
    )
    
    if not df.empty:
        print(f"\n✅ 共获取 {len(df)} 条热门股票数据")
        
        # 打印统计摘要
        print_summary(df)
        
        print("\n📋 数据预览 (前 10 条):")
        print(df.head(10).to_string())
        
        # 找出跨平台热门股票
        print("\n" + "=" * 60)
        print("🎯 跨平台热门股票 (在 2 个及以上平台同时热门)")
        print("=" * 60)
        cross = find_cross_platform_stocks(df)
        if not cross.empty:
            print(f"\n找到 {len(cross)} 只跨平台热门股票:\n")
            print(cross.to_string())
            
            # 导出
            filename = export_to_csv(cross, 'cross_platform_hot_stocks.csv')
            print(f"\n💾 跨平台数据已导出到：{filename}")
        else:
            print("暂无跨平台热门股票")
        
        # 导出全部数据
        all_filename = export_to_csv(df, 'all_popular_stocks.csv')
        print(f"💾 全部数据已导出到：{all_filename}")
    else:
        print("❌ 未能获取到任何数据")
