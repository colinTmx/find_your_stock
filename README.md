# Find Your Stock 📊

股票分析和筛选工具，支持 pywencai 和 akshare 数据源。

## 功能

- 🔍 **pywencai 筛选** - 同花顺问财自然语言选股
- 📈 **akshare 行情** - 东方财富实时行情数据
- 📉 **技术分析** - 量比、涨幅、换手率等指标
- 🔥 **人气热门整合** - 多平台热门股票数据整合（新增）

## 环境

- Python 3.11+
- uv 包管理

## 安装

```bash
cd /root/find_your_stock
uv sync
```

## 使用

### 📊 股票筛选

```bash
uv run python src/stock_screen.py
```

### 🔥 人气热门股票整合

```bash
uv run python src/popular_stocks.py
```

运行后会：
1. 获取东方财富人气榜/实时热门
2. 获取同花顺涨速榜/成交量榜
3. 获取雪球热门关注/热门讨论
4. 自动识别跨平台热门股票
5. 导出 CSV 文件

### Python 代码

```python
from src.stock_screen import wencai_screen, akshare_realtime
from src.popular_stocks import merge_all_popular, find_cross_platform_stocks

# pywencai 筛选
result = wencai_screen("量比大于 1.5，涨幅 0 到 7%")

# akshare 实时行情
info = akshare_realtime("300502")  # 新易盛

# 获取多平台热门股票
df = merge_all_popular(
    dongfang=True,      # 东方财富
    tonghuashun=True,   # 同花顺
    xueqiu=True,        # 雪球
    limit_per_platform=20
)

# 找出跨平台热门股票
cross = find_cross_platform_stocks(df)
```

## 常用筛选条件

| 条件 | 示例 |
|------|------|
| 量比 | `量比大于 1.5` |
| 涨幅 | `涨幅 0 到 7%` |
| 板块 | `科技股` / `白酒` / `半导体` |
| 排除 | `非 ST` / `非科创板` |

## 项目结构

```
find_your_stock/
├── src/
│   ├── stock_screen.py      # 股票筛选工具
│   └── popular_stocks.py    # 人气热门整合工具（新增）
├── pyproject.toml           # 项目配置
├── uv.lock                  # 依赖锁定
├── README.md
└── *.csv                    # 导出的数据文件
```

## 输出示例

运行 `popular_stocks.py` 后会生成：
- `all_popular_stocks.csv` - 所有平台热门股票数据
- `cross_platform_hot_stocks.csv` - 跨平台热门股票（重点关注）

## 数据来源

| 平台 | 数据类型 | 说明 |
|------|---------|------|
| 东方财富 | 人气榜、实时热门 | 股吧人气排名 |
| 同花顺 | 涨速榜、成交量榜 | 盘中异动监控 |
| 雪球 | 热门关注、热门讨论 | 社区热度 |
