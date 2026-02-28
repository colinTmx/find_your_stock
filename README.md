# Find Your Stock 📊

股票分析和筛选工具，支持 pywencai 和 akshare 数据源。

## 功能

- 🔍 **pywencai 筛选** - 同花顺问财自然语言选股
- 📈 **akshare 行情** - 东方财富实时行情数据
- 📉 **技术分析** - 量比、涨幅、换手率等指标

## 环境

- Python 3.11+
- uv 包管理

## 安装

```bash
cd /root/find_your_stock
uv sync
```

## 使用

### 股票筛选

```bash
uv run python src/stock_screen.py
```

### Python 代码

```python
from src.stock_screen import wencai_screen, akshare_realtime

# pywencai 筛选
result = wencai_screen("量比大于 1.5，涨幅 0 到 7%")

# akshare 实时行情
info = akshare_realtime("300502")  # 新易盛
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
│   └── stock_screen.py    # 股票筛选工具
├── pyproject.toml         # 项目配置
├── uv.lock               # 依赖锁定
└── README.md
```
