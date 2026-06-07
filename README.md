# Trading Journal Lite

Trading Journal Lite 是一个轻量级、本地优先的交易日志工具，用于通过 CSV 文件复盘交易记录。

它可以帮助交易员导入交易记录，计算核心绩效指标，并通过 Streamlit 仪表盘可视化交易结果。

## 功能

- CSV 交易记录导入
- Binance Futures CSV 导入
- Bybit CSV 导入
- 多单和空单 PnL 计算
- 净盈亏
- 胜率
- 平均 PnL
- 盈亏比
- 最大回撤
- 每日和每周 PnL 汇总
- 最佳和最差交易
- 资金曲线可视化
- 按交易品种统计 PnL
- 单元测试
- GitHub Actions 自动测试

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

运行应用：

```bash
streamlit run app.py
```

然后上传 Standard、Binance Futures 或 Bybit 格式的 CSV 文件。

## Standard CSV 格式

| 字段 | 是否必需 | 说明 |
|---|---:|---|
| date | 是 | 交易日期 |
| symbol | 是 | 交易品种、ticker 或合约 |
| side | 是 | `long` 或 `short` |
| qty | 是 | 仓位数量 |
| entry_price | 是 | 开仓价格 |
| exit_price | 是 | 平仓价格 |
| fee | 否 | 手续费 |

示例：

```csv
date,symbol,side,qty,entry_price,exit_price,fee
2026-05-01,BTCUSDT,long,0.1,60000,61200,4
2026-05-02,ETHUSDT,short,1,3100,3000,3
```

## 支持的导入格式

Trading Journal Lite 目前支持三种 CSV 格式：

| 格式 | 说明 |
|---|---|
| Standard | 使用标准化字段名的通用交易 CSV |
| Binance Futures | Binance Futures 风格的交易 CSV |
| Bybit | Bybit 风格的交易 CSV |

## Binance Futures CSV 格式

必需字段：

| 字段 | 说明 |
|---|---|
| Date | 交易日期 |
| Symbol | 交易品种 |
| Side | `LONG` 或 `SHORT` |
| Quantity | 仓位数量 |
| Entry Price | 开仓价格 |
| Exit Price | 平仓价格 |
| Fee | 手续费 |

示例：

```csv
Date,Symbol,Side,Quantity,Entry Price,Exit Price,Fee
2026-05-01,BTCUSDT,LONG,0.1,60000,61200,4
2026-05-02,ETHUSDT,SHORT,1,3100,3000,3
```

## Bybit CSV 格式

必需字段：

| 字段 | 说明 |
|---|---|
| Created Time | 交易日期 |
| Contract | 交易品种 |
| Side | `Buy` 或 `Sell` |
| Qty | 仓位数量 |
| Entry Price | 开仓价格 |
| Exit Price | 平仓价格 |
| Trading Fee | 手续费 |

示例：

```csv
Created Time,Contract,Side,Qty,Entry Price,Exit Price,Trading Fee
2026-05-01,BTCUSDT,Buy,0.1,60000,61200,4
2026-05-02,ETHUSDT,Sell,1,3100,3000,3
```

## 示例文件

项目中包含一个示例文件：

```text
sample_trades.csv
```

## 路线图

- [x] 添加最大回撤指标
- [x] 添加每日和每周 PnL 汇总
- [x] 添加 Binance Futures CSV 解析器
- [x] 添加 Bybit CSV 解析器
- [ ] 添加 OKX CSV 解析器
- [ ] 添加交易标签
- [ ] 添加每笔交易备注
- [ ] 添加可导出的 HTML 报告
- [ ] 添加更多风险指标

## 项目状态

本项目仍处于早期开发阶段。当前目标是提供一个简洁、可靠、基于 CSV 的个人交易复盘工具。

## 免责声明

Trading Journal Lite 不构成任何金融建议。它只是一个交易记录和绩效复盘工具。

## License

MIT
