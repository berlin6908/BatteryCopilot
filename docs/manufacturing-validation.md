# 制造资料核查验证 v2

本轮检查分页修复、引用选择和明确字段类型后的行为，并加强固定查询对照。
v1题库和108次原始结果保留；其源码检查点为 `14f44b8`。
v2不是在旧输出上重新评分，所有模型尝试重新运行并分别保存。

## 样本与范围

[题库](../data/manufacturing-validation/cases.json)包含8道已知失败回归题，
以及24道此前未出题的电芯对象上的问题。8道回归题补充了名称数组、整数数量、
数值/null等明确类型；没有改写其标准字段值。24题涉及12个新对象和12份不同的循环文件，
这些对象与文件均未用于v1问题。

原始归档只有12个关联循环测试的化成批次，v1已经涉及全部12个。
所以这里是**同批次新对象验证**，不是未见批次的泛化评测；同批工序和参数文件可能共享。
问题和金标准由开发助手编写及从原始归档材料化，未经过外部工程师独立标注。
原始来源、行号、节点属性及归档指纹均保留在题库及[清单](../data/manufacturing-validation/manifest.json)。

## 对照与评分

三种策略使用相同Terra模型、任务及字段类型约定，每题最多10次模型调用、16次工具调用：

- `no_data`：不提供资料，用于检查空值回答与题干提示的影响。
- `fixed`：固定读取完整明确履历、所有范围内工序参数、循环首尾各12行；
  同时用公开规则从用户问题中的 `Cycle 数字` 或 `循环数字` 抽取所求循环，并按编号读取。
  规则只看问题文本，不读取金标准、来源列表或题型标签。
- `agent`：产品实际的五个工具和取证循环，自行决定查询顺序和停止时机。

运行前已核对固定对照能取得全部32题要求的证据。这避免把“固定对照无法读取目标循环”
当成Agent能力优势，但该规则仍只覆盖本协议的明确循环编号表达，不代表完整自然语言检索。
工具的实际查询数、模型调用、token及耗时分别统计。

评分沿用v1的严格键集合、类型、数值和预设引用覆盖，并将回归和新对象成绩分开。
空值、零值、微小非零值区分；结构错误与事实取错在失败分析中分别解释。
没有逐句自动蕴含裁判，另外由开发助手抽查原始输出及来源，明确说明审查者身份。
不将引用ID可用解释成全部论断正确。

每个题目/策略组合只运行一次，不重试覆盖失败。先跑8题回归，再运行24题冻结验证；
源代码、题库、锁文件及模型配置冻结在同一运行清单中。

## 重现

先完成README安装及KIproBatt导入，然后执行：

```powershell
$env:PYTHONUTF8 = '1'
$env:HF_HUB_OFFLINE = '1'
uv run python -m battery_copilot.manufacturing_validation_cases --archive data/sources/kiprobatt/dataset-v0.3.2.zip
uv run python -m battery_copilot.manufacturing_benchmark --output data/runs/manufacturing-validation-v2 --split dev --workers 3
uv run python -m battery_copilot.manufacturing_benchmark --output data/runs/manufacturing-validation-v2 --split test --workers 3
```

原始轨迹留在被忽略的 `data/runs/`；公开仓库保存协议、题库、执行器和汇总结果。
