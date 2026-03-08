# AI 实操型图书启动包

这套启动包把“先卖数字验证款，再决定是否做纸书”的方案落成了可执行资产。

## 目录

- `01_market_and_unit_economics.md`
  - 市场判断、渠道顺序、价格带、回本线。
- `02_topic_validation_pack.md`
  - 3 个首测题目、打分、19.9 元验证款结构、每题 10 条短视频钩子。
- `03_digital_offer_and_video_assets.md`
  - 胜出题目的 19.9 元产品页文案、私信话术、10 条短视频脚本。
- `04_paper_book_outline.md`
  - 纸书题目、目录、页数、字数、配套素材要求。
- `05_14day_execution_sprint.md`
  - 从冷启动到 go/no-go 的 14 天执行节奏。
- `06_compliance_checklist.md`
  - 不能说什么、哪些说法必须有证据、上线前审稿清单。
- `07_digital_sample_chapter.md`
  - 数字验证款样章，可直接拿去改成 PDF 初版。
- `08_validation_handbook_full_draft.md`
  - 完整数字验证款全稿源文件，可生成正式 `.docx`。
- `financial_scenarios.json`
  - 测算脚本用的场景参数。
- `validation_tracker_template.csv`
  - 首轮 30 条视频的跟踪模板。
- `scripts/generate_book_docx.py`
  - 把全稿源文件生成为 `output/doc/` 下的 `.docx` 成品。

## 推荐使用顺序

1. 先看 `02_topic_validation_pack.md`，按默认建议从 `DeepSeek 短视频脚本` 开始首测。
2. 直接套用 `03_digital_offer_and_video_assets.md` 做 19.9 元验证款和短视频发布。
3. 用 `validation_tracker_template.csv` 记录首轮 30 条内容的数据。
4. 运行 `python3 scripts/book_launch_model.py` 刷新回本测算。
5. 只有在 14 天内拿到 300 到 500 单自然成交后，才进入 `04_paper_book_outline.md`。

## 当前默认决策

- 首测产品: `7 天做出 100 条短视频脚本`
- 首测工具: `DeepSeek`
- 首测人群: `有产品或服务、但写不出持续短视频内容的人`
- 首测价格: `19.9 元`
- 纸书条件: `14 天内自然成交 300 到 500 单，且咨询率稳定`

## 快速命令

```bash
cd /Users/kb/Desktop/AI自媒体视频
python3 scripts/book_launch_model.py
python3 scripts/generate_book_docx.py
```

输出文件会写到 `output/book_launch/` 和 `output/doc/`。
