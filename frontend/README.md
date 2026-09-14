# Flutter Web 工作台

Battery Engineering Copilot 的浏览器界面，通过当前站点的 `/api` 访问 FastAPI。
构建产物位于 `build/web`，由后端直接提供。

| 文件 | 职责 |
| --- | --- |
| `lib/main.dart` | 应用布局、导航、数据上下文 |
| `lib/manufacturing.dart` | 电芯履历、循环记录、报告与人工复核 |
| `lib/pages.dart` | 部件图浏览、记录序列、工艺指南检索 |
| `lib/copilot.dart` | 工程问答与工具运行状态 |
| `lib/cases.dart`、`lib/case_form.dart` | 变更申请、修订和复核 |
| `lib/widgets.dart` | 关系图、来源弹窗和通用组件 |
| `lib/api.dart` | HTTP 请求与流式响应 |

安装与运行见[项目 README](../README.md)，构建、静态分析和浏览器检查见[开发文档](../docs/development.md)。
