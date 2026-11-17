# 实验二 Consumer Insight Skill 设计

## 1. 本实验解决的营销问题

将消费者评论从自然语言整理为可重复调用的结构化洞察，支持后续实验按品牌、场景和痛点统计，同时避免没有证据的营销结论。

## 2. 复用上一实验的成果

复用实验一的 CSV 上传/读取思路、项目目录和 README 运行方式；本实验新增评论编码 Skill 与 JSON Schema。

## 3. 输入数据、来源与字段

输入为 `review_id`、`review_text`，可选品牌、产品、日期和评分。10 条盲测样例位于 `data/sample/reviews_10.csv`。公开页面采集由 `src/review_scraper.py` 完成；采集不到时用带 `source_type=simulated` 的 300 条可复现数据，不冒充真实评论。

## 4. 新增功能、Skill 或 Workflow

新增 `skills/consumer-insight-skill/SKILL.md`、`schemas/consumer_insight.schema.json`、确定性基线编码器和合规采集器。流程为：读取评论 → 按标签字典编码 → 绑定原文证据 → 无法判断返回 unknown → JSON Schema 校验。

## 5. 程序计算与 AI 判断的分工

程序负责字段校验、枚举约束、证据子串检查和后续计数；AI/Skill 负责语义识别、情绪与需求编码以及证据选择。AI 不负责百分比和最终排序。

## 6. 测试用例、结果与 Debug 记录

10 条边界样例覆盖正面、负面、混合、中性、空评论、只有评分、反讽、多场景、价格阻碍和无痛点。首轮 8/10 直接一致；修订后格式稳定，反讽仍要求人工复核并降低置信度。详情见 `docs/blind_test_record.md`。

## 7. 证据追溯示例

评论“通勤时降噪很安静，佩戴舒服。”输出 `need=降噪`、`scenario=通勤`，证据为“降噪很安静”；每个结论均可在 `review_text` 中定位。

## 8. 已知限制与合规说明

关键词基线无法可靠识别复杂反讽和跨句指代，必须人工复核。采集器只访问公开 HTML，遵守 robots.txt，不绕过登录、验证码、付费墙或访问限制；模拟数据明确标注，不作为真实消费者证据。

## 9. 版本号与运行方式

版本 `v0.2`。运行：`python src/consumer_insight.py --input data/sample/reviews_10.csv --output outputs/sample_insights.json`。

## 10. 小组成员贡献

请在 GitHub 提交前补充真实成员、角色、提交日期和 commit 链接。
