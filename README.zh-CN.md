# ClawProfit Guard｜龙虾合约风控官

语言版本：

- 中文版：`README.zh-CN.md`
- English: [README.md](/Users/kb/Desktop/AI自媒体视频/README.md)

ClawProfit Guard 是一个面向 `Binance USD-M Futures` 的交易前 AI 风控 Agent。

它解决的不是“下一笔做多还是做空”，而是：

- 用户在开仓前是否已经把风险配错了
- 杠杆是否过高
- 持仓是否过重
- 止损和止盈是否合理
- 当前行为和市场条件是否适合开仓

它的完整闭环是：

1. 动态问答建档
2. 账户与市场上下文同步
3. 交易评估
4. 合约预下单校验
5. 真实开仓
6. 自动挂止损 / 止盈保护单
7. 当前仓位查看 / 一键撤单 / 一键平仓

## 为什么它适合参赛

- 不是概念页，已经接上 `Binance USD-M Futures`
- 不是只打分，已经形成完整执行闭环
- 不是只有 UI，已经能真实开仓、挂保护单、看仓位、撤单和平仓
- 不是喊单机器人，而是一个更容易被评委理解的“风险闸门”

一句话定位：

- `先防可避免亏损，再追求收益。`

## 核心亮点

- 动态风险档位问答
- 接入合约账户行为做校准
- 实时市场同步
- 放行 / 预警 / 拦截三段式决策
- 自动修正建议：杠杆、持仓数量、止损、止盈
- 合约预下单校验
- 真实挂单试跑（撤单）
- 真实开仓执行（保留仓位）
- 开仓即挂止损止盈保护单
- 当前仓位 / 未实现盈亏 / 当前委托
- 一键撤单 / 一键平仓

## 快速开始

```bash
cd /Users/kb/Desktop/AI自媒体视频
python3 run.py --serve --host 127.0.0.1 --port 8080
```

打开演示页面：

- [http://127.0.0.1:8080/demo](http://127.0.0.1:8080/demo)

健康检查：

```bash
curl -s http://127.0.0.1:8080/health
```

## 演示流程

1. 完成风险问答
2. 确认系统建议档位
3. 自动同步账户与市场上下文
4. 点击 `评估交易`
5. 点击 `合约预下单校验`
6. 根据需要选择：
   - `真实挂单试跑（撤单）`
   - `真实开仓执行（保留仓位）`
7. 查看当前仓位 / 委托，或一键平仓

## 关键接口

### 风险档位

```bash
curl -s http://127.0.0.1:8080/v1/profile/recommend \
  -H 'Content-Type: application/json' \
  -d '{
    "quiz": {
      "experience_level": "intermediate",
      "risk_tolerance": "medium",
      "leverage_preference": "medium",
      "stop_loss_discipline": "always",
      "revenge_tendency": "sometimes",
      "trading_frequency": "medium",
      "max_drawdown_comfort_pct": 6
    },
    "behavior": {
      "consecutive_losses": 1,
      "trades_last_24h": 8,
      "day_pnl_pct": -1.0
    }
  }'
```

### 市场同步

```bash
curl -s 'http://127.0.0.1:8080/v1/binance/market-snapshot?symbol=BNBUSDT&side=LONG&profile=balanced'
```

### 账户同步

```bash
curl -s 'http://127.0.0.1:8080/v1/binance/account-snapshot?symbol=BNBUSDT&profile=balanced'
```

### 合约预下单校验

说明：

- 接口路径仍然叫 `/v1/binance/demo-order-test`
- 这是为了兼容旧入口名
- 当前实际行为已经是 `USD-M Futures` 的订单预览与执行准备校验

```bash
curl -s -X POST http://127.0.0.1:8080/v1/binance/demo-order-test \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 180
    }
  }'
```

### 真实开仓

```bash
curl -s -X POST http://127.0.0.1:8080/v1/binance/live-open-order \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 180,
      "margin_mode": "CROSSED"
    }
  }'
```

## 参赛材料

- [产品 PRD](/Users/kb/Desktop/AI自媒体视频/docs/PRD_v1.md)
- [60 秒视频脚本](/Users/kb/Desktop/AI自媒体视频/docs/DEMO_VIDEO_60S.md)
- [提交清单](/Users/kb/Desktop/AI自媒体视频/docs/CONTEST_SUBMISSION_CHECKLIST.md)
- [冠军版提交文案](/Users/kb/Desktop/AI自媒体视频/docs/FIRST_PRIZE_SUBMISSION.md)
- [OpenClaw 集成说明](/Users/kb/Desktop/AI自媒体视频/openclaw/README.md)

## 运行测试

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## 安全说明

这是一个风控与执行辅助工具，不是收益承诺，也不是投资建议。

- API 权限要最小化
- 演示尽量使用低风险 key
- 不要公开助记词和私钥
- 真实执行必须保持用户显式触发
