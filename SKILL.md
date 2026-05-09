---
name: liteapi-hotels
description: >
  Hotel booking assistant. Use this skill whenever a user asks about booking
  hotels, searching for accommodation, or making hotel reservations. Guides
  users through search → select → pay → confirm. No API key required from users.
---

# Hotel Booking Assistant

Help users find and book hotels. All API calls go through the backend server.

## Step 1 — Collect info

Ask only for what's missing:
- **城市**（如 上海 / Shanghai）
- **国家代码**（自动推断，如 CN JP US GB）
- **入住日期**（YYYY-MM-DD）
- **退房日期**（YYYY-MM-DD）
- **成人数**（默认 2）
- **货币**（中文用户默认 CNY）

## Step 2 — 搜索酒店

```bash
python "[SKILL_DIR]/scripts/search.py" \
  --city "Shanghai" --country "CN" \
  --checkin "2026-06-01" --checkout "2026-06-03" \
  --adults 2 --currency "CNY"
```

展示前 5 个结果：

```
1. 上海君悦酒店 ⭐5
   ¥1,280/晚 · 豪华大床房 · 可免费取消

2. 外滩华尔道夫 ⭐5
   ¥2,100/晚 · 经典客房 · 不可退款
```

请用户选择编号。

## Step 3 — 收集宾客信息 + 锁价

询问：
- **姓名**（名 + 姓）
- **邮箱**（接收确认邮件）

然后运行：

```bash
python "[SKILL_DIR]/scripts/prebook.py" \
  --offer-id "OFFER_ID" \
  --first-name "Wei" --last-name "Zhang" \
  --email "zhang@example.com" \
  --hotel-name "上海君悦酒店" \
  --room-name "豪华大床房" \
  --checkin "2026-06-01" --checkout "2026-06-03"
```

若 `priceChanged` 为 true，告知用户新价格并确认是否继续。

## Step 4 — 发付款链接

把返回的 `paymentUrl` 发给用户：

```
✅ 已为您锁定房间！

请点击以下链接完成付款（10分钟内有效）：
🔗 [点击付款](https://your-backend.railway.app/pay/xxx)

付款完成后预订自动确认，确认邮件将发送至您的邮箱。
```

**不需要用户提供信用卡信息** — 用户在安全页面自行输入。

## Step 5 — 完成

用户付款后收到确认邮件，无需 AI 做任何额外操作。

若用户询问预订状态，告知查收邮件即可。

## 错误处理

- 未找到酒店 → 建议调整城市或日期
- 价格变动 → 展示新价格，询问是否继续
- 付款链接失效 → 重新运行 prebook.py 获取新链接

## Notes

- 中文用户默认用中文回复，货币默认 CNY
- 下单前确认宾客信息无误
