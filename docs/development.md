# 开发与测试

## 环境

按 [README](../README.md#快速开始)完成安装和数据导入。
Python 依赖由 `pyproject.toml` 和 `uv.lock` 管理，Flutter 依赖由
`frontend/pubspec.yaml` 和 `frontend/pubspec.lock` 管理。

`.env` 保存本地数据库与模型配置，不提交到版本控制。
后端默认监听 `127.0.0.1:8000`，同时提供 `/api` 接口和 `frontend/build/web` 静态文件。

## 前端构建

从项目根目录运行：

```powershell
$projectPath = & ./scripts/project-path.ps1
Push-Location (Join-Path $projectPath 'frontend')
../.runtime/flutter/bin/flutter.bat analyze
../.runtime/flutter/bin/flutter.bat build web --no-web-resources-cdn
Pop-Location
```

`project-path.ps1` 为当前检出建立独立的 ASCII 路径别名，供 Windows 的 Java 与 Flutter 工具使用。
前端请求当前站点的 `/api`，构建后通过 FastAPI 访问完整应用。
组件说明见 [frontend/README.md](../frontend/README.md)。

## 后端检查

```powershell
$env:PYTHONUTF8 = '1'
uv run ruff check backend
uv run pytest -m 'not integration' -q
# 启动 Neo4j 并完成所有数据导入后：
uv run pytest -q
```

集成检查使用实际 Neo4j 和本地来源文件。Agent 循环测试使用可控的替代模型结果；
真实模型调用由浏览器检查或评测执行器验证。

## 浏览器检查

需要 Node、可解析的 Playwright 包与本机 Edge。
从项目根目录执行，结果及截图写入被忽略的 `data/runs/browser/`：

```powershell
$env:BASE_URL = 'http://127.0.0.1:8000'
node scripts/smoke-manufacturing.cjs
node scripts/smoke-browser.cjs
```

制造检查覆盖电芯选择、履历、循环原始行和分页。
通用检查覆盖图关系、CSV 来源、中文/德文指南检索、PDF 区域引用和变更工作台。

设置 `LIVE_AGENT=1` 会使用当前模型配置，生成报告并检查保存、恢复与导出；
通用检查还会运行正常、缺资料和冲突三种变更流程。
设置 `TEST_REVIEW=1` 会填写标记为自动化测试的制造复核意见。
这些操作会保存测试记录，运行时应使用独立测试数据库。

## 数据与评测

导入器、数据标签和来源映射见[系统架构](architecture.md)。
修改文档解析后，依次运行 `battery_copilot.documents` 和 `battery_copilot.retrieval` 更新派生索引。
原始来源、文件哈希、对象关系和单位应保留在导入结果中。

[评测入口](evaluation.md)列出题库、协议和重现命令；
[v0.1.0 验证记录](validation.md)记录独立安装与功能检查的环境和结果。
评测输出使用新目录或新文件，保留此前运行的失败结果与配置。

## 录制演示

需要上述浏览器依赖，以及 PATH 中可用的 FFmpeg。
先执行 `playwright install ffmpeg` 安装 Playwright 的录像组件。
对已启动的独立演示实例运行：

```powershell
$env:BASE_URL = 'http://127.0.0.1:18000'
node scripts/record-demo.cjs
uv run python scripts/render-demo.py
```

脚本会生成真实模型报告，录制来源核对、人工意见、历史恢复与导出。
录屏、字幕和最终 MP4 写入 `data/runs/demo/`。
录制中断后可设置 `DEMO_REUSE_REPORT=1` 复用同目录事件对应的未复核报告；
已提交复核的报告不能重复提交，应生成新报告后重录。

## 贡献

问题反馈请附复现步骤、相关版本和去除密钥的错误信息。
提交修改时说明问题、行为变化与验证方式；更改公开接口或数据处理方式时同步更新文档。
依赖变更需同步锁文件。针对行为变化补充必要的验证，界面或文案调整可通过构建和实际页面检查。
