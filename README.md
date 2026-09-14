# Battery Engineering Copilot

基于知识图谱的电池工程资料助手。关联制造履历、循环测试、部件关系和工艺文档，
通过 Agent 查询证据，生成可追溯、可复核的工程报告。

[使用指南](docs/usage.md) · [系统架构](docs/architecture.md) · [开发与测试](docs/development.md) ·
[评测](docs/evaluation.md) · [版本发布](https://github.com/berlin6908/BatteryCopilot/releases)

![制造履历与循环测试](docs/images/manufacturing-workbench.png)

## 功能

- **制造履历**：从电芯对象追溯明确前驱与制造工序，查看对应对象的工艺参数。
- **检验复核**：定位循环测试原始行，生成带引用的报告，保存复核意见并导出来源快照。
- **结构查询**：浏览电池包部件、连接件和拆解记录，追溯原始 CSV 行。
- **工艺检索**：支持中文、英文、德文查询，在 PDF 原页高亮证据区域。
- **变更复核**：保存变更申请，检查工具卡和作业指导书，支持补充资料、重新分析和逐项复核。

后端使用 Python、FastAPI、Neo4j 和 LangGraph；文档处理使用 Docling、PDFium、
E5 向量检索和多语言重排；前端使用 Flutter Web。关系范围与数值由领域工具读取，
Agent 根据问题选择查询并组织回答。

## 快速开始

安装脚本支持 Windows，需要 PowerShell 7、Git 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。
脚本会准备 Python 依赖、Java、Neo4j、Flutter 和工艺指南 PDF。

```powershell
git clone https://github.com/berlin6908/BatteryCopilot.git
Set-Location BatteryCopilot
pwsh -File scripts/setup.ps1
pwsh -File scripts/start-neo4j.ps1
```

保持数据库终端运行，在另一个终端进入项目目录，首次导入数据并建立索引：

```powershell
$env:PYTHONUTF8 = '1'
uv run python -m battery_copilot.ingest
uv run python -m battery_copilot.documents
uv run python -m battery_copilot.retrieval
uv run python -m battery_copilot.manufacturing_ingest
pwsh -File scripts/start.ps1
```

打开 [工作台](http://127.0.0.1:8000) 或 [API 文档](http://127.0.0.1:8000/docs)。
后续直接运行 `pwsh -File scripts/start.ps1`，无需重复导入。
首次解析和索引会下载公开模型；KIproBatt 导入会下载约 78 MB 的数据归档。

### 配置生成模型

Neo4j 首次启动时会创建本地 `.env`。编辑其中的模型配置，保留已有数据库连接信息。

支持使用 Chat Completions 工具调用接口：

```dotenv
MODEL_PROVIDER=openai
OPENAI_BASE_URL=https://your-provider.example/v1
OPENAI_API_KEY=your-api-key
MODEL_NAME=your-tool-calling-model
```

也支持本机已登录的 Codex CLI：

```dotenv
MODEL_PROVIDER=codex
MODEL_NAME=gpt-5.6-terra
```

使用 CLI 前执行 `codex login`，并将模型名改为账号可用的模型。
后端通过独立的 `codex exec` 进程调用模型，详见[模型适配](docs/architecture.md#模型适配)。
修改配置后重启后端。制造履历、原始证据和文档检索可以独立使用；
报告生成、工程问答和变更分析需要配置生成模型。

## 使用

进入「制造履历」，选择电芯，展开工序参数，点击循环记录的行号查看来源。
生成报告后，可核对结论引用、填写人工意见，并导出包含来源快照的 Markdown。

「结构与记录」提供部件关系查询；「工艺证据」提供文档检索和页内定位；
「变更复核」提供资料修订与复核流程。

详细步骤见[使用指南](docs/usage.md)。
[三分钟视频](https://github.com/berlin6908/BatteryCopilot/releases/download/v0.1.0/battery-copilot-demo.mp4)
展示了来源核对、报告恢复、人工复核和导出。

## 数据来源

| 数据集 | 用途 | 来源与许可 |
| --- | --- | --- |
| KIproBatt v0.3.2 | 电芯试制履历、过程参数、循环统计 | [数据归档](https://zenodo.org/records/11895571) · [署名与转换说明](data/sources/kiprobatt/ATTRIBUTION.md) · CC BY 4.0 |
| KIT / WBK | 电池包结构、连接件、拆解记录 | [数据 DOI](https://doi.org/10.35097/emz24pksshndq468) · [署名](data/sources/kit-battery/ATTRIBUTION.md) · CC BY 4.0 |
| PEM / RWTH Aachen / VDMA | 电池模组与电池包生产工艺指南 | [原始出版物](https://publications.rwth-aachen.de/record/973056/) · PDF 与页图由安装过程下载、生成，不随源码分发 |

制造数据来自公开实验室记录，指南提供通用工艺知识；变更示例中的规格、工具卡和指导书是模拟输入。
系统用于资料追溯与复核，报告中的质量判断仍取决于测试条件、验收标准和人工确认。

## 开发与评测

```powershell
uv run ruff check backend
uv run pytest -m 'not integration' -q
# 数据库启动且数据导入完成后，运行全部检查：
uv run pytest -q
```

[开发文档](docs/development.md)包含前端构建、浏览器检查和贡献说明。
[评测文档](docs/evaluation.md)统一列出制造、指南检索及历史题库的协议、结果与重现命令。
不同评测集的任务和评分口径不同，分项结果及已知失败随报告公开。

## 项目结构

```text
backend/             FastAPI 服务、领域工具、数据导入与测试
frontend/            Flutter Web 工作台
scripts/             安装、启动、浏览器检查与评测工具
data/                数据署名、示例场景、评测题库与结果
docs/                使用、架构、开发与评测文档
```

本地配置、运行环境、解析缓存和原始运行日志不进入版本控制。

## 许可证

源码采用 [MIT License](LICENSE)。第三方数据、文档和依赖保留各自许可与署名要求。
