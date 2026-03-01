#!/usr/bin/env python3
"""
人气热门股票整合工具
支持：雪球热股榜、同花顺热榜、东方财富人气榜
"""
import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Optional


def get_xueqiu_hot_stocks(limit: int = 20) -> pd.DataFrame:
    """
    雪球热股榜
    https://xueqiu.com/hq
    """
    try:
        df = ak.stock_hot_deal_xq()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['排名'] = range(1, len(df)+1)
        result['代码'] = df.get('股票代码', '')
        result['名称'] = df.get('股票简称', '')
        result['关注'] = df.get('关注', 0)
        result['最新价'] = df.get('最新价', 0)
        result['平台'] = '雪球'
        result['榜单类型'] = '热股榜'
        return result
    except Exception as e:
        print(f"❌ 雪球热股榜获取失败：{e}")
        return pd.DataFrame()


def get_tonghuashun_hot_stocks(limit: int = 20) -> pd.DataFrame:
    """
    同花顺热榜 - 创新高股票
    """
    try:
        df = ak.stock_rank_cxg_ths()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['排名'] = df.get('序号', range(1, len(df)+1))
        result['代码'] = df.get('股票代码', '')
        result['名称'] = df.get('股票简称', '')
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['换手率'] = df.get('换手率', 0)
        result['最新价'] = df.get('最新价', 0)
        result['平台'] = '同花顺'
        result['榜单类型'] = '创新高榜'
        return result
    except Exception as e:
        print(f"❌ 同花顺热榜获取失败：{e}")
        return pd.DataFrame()


def get_tonghuashun_volume_stocks(limit: int = 20) -> pd.DataFrame:
    """
    同花顺热榜 - 放量上涨
    """
    try:
        df = ak.stock_rank_cxfl_ths()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        result = pd.DataFrame()
        result['排名'] = df.get('序号', range(1, len(df)+1))
        result['代码'] = df.get('股票代码', '')
        result['名称'] = df.get('股票简称', '')
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['最新价'] = df.get('最新价', 0)
        result['成交量'] = df.get('成交量', 0)
        result['放量天数'] = df.get('放量天数', 0)
        result['平台'] = '同花顺'
        result['榜单类型'] = '放量上涨榜'
        return result
    except Exception as e:
        print(f"❌ 同花顺放量榜获取失败：{e}")
        return pd.DataFrame()


