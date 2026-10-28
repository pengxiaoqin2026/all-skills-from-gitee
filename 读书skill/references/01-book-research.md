# 阶段一：研究书籍

使用微信读书 skill（`weread-skills`，位于 `C:\Users\Administrator\.codex\skills\weread-skills`）。先读它的 `SKILL.md`，再按能力文档调用接口。

## 必读能力文档

- 搜索书：`search.md`
- 书籍信息：`book.md`
- 热门划线：`notes.md`
- 公开点评：`review.md`

## 接口要点

- 统一入口：`POST https://i.weread.qq.com/api/agent/gateway`
- Header：`Authorization: Bearer $WEREAD_API_KEY`
- Body 业务参数与 `api_name`、`skill_version` 平铺，不要包在 `params` 里。
- 先 `/store/search`（`scope=10`）拿 `bookId`，再 `/book/info`、`/book/chapterinfo`、`/book/bestbookmarks`、`/review/list`。
- 若环境变量 `WEREAD_API_KEY` 未设置，从本机已有配置中查找 `wrk-` 开头的 key；找不到再向用户要。

## 输出清单（对话中直接给出）

- 准确书名（含副标题、英文原名）
- 作者信息
- 出版信息
- 这本书主要解决什么问题
- 最适合做成视频讲的一条观点
- 目标观众
- 观众最容易共鸣的处境
- 可以使用书中的观点和案例
- 容易误解、不能夸大表述的内容
- 适合视频画面的视觉方向

清单必须基于微信读书返回数据；作者背景等通用知识只作补充，不编造评分、章节、划线和点评。
