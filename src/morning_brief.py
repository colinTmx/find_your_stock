#!/usr/bin/env python3
"""
投研晨间简报
每天自动抓取宏观/市场/行业关键消息
"""
import akshare as ak
import pandas as pd
from datetime import datetime
from typing import List, Dict


def get_market_snapshot() -> str:
    """获取市场快照"""
    lines = []
    
    # A 股指数
    try:
        indices = {
            '上证指数': 'sh000001',
            '深证成指': 'sz399001',
            '创业板指': 'sz399006'
        }
        for name, symbol in indices.items():
            df = ak.stock_zh_index_daily(symbol=symbol)
            if not df.empty:
                close = df.iloc[-1]['close']
                # 计算涨跌幅
                if len(df) > 1:
                    prev = df.iloc[-2]['close']
                    change = ((close - prev) / prev) * 100
                else:
                    change = 0
                lines.append(f"• {name}: {close:.2f} ({change:+.2f}%)")
    except Exception as e:
        lines.append(f"⚠️ 指数数据获取失败")
    
    # 汇率
    try:
        df = ak.currency_boc_sina(symbol="美元", start="2026-02-28", end="2026-03-01")
        if not df.empty:
            rate = df['收盘'].iloc[-1]
            lines.append(f"• 美元汇率：{rate:.4f}")
    except:
        pass
    
    # 国债
    try:
        df = ak.bond_china_yield()
        if not df.empty:
            rate = df['中国'].iloc[-1]
            lines.append(f"• 10 年国债收益率：{rate:.2f}%")
    except:
        pass
    
    return '\n'.join(lines) if lines else "数据暂不可用"


def fetch_economic_news(limit: int = 5) -> List[str]:
    """获取宏观经济新闻"""
    news_list = []
    try:
        df = ak.news_economic_baidu()
        if df is not None and not df.empty:
            for _, row in df.head(limit).iterrows():
                title = row.get('事件', '')
                if title:
                    news_list.append(title)
    except Exception as e:
        print(f"⚠️ 经济新闻获取失败：{e}")
    return news_list


def fetch_market_news(limit: int = 5) -> List[str]:
    """获取股市新闻"""
    news_list = []
    try:
        df = ak.stock_news_em(symbol="市场快讯")
        if df is not None and not df.empty:
            for _, row in df.head(limit).iterrows():
                title = row.get('新闻标题', '')
                if title:
                    news_list.append(title)
    except Exception as e:
        print(f"⚠️ 股市新闻获取失败：{e}")
    return news_list


def fetch_sector_news(sector: str, limit: int = 3) -> List[str]:
    """获取行业新闻"""
    news_list = []
    try:
        df = ak.stock_news_em(symbol=sector)
        if df is not None and not df.empty:
            for _, row in df.head(limit).iterrows():
                title = row.get('新闻标题', '')
                if title:
                    news_list.append(title)
    except Exception as e:
        print(f"⚠️ {sector}新闻获取失败：{e}")
    return news_list


def analyze_impact(title: str) -> str:
    """简单分析影响"""
    positive = ['利好', '增长', '上涨', '突破', '支持', '复苏', '回暖']
    negative = ['利空', '下滑', '下跌', '风险', '收紧', '违约', '衰退']
    
    for kw in positive:
        if kw in title:
            return "🟢 正面"
    for kw in negative:
        if kw in title:
            return "🔴 负面"
    return "⚪ 中性"


def generate_brief() -> str:
    """生成完整简报"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    lines = []
    lines.append("=" * 70)
    lines.append(f"📊 投研晨间简报 | {now}")
    lines.append("=" * 70)
    lines.append("")
    
    # 市场快照
    print("📈 获取市场快照...")
    lines.append("**📈 市场快照**")
    lines.append(get_market_snapshot())
    lines.append("")
    
    # 宏观经济
    print("🌐 获取宏观经济新闻...")
    eco_news = fetch_economic_news(5)
    if eco_news:
        lines.append("**🌐 宏观动态 (5 条)**")
        for i, title in enumerate(eco_news[:5], 1):
            impact = analyze_impact(title)
            lines.append(f"{i}. {title}")
            lines.append(f"   → 影响：{impact}")
        lines.append("")
    
    # 股市焦点
    print("📊 获取股市新闻...")
    market_news = fetch_market_news(5)
    if market_news:
        lines.append("**📊 股市焦点 (5 条)**")
        for i, title in enumerate(market_news[:5], 1):
            impact = analyze_impact(title)
            lines.append(f"{i}. {title}")
            lines.append(f"   → 影响：{impact}")
        lines.append("")
    
    # 重点行业
    print("🏭 获取行业新闻...")
    lines.append("**🏭 重点行业**")
    for sector in ['半导体', '人工智能', '新能源']:
        sector_news = fetch_sector_news(sector, 2)
        if sector_news:
            lines.append(f"\n**{sector}**")
            for title in sector_news[:2]:
                lines.append(f"• {title}")
    
    # 今日跟踪变量
    lines.append("\n\n**🎯 今日重点跟踪变量**")
    lines.append("1. **北向资金** - 开盘后 30 分钟/收盘前 30 分钟流向")
    lines.append("2. **成交量** - 是否放量/缩量（对比前 5 日均值）")
    lines.append("3. **板块轮动** - 领涨/领跌板块及持续性")
    lines.append("4. **关键点位** - 上证指数支撑/压力位")
    
    result = '\n'.join(lines)
    print("\n" + result)
    
    return result


if __name__ == "__main__":
    generate_brief()