def get_dongfang_popular_stocks(limit: int = 20) -> pd.DataFrame:
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
        
        # 检查是否有有效数据
        if '代码' not in df.columns or df['代码'].isna().all():
            return pd.DataFrame()
        
        result = pd.DataFrame()
        result['排名'] = df.get('当前排名', range(1, len(df)+1))
        result['代码'] = df.get('代码', '')
        result['名称'] = df.get('股票名称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌额'] = df.get('涨跌额', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '东方财富'
        result['榜单类型'] = '人气榜'
        return result
    except Exception as e:
        print(f"❌ 东方财富人气榜获取失败：{e}")
        return pd.DataFrame()


def get_dongfang_realtime_hot(limit: int = 20) -> pd.DataFrame:
    """
    东方财富实时热门
    """
    try:
        df = ak.stock_hot_rank_latest_em()
        if df is None or df.empty:
            return pd.DataFrame()
        if limit and len(df) > limit:
            df = df.head(limit)
        
        if '代码' not in df.columns or df['代码'].isna().all():
            return pd.DataFrame()
        
        result = pd.DataFrame()
        result['排名'] = range(1, len(df)+1)
        result['代码'] = df.get('代码', '')
        result['名称'] = df.get('股票名称', '')
        result['最新价'] = df.get('最新价', 0)
        result['涨跌幅'] = df.get('涨跌幅', 0)
        result['平台'] = '东方财富'
        result['榜单类型'] = '实时热门'
        return result
    except Exception as e:
        print(f"❌ 东方财富实时热门获取失败：{e}")
        return pd.DataFrame()


def merge_all_popular(
    xueqiu: bool = True,
    tonghuashun: bool = True,
    dongfang: bool = True,
    limit_per_board: int = 20
) -> pd.DataFrame:
    """
    整合所有平台的人气热门股票数据
    
    Args:
        xueqiu: 是否包含雪球
        tonghuashun: 是否包含同花顺
        dongfang: 是否包含东方财富
        limit_per_board: 每个榜单获取的股票数量
    
    Returns:
        合并后的 DataFrame
    """
    all_dfs = []
    
    if xueqiu:
        print("🔵 获取雪球热股榜...")
        df = get_xueqiu_hot_stocks(limit_per_board)
        if not df.empty:
            all_dfs.append(df)
    
    if tonghuashun:
        print("📈 获取同花顺创新高榜...")
        df = get_tonghuashun_hot_stocks(limit_per_board)
        if not df.empty:
            all_dfs.append(df)
        
        print("📊 获取同花顺放量上涨榜...")
        df = get_tonghuashun_volume_stocks(limit_per_board)
        if not df.empty:
            all_dfs.append(df)
    
    if dongfang:
        print("📊 获取东方财富人气榜...")
        df = get_dongfang_popular_stocks(limit_per_board)
        if not df.empty:
            all_dfs.append(df)
        else:
            print("⚡ 人气榜失败，尝试实时热门...")
            df = get_dongfang_realtime_hot(limit_per_board)
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
    """
    if df.empty:
        return pd.DataFrame()
    
    stock_counts = df.groupby(['代码', '名称']).agg({
        '平台': lambda x: '、'.join(sorted(set(x))),
        '排名': 'min',
        '最新价': 'first',
        '榜单类型': lambda x: '、'.join(sorted(set(x)))
    }).reset_index()
    
    stock_counts['平台数量'] = stock_counts['平台'].apply(lambda x: len(x.split('、')))
    
    cross_platform = stock_counts[stock_counts['平台数量'] >= 2].sort_values(
        by=['平台数量', '排名'],
        ascending=[False, True]
    )
    
    return cross_platform


def export_to_csv(df: pd.DataFrame, filename: Optional[str] = None) -> str:
    """导出数据到 CSV"""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'popular_stocks_{timestamp}.csv'
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename


def print_summary(df: pd.DataFrame):
    """打印数据统计"""
    if df.empty:
        return
    
    print("\n📊 数据统计:")
    print(f"   总记录数：{len(df)}")
    
    platform_counts = df['平台'].value_counts()
    print("\n   按平台分布:")
    for platform, count in platform_counts.items():
        print(f"   - {platform}: {count} 条")
    
    type_counts = df['榜单类型'].value_counts()
    print("\n   按榜单类型:")
    for dtype, count in type_counts.items():
        print(f"   - {dtype}: {count} 条")


if __name__ == "__main__":
    print("=" * 60)
    print("🔥 人气热门股票整合工具")
    print("=" * 60)
    
    df = merge_all_popular(
        xueqiu=True,
        tonghuashun=True,
        dongfang=True,
        limit_per_board=20
    )
    
    if not df.empty:
        print(f"\n✅ 共获取 {len(df)} 条热门股票数据")
        print_summary(df)
        
        print("\n📋 数据预览 (前 15 条):")
        print(df.head(15).to_string())
        
        print("\n" + "=" * 60)
        print("🎯 跨平台热门股票")
        print("=" * 60)
        cross = find_cross_platform_stocks(df)
        if not cross.empty:
            print(f"\n找到 {len(cross)} 只跨平台热门股票:\n")
            print(cross.to_string())
            export_to_csv(cross, 'cross_platform_hot_stocks.csv')
            print("\n💾 已导出到：cross_platform_hot_stocks.csv")
        else:
            print("暂无跨平台热门股票")
        
        export_to_csv(df, 'all_popular_stocks.csv')
        print("💾 全部数据已导出到：all_popular_stocks.csv")
    else:
        print("❌ 未能获取到任何数据")
