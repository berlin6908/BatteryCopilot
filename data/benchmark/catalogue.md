# BatteryCopilot 300 案例目录

开发集 60；测试集 240。完整答案、输入和来源见 cases.json。

## 台账核对

### inventory-001 · dev · 台账核对

为Fiat 500e准备部件备查：分别统计 insulation cap, busbar, module 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"insulation cap": 36, "busbar": 20, "module": 18}`

来源：data/sources/kit-battery/parts.csv:14; data/sources/kit-battery/parts.csv:15; data/sources/kit-battery/parts.csv:16; data/sources/kit-battery/parts.csv:17; data/sources/kit-battery/parts.csv:18; data/sources/kit-battery/parts.csv:19

### inventory-002 · dev · 台账核对

为Fiat 500e准备连接方式清点：分别统计 screwing, screw, plug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screwing": 134, "screw": 81, "plug": 62}`

来源：data/sources/kit-battery/fixations.csv:2; data/sources/kit-battery/fixations.csv:3; data/sources/kit-battery/fixations.csv:4; data/sources/kit-battery/fixations.csv:5; data/sources/kit-battery/fixations.csv:6; data/sources/kit-battery/fixations.csv:7

### inventory-003 · dev · 台账核对

为Fiat 500e准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 215, "lift_off": 94, "unplug": 62}`

来源：data/sources/kit-battery/operations.csv:2; data/sources/kit-battery/operations.csv:3; data/sources/kit-battery/operations.csv:4; data/sources/kit-battery/operations.csv:5; data/sources/kit-battery/operations.csv:6; data/sources/kit-battery/operations.csv:7

### inventory-004 · dev · 台账核对

采购核对：kit-v1:part:1007 与 kit-v1:part:1033 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:1007": "5", "kit-v1:part:1033": "2"}}`

来源：data/sources/kit-battery/parts.csv:9; data/sources/kit-battery/parts.csv:35

### inventory-005 · dev · 台账核对

台账中数字编号 1002 同时用于部件和连接件。核对 kit-v1:part:1002 与 kit-v1:fixation:1002 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:4; data/sources/kit-battery/fixations.csv:4

### inventory-006 · dev · 台账核对

为Chevrolet Spark准备部件备查：分别统计 busbar, module frame, module 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"busbar": 8, "module frame": 8, "module": 6}`

来源：data/sources/kit-battery/parts.csv:107; data/sources/kit-battery/parts.csv:108; data/sources/kit-battery/parts.csv:109; data/sources/kit-battery/parts.csv:110; data/sources/kit-battery/parts.csv:111; data/sources/kit-battery/parts.csv:112

### inventory-007 · dev · 台账核对

为Chevrolet Spark准备连接方式清点：分别统计 screw, plug, screwing 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 79, "plug": 26, "screwing": 14}`

来源：data/sources/kit-battery/fixations.csv:285; data/sources/kit-battery/fixations.csv:286; data/sources/kit-battery/fixations.csv:287; data/sources/kit-battery/fixations.csv:288; data/sources/kit-battery/fixations.csv:289; data/sources/kit-battery/fixations.csv:290

### inventory-008 · dev · 台账核对

为Chevrolet Spark准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 93, "lift_off": 27, "unplug": 26}`

来源：data/sources/kit-battery/operations.csv:377; data/sources/kit-battery/operations.csv:378; data/sources/kit-battery/operations.csv:379; data/sources/kit-battery/operations.csv:380; data/sources/kit-battery/operations.csv:381; data/sources/kit-battery/operations.csv:382

### inventory-009 · dev · 台账核对

采购核对：kit-v1:part:2021 与 kit-v1:part:2004 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:2021": "5", "kit-v1:part:2004": "2"}}`

来源：data/sources/kit-battery/parts.csv:121; data/sources/kit-battery/parts.csv:106

### inventory-010 · dev · 台账核对

台账中数字编号 2021 同时用于部件和连接件。核对 kit-v1:part:2021 与 kit-v1:fixation:2021 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "busbar", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:121; data/sources/kit-battery/fixations.csv:306

### inventory-011 · test · 台账核对

为Hyundai IONIQ 5准备部件备查：分别统计 insulation cap, busbar, module 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"insulation cap": 40, "busbar": 28, "module": 24}`

来源：data/sources/kit-battery/parts.csv:149; data/sources/kit-battery/parts.csv:150; data/sources/kit-battery/parts.csv:151; data/sources/kit-battery/parts.csv:152; data/sources/kit-battery/parts.csv:153; data/sources/kit-battery/parts.csv:154

### inventory-012 · test · 台账核对

为Hyundai IONIQ 5准备连接方式清点：分别统计 screw, screwing, plug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 98, "screwing": 98, "plug": 78}`

来源：data/sources/kit-battery/fixations.csv:430; data/sources/kit-battery/fixations.csv:431; data/sources/kit-battery/fixations.csv:432; data/sources/kit-battery/fixations.csv:433; data/sources/kit-battery/fixations.csv:434; data/sources/kit-battery/fixations.csv:435

### inventory-013 · test · 台账核对

为Hyundai IONIQ 5准备拆解技能工作量：分别统计 unscrew, unplug, lift_off 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 196, "unplug": 78, "lift_off": 71}`

来源：data/sources/kit-battery/operations.csv:545; data/sources/kit-battery/operations.csv:546; data/sources/kit-battery/operations.csv:547; data/sources/kit-battery/operations.csv:548; data/sources/kit-battery/operations.csv:549; data/sources/kit-battery/operations.csv:550

### inventory-014 · test · 台账核对

采购核对：kit-v1:part:3129 与 kit-v1:part:3044 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:3129": "4", "kit-v1:part:3044": "2"}}`

来源：data/sources/kit-battery/parts.csv:247; data/sources/kit-battery/parts.csv:178

### inventory-015 · test · 台账核对

台账中数字编号 3007 同时用于部件和连接件。核对 kit-v1:part:3007 与 kit-v1:fixation:3007 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:141; data/sources/kit-battery/fixations.csv:437

### inventory-016 · test · 台账核对

为BMW 530e准备部件备查：分别统计 HV cable, module, cooling plate 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"HV cable": 9, "module": 6, "cooling plate": 4}`

来源：data/sources/kit-battery/parts.csv:255; data/sources/kit-battery/parts.csv:256; data/sources/kit-battery/parts.csv:257; data/sources/kit-battery/parts.csv:258; data/sources/kit-battery/parts.csv:259; data/sources/kit-battery/parts.csv:260

### inventory-017 · test · 台账核对

为BMW 530e准备连接方式清点：分别统计 screw, plug, clip 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 87, "plug": 24, "clip": 17}`

来源：data/sources/kit-battery/fixations.csv:750; data/sources/kit-battery/fixations.csv:751; data/sources/kit-battery/fixations.csv:752; data/sources/kit-battery/fixations.csv:753; data/sources/kit-battery/fixations.csv:754; data/sources/kit-battery/fixations.csv:755

### inventory-018 · test · 台账核对

为BMW 530e准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 87, "lift_off": 25, "unplug": 24}`

来源：data/sources/kit-battery/operations.csv:932; data/sources/kit-battery/operations.csv:933; data/sources/kit-battery/operations.csv:934; data/sources/kit-battery/operations.csv:935; data/sources/kit-battery/operations.csv:936; data/sources/kit-battery/operations.csv:937

### inventory-019 · test · 台账核对

采购核对：kit-v1:part:4009 与 kit-v1:part:4024 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:4009": "5", "kit-v1:part:4024": "3"}}`

来源：data/sources/kit-battery/parts.csv:259; data/sources/kit-battery/parts.csv:274

### inventory-020 · test · 台账核对

台账中数字编号 4009 同时用于部件和连接件。核对 kit-v1:part:4009 与 kit-v1:fixation:4009 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "HV cable", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:259; data/sources/kit-battery/fixations.csv:759

### inventory-021 · test · 台账核对

为Chevrolet Volt准备部件备查：分别统计 LV cable, module clamp, coolant tubing 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"LV cable": 9, "module clamp": 8, "coolant tubing": 6}`

来源：data/sources/kit-battery/parts.csv:291; data/sources/kit-battery/parts.csv:292; data/sources/kit-battery/parts.csv:293; data/sources/kit-battery/parts.csv:294; data/sources/kit-battery/parts.csv:295; data/sources/kit-battery/parts.csv:296

### inventory-022 · test · 台账核对

为Chevrolet Volt准备连接方式清点：分别统计 screw, screwing, plug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 53, "screwing": 48, "plug": 18}`

来源：data/sources/kit-battery/fixations.csv:885; data/sources/kit-battery/fixations.csv:886; data/sources/kit-battery/fixations.csv:887; data/sources/kit-battery/fixations.csv:888; data/sources/kit-battery/fixations.csv:889; data/sources/kit-battery/fixations.csv:890

### inventory-023 · test · 台账核对

为Chevrolet Volt准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 101, "lift_off": 32, "unplug": 18}`

来源：data/sources/kit-battery/operations.csv:1090; data/sources/kit-battery/operations.csv:1091; data/sources/kit-battery/operations.csv:1092; data/sources/kit-battery/operations.csv:1093; data/sources/kit-battery/operations.csv:1094; data/sources/kit-battery/operations.csv:1095

### inventory-024 · test · 台账核对

采购核对：kit-v1:part:5017 与 kit-v1:part:5007 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:5017": "5", "kit-v1:part:5007": "3"}}`

来源：data/sources/kit-battery/parts.csv:295; data/sources/kit-battery/parts.csv:285

### inventory-025 · test · 台账核对

台账中数字编号 5017 同时用于部件和连接件。核对 kit-v1:part:5017 与 kit-v1:fixation:5017 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "LV cable", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:295; data/sources/kit-battery/fixations.csv:902

### inventory-026 · test · 台账核对

为Volvo EX30准备部件备查：分别统计 busbar, insulation cap, busbar bracket 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"busbar": 10, "insulation cap": 8, "busbar bracket": 5}`

来源：data/sources/kit-battery/parts.csv:316; data/sources/kit-battery/parts.csv:317; data/sources/kit-battery/parts.csv:318; data/sources/kit-battery/parts.csv:319; data/sources/kit-battery/parts.csv:320; data/sources/kit-battery/parts.csv:321

### inventory-027 · test · 台账核对

为Volvo EX30准备连接方式清点：分别统计 screw, plug, cable tie 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 116, "plug": 21, "cable tie": 21}`

来源：data/sources/kit-battery/fixations.csv:1022; data/sources/kit-battery/fixations.csv:1023; data/sources/kit-battery/fixations.csv:1024; data/sources/kit-battery/fixations.csv:1025; data/sources/kit-battery/fixations.csv:1026; data/sources/kit-battery/fixations.csv:1027

### inventory-028 · test · 台账核对

为Volvo EX30准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 123, "lift_off": 33, "unplug": 21}`

来源：data/sources/kit-battery/operations.csv:1257; data/sources/kit-battery/operations.csv:1258; data/sources/kit-battery/operations.csv:1259; data/sources/kit-battery/operations.csv:1260; data/sources/kit-battery/operations.csv:1261; data/sources/kit-battery/operations.csv:1262

### inventory-029 · test · 台账核对

采购核对：kit-v1:part:6034 与 kit-v1:part:6007 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:6034": "2", "kit-v1:part:6007": "6"}}`

来源：data/sources/kit-battery/parts.csv:348; data/sources/kit-battery/parts.csv:321

### inventory-030 · test · 台账核对

台账中数字编号 6017 同时用于部件和连接件。核对 kit-v1:part:6017 与 kit-v1:fixation:6017 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:331; data/sources/kit-battery/fixations.csv:1038

### inventory-031 · test · 台账核对

为BMW 330e准备部件备查：分别统计 HV cable, module, housing cover 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"HV cable": 8, "module": 5, "housing cover": 1}`

来源：data/sources/kit-battery/parts.csv:356; data/sources/kit-battery/parts.csv:359; data/sources/kit-battery/parts.csv:360; data/sources/kit-battery/parts.csv:361; data/sources/kit-battery/parts.csv:362; data/sources/kit-battery/parts.csv:363

### inventory-032 · test · 台账核对

为BMW 330e准备连接方式清点：分别统计 screw, plug, cable tie 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 75, "plug": 21, "cable tie": 12}`

来源：data/sources/kit-battery/fixations.csv:1208; data/sources/kit-battery/fixations.csv:1209; data/sources/kit-battery/fixations.csv:1210; data/sources/kit-battery/fixations.csv:1211; data/sources/kit-battery/fixations.csv:1212; data/sources/kit-battery/fixations.csv:1213

### inventory-033 · test · 台账核对

为BMW 330e准备拆解技能工作量：分别统计 unscrew, unplug, lift_off 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 72, "unplug": 21, "lift_off": 17}`

来源：data/sources/kit-battery/operations.csv:1468; data/sources/kit-battery/operations.csv:1469; data/sources/kit-battery/operations.csv:1470; data/sources/kit-battery/operations.csv:1471; data/sources/kit-battery/operations.csv:1472; data/sources/kit-battery/operations.csv:1473

### inventory-034 · test · 台账核对

采购核对：kit-v1:part:7007 与 kit-v1:part:7013 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:7007": "5", "kit-v1:part:7013": "3"}}`

来源：data/sources/kit-battery/parts.csv:363; data/sources/kit-battery/parts.csv:369

### inventory-035 · test · 台账核对

台账中数字编号 7016 同时用于部件和连接件。核对 kit-v1:part:7016 与 kit-v1:fixation:7016 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:372; data/sources/kit-battery/fixations.csv:1224

### inventory-036 · test · 台账核对

为MG ZS准备部件备查：分别统计 insulation cap, busbar, module 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"insulation cap": 36, "busbar": 19, "module": 18}`

来源：data/sources/kit-battery/parts.csv:392; data/sources/kit-battery/parts.csv:393; data/sources/kit-battery/parts.csv:394; data/sources/kit-battery/parts.csv:395; data/sources/kit-battery/parts.csv:396; data/sources/kit-battery/parts.csv:397

### inventory-037 · test · 台账核对

为MG ZS准备连接方式清点：分别统计 screw, plug, cable tie 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 192, "plug": 34, "cable tie": 23}`

来源：data/sources/kit-battery/fixations.csv:1329; data/sources/kit-battery/fixations.csv:1330; data/sources/kit-battery/fixations.csv:1331; data/sources/kit-battery/fixations.csv:1332; data/sources/kit-battery/fixations.csv:1333; data/sources/kit-battery/fixations.csv:1334

### inventory-038 · test · 台账核对

为MG ZS准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 192, "lift_off": 89, "unplug": 34}`

来源：data/sources/kit-battery/operations.csv:1599; data/sources/kit-battery/operations.csv:1600; data/sources/kit-battery/operations.csv:1601; data/sources/kit-battery/operations.csv:1602; data/sources/kit-battery/operations.csv:1603; data/sources/kit-battery/operations.csv:1604

### inventory-039 · test · 台账核对

采购核对：kit-v1:part:8034 与 kit-v1:part:8081 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:8034": "5", "kit-v1:part:8081": "10"}}`

来源：data/sources/kit-battery/parts.csv:414; data/sources/kit-battery/parts.csv:461

### inventory-040 · test · 台账核对

台账中数字编号 8001 同时用于部件和连接件。核对 kit-v1:part:8001 与 kit-v1:fixation:8001 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:381; data/sources/kit-battery/fixations.csv:1330

### inventory-041 · test · 台账核对

为Mitsubishi Outlander准备部件备查：分别统计 insulation cap, busbar, module 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"insulation cap": 20, "busbar": 14, "module": 5}`

来源：data/sources/kit-battery/parts.csv:493; data/sources/kit-battery/parts.csv:494; data/sources/kit-battery/parts.csv:495; data/sources/kit-battery/parts.csv:496; data/sources/kit-battery/parts.csv:497; data/sources/kit-battery/parts.csv:498

### inventory-042 · test · 台账核对

为Mitsubishi Outlander准备连接方式清点：分别统计 screw, plug, screwing 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 79, "plug": 27, "screwing": 22}`

来源：data/sources/kit-battery/fixations.csv:1585; data/sources/kit-battery/fixations.csv:1586; data/sources/kit-battery/fixations.csv:1587; data/sources/kit-battery/fixations.csv:1588; data/sources/kit-battery/fixations.csv:1589; data/sources/kit-battery/fixations.csv:1590

### inventory-043 · test · 台账核对

为Mitsubishi Outlander准备拆解技能工作量：分别统计 unscrew, lift_off, unplug 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 101, "lift_off": 51, "unplug": 27}`

来源：data/sources/kit-battery/operations.csv:1927; data/sources/kit-battery/operations.csv:1928; data/sources/kit-battery/operations.csv:1929; data/sources/kit-battery/operations.csv:1930; data/sources/kit-battery/operations.csv:1931; data/sources/kit-battery/operations.csv:1932

### inventory-044 · test · 台账核对

采购核对：kit-v1:part:9005 与 kit-v1:part:9043 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:9005": "2", "kit-v1:part:9043": "8"}}`

来源：data/sources/kit-battery/parts.csv:482; data/sources/kit-battery/parts.csv:520

### inventory-045 · test · 台账核对

台账中数字编号 9005 同时用于部件和连接件。核对 kit-v1:part:9005 与 kit-v1:fixation:9005 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "HV cable", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:482; data/sources/kit-battery/fixations.csv:1590

### inventory-046 · test · 台账核对

为BMW i3准备部件备查：分别统计 HV cable, module, module frame 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"HV cable": 12, "module": 8, "module frame": 5}`

来源：data/sources/kit-battery/parts.csv:536; data/sources/kit-battery/parts.csv:537; data/sources/kit-battery/parts.csv:538; data/sources/kit-battery/parts.csv:539; data/sources/kit-battery/parts.csv:540; data/sources/kit-battery/parts.csv:541

### inventory-047 · test · 台账核对

为BMW i3准备连接方式清点：分别统计 screw, plug, fixed 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"screw": 124, "plug": 20, "fixed": 17}`

来源：data/sources/kit-battery/fixations.csv:1721; data/sources/kit-battery/fixations.csv:1722; data/sources/kit-battery/fixations.csv:1723; data/sources/kit-battery/fixations.csv:1724; data/sources/kit-battery/fixations.csv:1725; data/sources/kit-battery/fixations.csv:1726

### inventory-048 · test · 台账核对

为BMW i3准备拆解技能工作量：分别统计 unscrew, unplug, unclip 的记录条数。返回以原始英文类别为键、整数数量为值的对象。

答案：`{"unscrew": 124, "unplug": 18, "unclip": 16}`

来源：data/sources/kit-battery/operations.csv:2110; data/sources/kit-battery/operations.csv:2111; data/sources/kit-battery/operations.csv:2112; data/sources/kit-battery/operations.csv:2113; data/sources/kit-battery/operations.csv:2114; data/sources/kit-battery/operations.csv:2115

### inventory-049 · test · 台账核对

采购核对：kit-v1:part:10017 与 kit-v1:part:10007 的原始部件编号分别是什么？返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。

答案：`{"part_numbers": {"kit-v1:part:10017": "7", "kit-v1:part:10007": "5"}}`

来源：data/sources/kit-battery/parts.csv:550; data/sources/kit-battery/parts.csv:540

### inventory-050 · test · 台账核对

台账中数字编号 10021 同时用于部件和连接件。核对 kit-v1:part:10021 与 kit-v1:fixation:10021 的类别，返回 part_class 和 fixation_class，保留原始英文类别。

答案：`{"part_class": "BMS", "fixation_class": "screw"}`

来源：data/sources/kit-battery/parts.csv:554; data/sources/kit-battery/fixations.csv:1742

## 连接关系

### connections-001 · dev · 连接关系

变更前核对 kit-v1:fixation:1281 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:1041", "to_part": "kit-v1:part:1001", "removal_operations": ["kit-v1:operation:1372"]}`

来源：data/sources/kit-battery/fixations.csv:283; data/sources/kit-battery/operations.csv:374

### connections-002 · dev · 连接关系

评估 kit-v1:fixation:1164 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "busbar", "to_class": "service disconnect", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:166; data/sources/kit-battery/parts.csv:95; data/sources/kit-battery/parts.csv:37

### connections-003 · dev · 连接关系

两个连接件 kit-v1:fixation:1097、kit-v1:fixation:1171 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:99; data/sources/kit-battery/fixations.csv:173

### connections-004 · dev · 连接关系

为复核清单补充 kit-v1:part:1002 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:1079"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:4; data/sources/kit-battery/operations.csv:81

### connections-005 · dev · 连接关系

审查 kit-v1:operation:1372 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:1281", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:374; data/sources/kit-battery/fixations.csv:283

### connections-006 · dev · 连接关系

变更前核对 kit-v1:fixation:2164 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:2012", "to_part": "kit-v1:part:2001", "removal_operations": ["kit-v1:operation:2169"]}`

来源：data/sources/kit-battery/fixations.csv:424; data/sources/kit-battery/operations.csv:531

### connections-007 · dev · 连接关系

评估 kit-v1:fixation:2092 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "busbar", "to_class": "module", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:364; data/sources/kit-battery/parts.csv:124; data/sources/kit-battery/parts.csv:108

### connections-008 · dev · 连接关系

两个连接件 kit-v1:fixation:2155、kit-v1:fixation:2085 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:415; data/sources/kit-battery/fixations.csv:357

### connections-009 · dev · 连接关系

为复核清单补充 kit-v1:part:2022 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:2094"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:122; data/sources/kit-battery/operations.csv:456

### connections-010 · dev · 连接关系

审查 kit-v1:operation:2173 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:2168", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:535; data/sources/kit-battery/fixations.csv:428

### connections-011 · test · 连接关系

变更前核对 kit-v1:fixation:3067 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:3015", "to_part": "kit-v1:part:3002", "removal_operations": ["kit-v1:operation:3128"]}`

来源：data/sources/kit-battery/fixations.csv:497; data/sources/kit-battery/operations.csv:617

### connections-012 · test · 连接关系

评估 kit-v1:fixation:3062 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "service disconnect cover", "to_class": "service disconnect", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:492; data/sources/kit-battery/parts.csv:179; data/sources/kit-battery/parts.csv:137

### connections-013 · test · 连接关系

两个连接件 kit-v1:fixation:3316、kit-v1:fixation:3276 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:736; data/sources/kit-battery/fixations.csv:696

### connections-014 · test · 连接关系

为复核清单补充 kit-v1:part:3007 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:3315"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:141; data/sources/kit-battery/operations.csv:794

### connections-015 · test · 连接关系

审查 kit-v1:operation:3128 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:3067", "target_kind": "fixation", "target_class": "clip"}`

来源：data/sources/kit-battery/operations.csv:617; data/sources/kit-battery/fixations.csv:497

### connections-016 · test · 连接关系

变更前核对 kit-v1:fixation:4138 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:4004", "to_part": "kit-v1:part:4002", "removal_operations": ["kit-v1:operation:4160"]}`

来源：data/sources/kit-battery/fixations.csv:882; data/sources/kit-battery/operations.csv:1086

### connections-017 · test · 连接关系

评估 kit-v1:fixation:4091 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "HV cable", "to_class": "housing bottom", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:839; data/sources/kit-battery/parts.csv:255; data/sources/kit-battery/parts.csv:252

### connections-018 · test · 连接关系

两个连接件 kit-v1:fixation:4076、kit-v1:fixation:4073 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:824; data/sources/kit-battery/fixations.csv:821

### connections-019 · test · 连接关系

为复核清单补充 kit-v1:part:4009 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:4064"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:259; data/sources/kit-battery/operations.csv:996

### connections-020 · test · 连接关系

审查 kit-v1:operation:4158 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:4136", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1084; data/sources/kit-battery/fixations.csv:880

### connections-021 · test · 连接关系

变更前核对 kit-v1:fixation:5071 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:5018", "to_part": "kit-v1:part:5012", "removal_operations": ["kit-v1:operation:5080"]}`

来源：data/sources/kit-battery/fixations.csv:956; data/sources/kit-battery/operations.csv:1170

### connections-022 · test · 连接关系

评估 kit-v1:fixation:5047 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "busbar", "to_class": "service disconnect", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:932; data/sources/kit-battery/parts.csv:286; data/sources/kit-battery/parts.csv:281

### connections-023 · test · 连接关系

两个连接件 kit-v1:fixation:5066、kit-v1:fixation:5087 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:951; data/sources/kit-battery/fixations.csv:972

### connections-024 · test · 连接关系

为复核清单补充 kit-v1:part:5017 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:5077"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:295; data/sources/kit-battery/operations.csv:1167

### connections-025 · test · 连接关系

审查 kit-v1:operation:5080 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:5071", "target_kind": "fixation", "target_class": "clip"}`

来源：data/sources/kit-battery/operations.csv:1170; data/sources/kit-battery/fixations.csv:956

### connections-026 · test · 连接关系

变更前核对 kit-v1:fixation:6151 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:6007", "to_part": "kit-v1:part:6041", "removal_operations": ["kit-v1:operation:6087"]}`

来源：data/sources/kit-battery/fixations.csv:1172; data/sources/kit-battery/operations.csv:1344

### connections-027 · test · 连接关系

评估 kit-v1:fixation:6174 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "wire harness", "to_class": "disconnect unit cover", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:1195; data/sources/kit-battery/parts.csv:334; data/sources/kit-battery/parts.csv:332

### connections-028 · test · 连接关系

两个连接件 kit-v1:fixation:6160、kit-v1:fixation:6176 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": ["kit-v1:part:6020"]}`

来源：data/sources/kit-battery/fixations.csv:1181; data/sources/kit-battery/fixations.csv:1197

### connections-029 · test · 连接关系

为复核清单补充 kit-v1:part:6017 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:6070"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:331; data/sources/kit-battery/operations.csv:1327

### connections-030 · test · 连接关系

审查 kit-v1:operation:6150 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:6157", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1407; data/sources/kit-battery/fixations.csv:1178

### connections-031 · test · 连接关系

变更前核对 kit-v1:fixation:7109 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:7006", "to_part": "kit-v1:part:7001", "removal_operations": ["kit-v1:operation:7120"]}`

来源：data/sources/kit-battery/fixations.csv:1301; data/sources/kit-battery/operations.csv:1568

### connections-032 · test · 连接关系

评估 kit-v1:fixation:7137 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "HV cable", "to_class": "module", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:1325; data/sources/kit-battery/parts.csv:364; data/sources/kit-battery/parts.csv:368

### connections-033 · test · 连接关系

两个连接件 kit-v1:fixation:7099、kit-v1:fixation:7132 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:1294; data/sources/kit-battery/fixations.csv:1320

### connections-034 · test · 连接关系

为复核清单补充 kit-v1:part:7006 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:7124"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:362; data/sources/kit-battery/operations.csv:1572

### connections-035 · test · 连接关系

审查 kit-v1:operation:7120 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:7109", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1568; data/sources/kit-battery/fixations.csv:1301

### connections-036 · test · 连接关系

变更前核对 kit-v1:fixation:8249 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:8092", "to_part": "kit-v1:part:8004", "removal_operations": ["kit-v1:operation:8333"]}`

来源：data/sources/kit-battery/fixations.csv:1566; data/sources/kit-battery/operations.csv:1915

### connections-037 · test · 连接关系

评估 kit-v1:fixation:8163 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "busbar", "to_class": "housing bottom", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:1480; data/sources/kit-battery/parts.csv:469; data/sources/kit-battery/parts.csv:384

### connections-038 · test · 连接关系

两个连接件 kit-v1:fixation:8238、kit-v1:fixation:8267 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": ["kit-v1:part:8002"]}`

来源：data/sources/kit-battery/fixations.csv:1555; data/sources/kit-battery/fixations.csv:1583

### connections-039 · test · 连接关系

为复核清单补充 kit-v1:part:8001 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:8024"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:381; data/sources/kit-battery/operations.csv:1623

### connections-040 · test · 连接关系

审查 kit-v1:operation:8326 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:8238", "target_kind": "fixation", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1908; data/sources/kit-battery/fixations.csv:1555

### connections-041 · test · 连接关系

变更前核对 kit-v1:fixation:9040 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:9005", "to_part": "kit-v1:part:9006", "removal_operations": ["kit-v1:operation:9041"]}`

来源：data/sources/kit-battery/fixations.csv:1625; data/sources/kit-battery/operations.csv:1968

### connections-042 · test · 连接关系

评估 kit-v1:fixation:9066 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "busbar", "to_class": "service disconnect", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:1651; data/sources/kit-battery/parts.csv:498; data/sources/kit-battery/parts.csv:492

### connections-043 · test · 连接关系

两个连接件 kit-v1:fixation:9131、kit-v1:fixation:9047 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": ["kit-v1:part:9001"]}`

来源：data/sources/kit-battery/fixations.csv:1716; data/sources/kit-battery/fixations.csv:1632

### connections-044 · test · 连接关系

为复核清单补充 kit-v1:part:9005 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:9044"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:482; data/sources/kit-battery/operations.csv:1971

### connections-045 · test · 连接关系

审查 kit-v1:operation:9040 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:fixation:9039", "target_kind": "fixation", "target_class": "clip"}`

来源：data/sources/kit-battery/operations.csv:1967; data/sources/kit-battery/fixations.csv:1624

### connections-046 · test · 连接关系

变更前核对 kit-v1:fixation:10079 的两端：返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。

答案：`{"from_part": "kit-v1:part:10016", "to_part": "kit-v1:part:10007", "removal_operations": ["kit-v1:operation:10076"]}`

来源：data/sources/kit-battery/fixations.csv:1800; data/sources/kit-battery/operations.csv:2186

### connections-047 · test · 连接关系

评估 kit-v1:fixation:10170 的关联范围：读取其两端部件，返回 from_class、to_class（英文类别）和 same_class（布尔值）。

答案：`{"from_class": "BMS", "to_class": "disconnect unit", "same_class": false}`

来源：data/sources/kit-battery/fixations.csv:1891; data/sources/kit-battery/parts.csv:554; data/sources/kit-battery/parts.csv:535

### connections-048 · test · 连接关系

两个连接件 kit-v1:fixation:10060、kit-v1:fixation:10176 是否涉及共同部件？返回 shared_parts（共有部件 UID 列表，若无则空列表）。

答案：`{"shared_parts": []}`

来源：data/sources/kit-battery/fixations.csv:1781; data/sources/kit-battery/fixations.csv:1896

### connections-049 · test · 连接关系

为复核清单补充 kit-v1:part:10000 的已记录移除方法：返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。

答案：`{"operation_uids": ["kit-v1:operation:10060"], "skills": ["lift_off"]}`

来源：data/sources/kit-battery/parts.csv:533; data/sources/kit-battery/operations.csv:2170

### connections-050 · test · 连接关系

审查 kit-v1:operation:10165 的操作对象：返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。

答案：`{"target_uid": "kit-v1:part:10003", "target_kind": "part", "target_class": "module"}`

来源：data/sources/kit-battery/operations.csv:2275; data/sources/kit-battery/parts.csv:536

## 记录顺序

### sequence-001 · dev · 记录顺序

完成记录操作 kit-v1:operation:1370 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:1371", "target_uid": "kit-v1:fixation:1280", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:372; data/sources/kit-battery/operations.csv:373; data/sources/kit-battery/fixations.csv:282

### sequence-002 · dev · 记录顺序

按 NEXT 从 kit-v1:operation:1369 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:1370", "kit-v1:operation:1371"], "target_uids": ["kit-v1:fixation:1279", "kit-v1:fixation:1280"]}`

来源：data/sources/kit-battery/operations.csv:371; data/sources/kit-battery/operations.csv:372; data/sources/kit-battery/operations.csv:373

### sequence-003 · dev · 记录顺序

检查记录操作 kit-v1:operation:1140 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:1139", "previous_target": "kit-v1:part:1053"}`

来源：data/sources/kit-battery/operations.csv:142; data/sources/kit-battery/operations.csv:141

### sequence-004 · dev · 记录顺序

从 kit-v1:operation:1285 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:1285", "kit-v1:operation:1286", "kit-v1:operation:1287", "kit-v1:operation:1288"], "skills": ["lift_off", "lift_off", "lift_off", "lift_off"]}`

来源：data/sources/kit-battery/operations.csv:287; data/sources/kit-battery/operations.csv:288; data/sources/kit-battery/operations.csv:289; data/sources/kit-battery/operations.csv:290

### sequence-005 · dev · 记录顺序

kit-v1:operation:1286 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:part:1062", "next_target": "kit-v1:part:1065"}`

来源：data/sources/kit-battery/operations.csv:288; data/sources/kit-battery/operations.csv:289

### sequence-006 · dev · 记录顺序

完成记录操作 kit-v1:operation:2176 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:2177", "target_uid": "kit-v1:fixation:2159", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:538; data/sources/kit-battery/operations.csv:539; data/sources/kit-battery/fixations.csv:419

### sequence-007 · dev · 记录顺序

按 NEXT 从 kit-v1:operation:2178 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:2179", "kit-v1:operation:2180"], "target_uids": ["kit-v1:fixation:2161", "kit-v1:fixation:2162"]}`

来源：data/sources/kit-battery/operations.csv:540; data/sources/kit-battery/operations.csv:541; data/sources/kit-battery/operations.csv:542

### sequence-008 · dev · 记录顺序

检查记录操作 kit-v1:operation:2174 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:2173", "previous_target": "kit-v1:fixation:2168"}`

来源：data/sources/kit-battery/operations.csv:536; data/sources/kit-battery/operations.csv:535

### sequence-009 · dev · 记录顺序

从 kit-v1:operation:2173 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:2173", "kit-v1:operation:2174", "kit-v1:operation:2175", "kit-v1:operation:2176"], "skills": ["cut", "cut", "lift_off", "cut"]}`

来源：data/sources/kit-battery/operations.csv:535; data/sources/kit-battery/operations.csv:536; data/sources/kit-battery/operations.csv:537; data/sources/kit-battery/operations.csv:538

### sequence-010 · dev · 记录顺序

kit-v1:operation:2078 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:2074", "next_target": "kit-v1:fixation:2075"}`

来源：data/sources/kit-battery/operations.csv:442; data/sources/kit-battery/operations.csv:443

### sequence-011 · test · 记录顺序

完成记录操作 kit-v1:operation:3128 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:3129", "target_uid": "kit-v1:fixation:3068", "target_class": "screwing"}`

来源：data/sources/kit-battery/operations.csv:617; data/sources/kit-battery/operations.csv:618; data/sources/kit-battery/fixations.csv:498

### sequence-012 · test · 记录顺序

按 NEXT 从 kit-v1:operation:3062 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:3063", "kit-v1:operation:3064"], "target_uids": ["kit-v1:part:3001", "kit-v1:fixation:3062"]}`

来源：data/sources/kit-battery/operations.csv:607; data/sources/kit-battery/operations.csv:608; data/sources/kit-battery/operations.csv:609

### sequence-013 · test · 记录顺序

检查记录操作 kit-v1:operation:3313 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:3452", "previous_target": "kit-v1:part:3014"}`

来源：data/sources/kit-battery/operations.csv:792; data/sources/kit-battery/operations.csv:931

### sequence-014 · test · 记录顺序

从 kit-v1:operation:3071 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:3071", "kit-v1:operation:3404", "kit-v1:operation:3405", "kit-v1:operation:3128"], "skills": ["lift_off", "open", "open", "cut"]}`

来源：data/sources/kit-battery/operations.csv:616; data/sources/kit-battery/operations.csv:883; data/sources/kit-battery/operations.csv:884; data/sources/kit-battery/operations.csv:617

### sequence-015 · test · 记录顺序

kit-v1:operation:3155 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:part:3023", "next_target": "kit-v1:part:3063"}`

来源：data/sources/kit-battery/operations.csv:644; data/sources/kit-battery/operations.csv:895

### sequence-016 · test · 记录顺序

完成记录操作 kit-v1:operation:4158 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:4159", "target_uid": "kit-v1:fixation:4137", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1084; data/sources/kit-battery/operations.csv:1085; data/sources/kit-battery/fixations.csv:881

### sequence-017 · test · 记录顺序

按 NEXT 从 kit-v1:operation:4159 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:4160", "kit-v1:operation:4161"], "target_uids": ["kit-v1:fixation:4138", "kit-v1:fixation:4139"]}`

来源：data/sources/kit-battery/operations.csv:1085; data/sources/kit-battery/operations.csv:1086; data/sources/kit-battery/operations.csv:1087

### sequence-018 · test · 记录顺序

检查记录操作 kit-v1:operation:4084 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:4083", "previous_target": "kit-v1:fixation:4074"}`

来源：data/sources/kit-battery/operations.csv:1014; data/sources/kit-battery/operations.csv:1013

### sequence-019 · test · 记录顺序

从 kit-v1:operation:4078 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:4078", "kit-v1:operation:4079", "kit-v1:operation:4080", "kit-v1:operation:4081"], "skills": ["cut", "cut", "lift_off", "unscrew"]}`

来源：data/sources/kit-battery/operations.csv:1008; data/sources/kit-battery/operations.csv:1009; data/sources/kit-battery/operations.csv:1010; data/sources/kit-battery/operations.csv:1011

### sequence-020 · test · 记录顺序

kit-v1:operation:4083 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:4074", "next_target": "kit-v1:part:4023"}`

来源：data/sources/kit-battery/operations.csv:1013; data/sources/kit-battery/operations.csv:1014

### sequence-021 · test · 记录顺序

完成记录操作 kit-v1:operation:5080 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:5081", "target_uid": "kit-v1:fixation:5072", "target_class": "clip"}`

来源：data/sources/kit-battery/operations.csv:1170; data/sources/kit-battery/operations.csv:1171; data/sources/kit-battery/fixations.csv:957

### sequence-022 · test · 记录顺序

按 NEXT 从 kit-v1:operation:5095 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:5096", "kit-v1:operation:5097"], "target_uids": ["kit-v1:fixation:5084", "kit-v1:part:5021"]}`

来源：data/sources/kit-battery/operations.csv:1185; data/sources/kit-battery/operations.csv:1186; data/sources/kit-battery/operations.csv:1187

### sequence-023 · test · 记录顺序

检查记录操作 kit-v1:operation:5078 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:5077", "previous_target": "kit-v1:part:5017"}`

来源：data/sources/kit-battery/operations.csv:1168; data/sources/kit-battery/operations.csv:1167

### sequence-024 · test · 记录顺序

从 kit-v1:operation:5096 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:5096", "kit-v1:operation:5097", "kit-v1:operation:5098", "kit-v1:operation:5099"], "skills": ["cut", "lift_off", "unscrew", "unscrew"]}`

来源：data/sources/kit-battery/operations.csv:1186; data/sources/kit-battery/operations.csv:1187; data/sources/kit-battery/operations.csv:1188; data/sources/kit-battery/operations.csv:1189

### sequence-025 · test · 记录顺序

kit-v1:operation:5077 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:part:5017", "next_target": "kit-v1:fixation:5069"}`

来源：data/sources/kit-battery/operations.csv:1167; data/sources/kit-battery/operations.csv:1168

### sequence-026 · test · 记录顺序

完成记录操作 kit-v1:operation:6150 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:6151", "target_uid": "kit-v1:fixation:6158", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1407; data/sources/kit-battery/operations.csv:1408; data/sources/kit-battery/fixations.csv:1179

### sequence-027 · test · 记录顺序

按 NEXT 从 kit-v1:operation:6152 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:6153", "kit-v1:operation:6154"], "target_uids": ["kit-v1:fixation:6160", "kit-v1:fixation:6161"]}`

来源：data/sources/kit-battery/operations.csv:1409; data/sources/kit-battery/operations.csv:1410; data/sources/kit-battery/operations.csv:1411

### sequence-028 · test · 记录顺序

检查记录操作 kit-v1:operation:6203 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:6202", "previous_target": "kit-v1:fixation:6165"}`

来源：data/sources/kit-battery/operations.csv:1460; data/sources/kit-battery/operations.csv:1459

### sequence-029 · test · 记录顺序

从 kit-v1:operation:6153 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:6153", "kit-v1:operation:6154", "kit-v1:operation:6155", "kit-v1:operation:6156"], "skills": ["cut", "cut", "cut", "unplug"]}`

来源：data/sources/kit-battery/operations.csv:1410; data/sources/kit-battery/operations.csv:1411; data/sources/kit-battery/operations.csv:1412; data/sources/kit-battery/operations.csv:1413

### sequence-030 · test · 记录顺序

kit-v1:operation:6202 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:6165", "next_target": "kit-v1:fixation:6166"}`

来源：data/sources/kit-battery/operations.csv:1459; data/sources/kit-battery/operations.csv:1460

### sequence-031 · test · 记录顺序

完成记录操作 kit-v1:operation:7097 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:7098", "target_uid": "kit-v1:fixation:7087", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1548; data/sources/kit-battery/operations.csv:1549; data/sources/kit-battery/fixations.csv:1282

### sequence-032 · test · 记录顺序

按 NEXT 从 kit-v1:operation:7100 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:7120", "kit-v1:operation:7121"], "target_uids": ["kit-v1:fixation:7109", "kit-v1:fixation:7110"]}`

来源：data/sources/kit-battery/operations.csv:1551; data/sources/kit-battery/operations.csv:1568; data/sources/kit-battery/operations.csv:1569

### sequence-033 · test · 记录顺序

检查记录操作 kit-v1:operation:7154 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:7153", "previous_target": "kit-v1:fixation:7123"}`

来源：data/sources/kit-battery/operations.csv:1598; data/sources/kit-battery/operations.csv:1597

### sequence-034 · test · 记录顺序

从 kit-v1:operation:7153 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:7153", "kit-v1:operation:7154", "kit-v1:operation:7048", "kit-v1:operation:7095"], "skills": ["cut", "cut", "lift_off", "cut"]}`

来源：data/sources/kit-battery/operations.csv:1597; data/sources/kit-battery/operations.csv:1598; data/sources/kit-battery/operations.csv:1513; data/sources/kit-battery/operations.csv:1546

### sequence-035 · test · 记录顺序

kit-v1:operation:7154 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:7124", "next_target": "kit-v1:part:7004"}`

来源：data/sources/kit-battery/operations.csv:1598; data/sources/kit-battery/operations.csv:1513

### sequence-036 · test · 记录顺序

完成记录操作 kit-v1:operation:8324 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:8325", "target_uid": "kit-v1:fixation:8239", "target_class": "cable tie"}`

来源：data/sources/kit-battery/operations.csv:1906; data/sources/kit-battery/operations.csv:1907; data/sources/kit-battery/fixations.csv:1556

### sequence-037 · test · 记录顺序

按 NEXT 从 kit-v1:operation:8325 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:8326", "kit-v1:operation:8327"], "target_uids": ["kit-v1:fixation:8238", "kit-v1:fixation:8237"]}`

来源：data/sources/kit-battery/operations.csv:1907; data/sources/kit-battery/operations.csv:1908; data/sources/kit-battery/operations.csv:1909

### sequence-038 · test · 记录顺序

检查记录操作 kit-v1:operation:8328 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:8327", "previous_target": "kit-v1:fixation:8237"}`

来源：data/sources/kit-battery/operations.csv:1910; data/sources/kit-battery/operations.csv:1909

### sequence-039 · test · 记录顺序

从 kit-v1:operation:8223 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:8223", "kit-v1:operation:8224", "kit-v1:operation:8225", "kit-v1:operation:8145"], "skills": ["cut", "cut", "lift_off", "lift_off"]}`

来源：data/sources/kit-battery/operations.csv:1809; data/sources/kit-battery/operations.csv:1810; data/sources/kit-battery/operations.csv:1811; data/sources/kit-battery/operations.csv:1731

### sequence-040 · test · 记录顺序

kit-v1:operation:8332 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:8248", "next_target": "kit-v1:fixation:8249"}`

来源：data/sources/kit-battery/operations.csv:1914; data/sources/kit-battery/operations.csv:1915

### sequence-041 · test · 记录顺序

完成记录操作 kit-v1:operation:9040 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:9041", "target_uid": "kit-v1:fixation:9040", "target_class": "clip"}`

来源：data/sources/kit-battery/operations.csv:1967; data/sources/kit-battery/operations.csv:1968; data/sources/kit-battery/fixations.csv:1625

### sequence-042 · test · 记录顺序

按 NEXT 从 kit-v1:operation:9088 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:9089", "kit-v1:operation:9090"], "target_uids": ["kit-v1:part:9033", "kit-v1:part:9034"]}`

来源：data/sources/kit-battery/operations.csv:2015; data/sources/kit-battery/operations.csv:2016; data/sources/kit-battery/operations.csv:2017

### sequence-043 · test · 记录顺序

检查记录操作 kit-v1:operation:9176 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:9175", "previous_target": "kit-v1:part:9052"}`

来源：data/sources/kit-battery/operations.csv:2103; data/sources/kit-battery/operations.csv:2102

### sequence-044 · test · 记录顺序

从 kit-v1:operation:9127 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:9127", "kit-v1:operation:9128", "kit-v1:operation:9129", "kit-v1:operation:9130"], "skills": ["lift_off", "lift_off", "lift_off", "lift_off"]}`

来源：data/sources/kit-battery/operations.csv:2054; data/sources/kit-battery/operations.csv:2055; data/sources/kit-battery/operations.csv:2056; data/sources/kit-battery/operations.csv:2057

### sequence-045 · test · 记录顺序

kit-v1:operation:9175 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:part:9052", "next_target": "kit-v1:part:9053"}`

来源：data/sources/kit-battery/operations.csv:2102; data/sources/kit-battery/operations.csv:2103

### sequence-046 · test · 记录顺序

完成记录操作 kit-v1:operation:10060 后，NEXT 紧接的操作及对象是什么？返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。

答案：`{"next_operation": "kit-v1:operation:10061", "target_uid": "kit-v1:fixation:10063", "target_class": "plug"}`

来源：data/sources/kit-battery/operations.csv:2170; data/sources/kit-battery/operations.csv:2171; data/sources/kit-battery/fixations.csv:1784

### sequence-047 · test · 记录顺序

按 NEXT 从 kit-v1:operation:10123 向后追踪两步（不含当前操作），返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。

答案：`{"operation_uids": ["kit-v1:operation:10124", "kit-v1:operation:10125"], "target_uids": ["kit-v1:fixation:10128", "kit-v1:fixation:10129"]}`

来源：data/sources/kit-battery/operations.csv:2233; data/sources/kit-battery/operations.csv:2234; data/sources/kit-battery/operations.csv:2235

### sequence-048 · test · 记录顺序

检查记录操作 kit-v1:operation:10146 的紧邻前序记录，返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。

答案：`{"previous_operation": "kit-v1:operation:10145", "previous_target": "kit-v1:fixation:10149"}`

来源：data/sources/kit-battery/operations.csv:2256; data/sources/kit-battery/operations.csv:2255

### sequence-049 · test · 记录顺序

从 kit-v1:operation:10075 起沿 NEXT 取连续四条操作（含当前操作），返回 operation_uids 和 skills，两个列表均保持顺序且不去重。

答案：`{"operation_uids": ["kit-v1:operation:10075", "kit-v1:operation:10076", "kit-v1:operation:10077", "kit-v1:operation:10078"], "skills": ["unclip", "unclip", "unplug", "unclip"]}`

来源：data/sources/kit-battery/operations.csv:2185; data/sources/kit-battery/operations.csv:2186; data/sources/kit-battery/operations.csv:2187; data/sources/kit-battery/operations.csv:2188

### sequence-050 · test · 记录顺序

kit-v1:operation:10071 与其 NEXT 后继是否作用于同一个对象？返回 same_target（布尔值）、current_target 和 next_target（UID）。

答案：`{"same_target": false, "current_target": "kit-v1:fixation:10074", "next_target": "kit-v1:fixation:10073"}`

来源：data/sources/kit-battery/operations.csv:2181; data/sources/kit-battery/operations.csv:2182

## 指南证据定位

### guide-001 · dev · Begin - of - line testing：工艺约束核对

为“Begin - of - line testing”准备工艺约束核对。请定位 PEM 指南第 6 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p6:e118:0", "pem:p6:e119:0", "pem:p6:e120:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6

### guide-002 · dev · Begin - of - line testing：质量检查清单

为“Begin - of - line testing”准备质量检查清单。请定位 PEM 指南第 6 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p6:e122:0", "pem:p6:e123:0", "pem:p6:e124:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6

### guide-003 · dev · Begin - of - line testing：工序资料准备

为“Begin - of - line testing”准备工序资料准备。请定位 PEM 指南第 6 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p6:e111:0", "pem:p6:e112:0", "pem:p6:e113:0", "pem:p6:e114:0", "pem:p6:e115:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6; data/sources/pem-module-pack-guide.pdf:6

### guide-004 · dev · Stacking the cells：工艺约束核对

为“Stacking the cells”准备工艺约束核对。请定位 PEM 指南第 7 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p7:e147:0", "pem:p7:e148:0", "pem:p7:e149:0", "pem:p7:e150:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7

### guide-005 · dev · Stacking the cells：质量检查清单

为“Stacking the cells”准备质量检查清单。请定位 PEM 指南第 7 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p7:e152:0", "pem:p7:e153:0", "pem:p7:e154:0", "pem:p7:e155:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7

### guide-006 · dev · Stacking the cells：工序资料准备

为“Stacking the cells”准备工序资料准备。请定位 PEM 指南第 7 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p7:e139:0", "pem:p7:e140:0", "pem:p7:e141:0", "pem:p7:e142:0", "pem:p7:e143:0", "pem:p7:e144:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7; data/sources/pem-module-pack-guide.pdf:7

### guide-007 · test · Stacking the cells：工艺约束核对

为“Stacking the cells”准备工艺约束核对。请定位 PEM 指南第 8 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p8:e177:0", "pem:p8:e178:0", "pem:p8:e179:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8

### guide-008 · test · Stacking the cells：质量检查清单

为“Stacking the cells”准备质量检查清单。请定位 PEM 指南第 8 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p8:e181:0", "pem:p8:e182:0", "pem:p8:e183:0", "pem:p8:e184:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8

### guide-009 · test · Stacking the cells：工序资料准备

为“Stacking the cells”准备工序资料准备。请定位 PEM 指南第 8 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p8:e169:0", "pem:p8:e170:0", "pem:p8:e171:0", "pem:p8:e172:0", "pem:p8:e173:0", "pem:p8:e174:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8; data/sources/pem-module-pack-guide.pdf:8

### guide-010 · test · Stacking the cells：工艺约束核对

为“Stacking the cells”准备工艺约束核对。请定位 PEM 指南第 9 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p9:e205:0", "pem:p9:e206:0", "pem:p9:e207:0", "pem:p9:e208:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9

### guide-011 · test · Stacking the cells：质量检查清单

为“Stacking the cells”准备质量检查清单。请定位 PEM 指南第 9 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p9:e210:0", "pem:p9:e211:0", "pem:p9:e212:0", "pem:p9:e213:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9

### guide-012 · test · Stacking the cells：工序资料准备

为“Stacking the cells”准备工序资料准备。请定位 PEM 指南第 9 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p9:e197:0", "pem:p9:e198:0", "pem:p9:e199:0", "pem:p9:e200:0", "pem:p9:e201:0", "pem:p9:e202:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9; data/sources/pem-module-pack-guide.pdf:9

### guide-013 · test · Mounting the BMS：工艺约束核对

为“Mounting the BMS”准备工艺约束核对。请定位 PEM 指南第 10 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p10:e233:0", "pem:p10:e234:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10

### guide-014 · test · Mounting the BMS：质量检查清单

为“Mounting the BMS”准备质量检查清单。请定位 PEM 指南第 10 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p10:e236:0", "pem:p10:e237:0", "pem:p10:e238:0", "pem:p10:e239:0", "pem:p10:e240:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10

### guide-015 · test · Mounting the BMS：工序资料准备

为“Mounting the BMS”准备工序资料准备。请定位 PEM 指南第 10 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p10:e226:0", "pem:p10:e227:0", "pem:p10:e228:0", "pem:p10:e229:0", "pem:p10:e230:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10; data/sources/pem-module-pack-guide.pdf:10

### guide-016 · test · Contacting the tabs：工艺约束核对

为“Contacting the tabs”准备工艺约束核对。请定位 PEM 指南第 12 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p12:e281:0", "pem:p12:e282:0", "pem:p12:e283:0", "pem:p12:e284:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12

### guide-017 · test · Contacting the tabs：质量检查清单

为“Contacting the tabs”准备质量检查清单。请定位 PEM 指南第 12 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p12:e286:0", "pem:p12:e287:0", "pem:p12:e288:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12

### guide-018 · test · Contacting the tabs：工序资料准备

为“Contacting the tabs”准备工序资料准备。请定位 PEM 指南第 12 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p12:e274:0", "pem:p12:e275:0", "pem:p12:e276:0", "pem:p12:e277:0", "pem:p12:e278:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12; data/sources/pem-module-pack-guide.pdf:12

### guide-019 · test · Contacting the tabs：工艺约束核对

为“Contacting the tabs”准备工艺约束核对。请定位 PEM 指南第 13 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p13:e308:0", "pem:p13:e309:0", "pem:p13:e310:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13

### guide-020 · test · Contacting the tabs：质量检查清单

为“Contacting the tabs”准备质量检查清单。请定位 PEM 指南第 13 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p13:e312:0", "pem:p13:e313:0", "pem:p13:e314:0", "pem:p13:e315:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13

### guide-021 · test · Contacting the tabs：工序资料准备

为“Contacting the tabs”准备工序资料准备。请定位 PEM 指南第 13 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p13:e301:0", "pem:p13:e302:0", "pem:p13:e303:0", "pem:p13:e304:0", "pem:p13:e305:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13; data/sources/pem-module-pack-guide.pdf:13

### guide-022 · test · Tensioning of the cells：工艺约束核对

为“Tensioning of the cells”准备工艺约束核对。请定位 PEM 指南第 15 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p15:e363:0", "pem:p15:e364:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15

### guide-023 · test · Tensioning of the cells：质量检查清单

为“Tensioning of the cells”准备质量检查清单。请定位 PEM 指南第 15 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p15:e366:0", "pem:p15:e367:0", "pem:p15:e368:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15

### guide-024 · test · Tensioning of the cells：工序资料准备

为“Tensioning of the cells”准备工序资料准备。请定位 PEM 指南第 15 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p15:e357:0", "pem:p15:e358:0", "pem:p15:e359:0", "pem:p15:e360:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15; data/sources/pem-module-pack-guide.pdf:15

### guide-025 · test · Module final assembly：工艺约束核对

为“Module final assembly”准备工艺约束核对。请定位 PEM 指南第 17 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p17:e419:0", "pem:p17:e420:0", "pem:p17:e421:0", "pem:p17:e422:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17

### guide-026 · test · Module final assembly：质量检查清单

为“Module final assembly”准备质量检查清单。请定位 PEM 指南第 17 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p17:e424:0", "pem:p17:e425:0", "pem:p17:e426:0", "pem:p17:e427:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17

### guide-027 · test · Module final assembly：工序资料准备

为“Module final assembly”准备工序资料准备。请定位 PEM 指南第 17 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p17:e408:0", "pem:p17:e409:0", "pem:p17:e410:0", "pem:p17:e411:0", "pem:p17:e412:0", "pem:p17:e413:0", "pem:p17:e414:0", "pem:p17:e415:0", "pem:p17:e416:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17; data/sources/pem-module-pack-guide.pdf:17

### guide-028 · test · Mounting the modules：工艺约束核对

为“Mounting the modules”准备工艺约束核对。请定位 PEM 指南第 18 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p18:e447:0", "pem:p18:e448:0", "pem:p18:e449:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18

### guide-029 · test · Mounting the modules：质量检查清单

为“Mounting the modules”准备质量检查清单。请定位 PEM 指南第 18 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p18:e451:0", "pem:p18:e452:0", "pem:p18:e453:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18

### guide-030 · test · Mounting the modules：工序资料准备

为“Mounting the modules”准备工序资料准备。请定位 PEM 指南第 18 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p18:e440:0", "pem:p18:e441:0", "pem:p18:e442:0", "pem:p18:e443:0", "pem:p18:e444:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18; data/sources/pem-module-pack-guide.pdf:18

### guide-031 · test · Assembly of internal components：工艺约束核对

为“Assembly of internal components”准备工艺约束核对。请定位 PEM 指南第 20 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p20:e499:0", "pem:p20:e500:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20

### guide-032 · test · Assembly of internal components：质量检查清单

为“Assembly of internal components”准备质量检查清单。请定位 PEM 指南第 20 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p20:e502:0", "pem:p20:e503:0", "pem:p20:e504:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20

### guide-033 · test · Assembly of internal components：工序资料准备

为“Assembly of internal components”准备工序资料准备。请定位 PEM 指南第 20 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p20:e491:0", "pem:p20:e492:0", "pem:p20:e493:0", "pem:p20:e494:0", "pem:p20:e495:0", "pem:p20:e496:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20; data/sources/pem-module-pack-guide.pdf:20

### guide-034 · test · Sealing & Leak testing：工艺约束核对

为“Sealing & Leak testing”准备工艺约束核对。请定位 PEM 指南第 21 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p21:e525:0", "pem:p21:e526:0", "pem:p21:e527:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21

### guide-035 · test · Sealing & Leak testing：质量检查清单

为“Sealing & Leak testing”准备质量检查清单。请定位 PEM 指南第 21 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p21:e529:0", "pem:p21:e530:0", "pem:p21:e531:0", "pem:p21:e532:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21

### guide-036 · test · Sealing & Leak testing：工序资料准备

为“Sealing & Leak testing”准备工序资料准备。请定位 PEM 指南第 21 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p21:e518:0", "pem:p21:e519:0", "pem:p21:e520:0", "pem:p21:e521:0", "pem:p21:e522:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21; data/sources/pem-module-pack-guide.pdf:21

### guide-037 · test · Charging & Flashing：工艺约束核对

为“Charging & Flashing”准备工艺约束核对。请定位 PEM 指南第 22 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p22:e551:0", "pem:p22:e552:0", "pem:p22:e553:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22

### guide-038 · test · Charging & Flashing：质量检查清单

为“Charging & Flashing”准备质量检查清单。请定位 PEM 指南第 22 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p22:e555:0", "pem:p22:e556:0", "pem:p22:e557:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22

### guide-039 · test · Charging & Flashing：工序资料准备

为“Charging & Flashing”准备工序资料准备。请定位 PEM 指南第 22 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p22:e545:0", "pem:p22:e546:0", "pem:p22:e547:0", "pem:p22:e548:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22; data/sources/pem-module-pack-guide.pdf:22

### guide-040 · test · End - of - line testing：工艺约束核对

为“End - of - line testing”准备工艺约束核对。请定位 PEM 指南第 23 页“左栏 Process parameters & requirements”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p23:e576:0", "pem:p23:e577:0", "pem:p23:e578:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23

### guide-041 · test · End - of - line testing：质量检查清单

为“End - of - line testing”准备质量检查清单。请定位 PEM 指南第 23 页“右栏 Quality parameters”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p23:e580:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:23

### guide-042 · test · End - of - line testing：工序资料准备

为“End - of - line testing”准备工序资料准备。请定位 PEM 指南第 23 页“Production process”栏的全部项目符号条目，不包含标题、成本和图片说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p23:e568:0", "pem:p23:e569:0", "pem:p23:e570:0", "pem:p23:e571:0", "pem:p23:e572:0", "pem:p23:e573:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23; data/sources/pem-module-pack-guide.pdf:23

### guide-043 · dev · 连接工艺选型依据

为连接工艺选型准备依据，定位 PEM 指南第 14 页关于激光焊接的占地、颗粒控制和反射表面限制的全部对应条目。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p14:e333:0", "pem:p14:e334:0", "pem:p14:e335:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14

### guide-044 · dev · 连接工艺选型依据

为连接工艺选型准备依据，定位 PEM 指南第 14 页关于超声焊接的接触形式、连接性能及设备可达性限制的全部对应条目。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p14:e338:0", "pem:p14:e339:0", "pem:p14:e340:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14

### guide-045 · dev · 连接工艺选型依据

为连接工艺选型准备依据，定位 PEM 指南第 14 页关于电阻焊接的电压施加、发热机制、自动化收益及材料限制的全部对应条目。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p14:e342:0", "pem:p14:e343:0", "pem:p14:e344:0", "pem:p14:e345:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14

### guide-046 · dev · 连接工艺选型依据

为连接工艺选型准备依据，定位 PEM 指南第 14 页关于线键合的连接方式、成形作用、熔断保护、错位补偿及强度限制的全部对应条目。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p14:e347:0", "pem:p14:e348:0", "pem:p14:e349:0", "pem:p14:e350:0", "pem:p14:e351:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14; data/sources/pem-module-pack-guide.pdf:14

### guide-047 · test · 设计约束来源核对

整理设计约束来源：定位 PEM 指南第 16 页“Mechanical load and fixation of the cells”栏全部正文条目，不包括下方示意图标签。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p16:e378:0", "pem:p16:e379:0", "pem:p16:e380:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:16; data/sources/pem-module-pack-guide.pdf:16; data/sources/pem-module-pack-guide.pdf:16

### guide-048 · test · 设计约束来源核对

整理设计约束来源：定位 PEM 指南第 16 页“Thermal load and fire protection”栏全部正文条目，不包括下方示意图标签。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p16:e382:0", "pem:p16:e383:0", "pem:p16:e384:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:16; data/sources/pem-module-pack-guide.pdf:16; data/sources/pem-module-pack-guide.pdf:16

### guide-049 · test · 设计约束来源核对

整理设计约束来源：定位 PEM 指南第 16 页“Insulation and electromagnetic compatibility”栏全部正文条目，不包括下方示意图标签。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p16:e386:0", "pem:p16:e387:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:16; data/sources/pem-module-pack-guide.pdf:16

### guide-050 · test · 冷却方案比较依据

比较底板冷却与浸没冷却，定位 PEM 指南第 19 页描述两者传热介质/位置、冷却性能以及浸没方案密封和维护要求的条目，不包括底板单件安装说明。 返回 evidence_uids（覆盖所求全部条目的 UID 列表），在 claims 中说明条目内容。

答案：`{"evidence_uids": ["pem:p19:e465:0", "pem:p19:e467:0", "pem:p19:e483:0", "pem:p19:e484:0", "pem:p19:e485:0"]}`

来源：data/sources/pem-module-pack-guide.pdf:19; data/sources/pem-module-pack-guide.pdf:19; data/sources/pem-module-pack-guide.pdf:19; data/sources/pem-module-pack-guide.pdf:19; data/sources/pem-module-pack-guide.pdf:19

## 资料边界

### scope-001 · dev · 资料边界

仅根据 kit-v1:fixation:1079 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:81

### scope-002 · dev · 资料边界

Fiat 500e 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2016}`

来源：data/sources/kit-battery/battery_catalogue.csv:2

### scope-003 · dev · 资料边界

当前产品是Fiat 500e。查找连接件原始编号 2007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:2; data/sources/kit-battery/fixations.csv:3; data/sources/kit-battery/fixations.csv:4; data/sources/kit-battery/fixations.csv:5; data/sources/kit-battery/fixations.csv:6; data/sources/kit-battery/fixations.csv:7

### scope-004 · dev · 资料边界

查阅 kit-v1:operation:1370 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:372

### scope-005 · dev · 资料边界

仅核对 kit-v1:part:1034 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:36

### scope-006 · dev · 资料边界

仅根据 kit-v1:fixation:2157 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:417

### scope-007 · dev · 资料边界

Chevrolet Spark 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": false, "year": null}`

来源：data/sources/kit-battery/battery_catalogue.csv:3

### scope-008 · dev · 资料边界

当前产品是Chevrolet Spark。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:285; data/sources/kit-battery/fixations.csv:286; data/sources/kit-battery/fixations.csv:287; data/sources/kit-battery/fixations.csv:288; data/sources/kit-battery/fixations.csv:289; data/sources/kit-battery/fixations.csv:290

### scope-009 · dev · 资料边界

查阅 kit-v1:operation:2176 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:538

### scope-010 · dev · 资料边界

仅核对 kit-v1:part:2016 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:116

### scope-011 · test · 资料边界

仅根据 kit-v1:fixation:3296 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:716

### scope-012 · test · 资料边界

Hyundai IONIQ 5 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2022}`

来源：data/sources/kit-battery/battery_catalogue.csv:4

### scope-013 · test · 资料边界

当前产品是Hyundai IONIQ 5。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:430; data/sources/kit-battery/fixations.csv:431; data/sources/kit-battery/fixations.csv:432; data/sources/kit-battery/fixations.csv:433; data/sources/kit-battery/fixations.csv:434; data/sources/kit-battery/fixations.csv:435

### scope-014 · test · 资料边界

查阅 kit-v1:operation:3128 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:617

### scope-015 · test · 资料边界

仅核对 kit-v1:part:3007 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:141

### scope-016 · test · 资料边界

仅根据 kit-v1:fixation:4128 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:872

### scope-017 · test · 资料边界

BMW 530e 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": false, "year": null}`

来源：data/sources/kit-battery/battery_catalogue.csv:5

### scope-018 · test · 资料边界

当前产品是BMW 530e。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:750; data/sources/kit-battery/fixations.csv:751; data/sources/kit-battery/fixations.csv:752; data/sources/kit-battery/fixations.csv:753; data/sources/kit-battery/fixations.csv:754; data/sources/kit-battery/fixations.csv:755

### scope-019 · test · 资料边界

查阅 kit-v1:operation:4158 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1084

### scope-020 · test · 资料边界

仅核对 kit-v1:part:4014 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:264

### scope-021 · test · 资料边界

仅根据 kit-v1:fixation:5092 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:977

### scope-022 · test · 资料边界

Chevrolet Volt 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": false, "year": null}`

来源：data/sources/kit-battery/battery_catalogue.csv:6

### scope-023 · test · 资料边界

当前产品是Chevrolet Volt。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:885; data/sources/kit-battery/fixations.csv:886; data/sources/kit-battery/fixations.csv:887; data/sources/kit-battery/fixations.csv:888; data/sources/kit-battery/fixations.csv:889; data/sources/kit-battery/fixations.csv:890

### scope-024 · test · 资料边界

查阅 kit-v1:operation:5080 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1170

### scope-025 · test · 资料边界

仅核对 kit-v1:part:5004 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:282

### scope-026 · test · 资料边界

仅根据 kit-v1:fixation:6033 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:1054

### scope-027 · test · 资料边界

Volvo EX30 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2024}`

来源：data/sources/kit-battery/battery_catalogue.csv:7

### scope-028 · test · 资料边界

当前产品是Volvo EX30。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:1022; data/sources/kit-battery/fixations.csv:1023; data/sources/kit-battery/fixations.csv:1024; data/sources/kit-battery/fixations.csv:1025; data/sources/kit-battery/fixations.csv:1026; data/sources/kit-battery/fixations.csv:1027

### scope-029 · test · 资料边界

查阅 kit-v1:operation:6150 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1407

### scope-030 · test · 资料边界

仅核对 kit-v1:part:6019 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:333

### scope-031 · test · 资料边界

仅根据 kit-v1:fixation:7134 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:1322

### scope-032 · test · 资料边界

BMW 330e 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2016}`

来源：data/sources/kit-battery/battery_catalogue.csv:8

### scope-033 · test · 资料边界

当前产品是BMW 330e。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:1208; data/sources/kit-battery/fixations.csv:1209; data/sources/kit-battery/fixations.csv:1210; data/sources/kit-battery/fixations.csv:1211; data/sources/kit-battery/fixations.csv:1212; data/sources/kit-battery/fixations.csv:1213

### scope-034 · test · 资料边界

查阅 kit-v1:operation:7097 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1548

### scope-035 · test · 资料边界

仅核对 kit-v1:part:7020 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:376

### scope-036 · test · 资料边界

仅根据 kit-v1:fixation:8260 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:1577

### scope-037 · test · 资料边界

MG ZS 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2019}`

来源：data/sources/kit-battery/battery_catalogue.csv:9

### scope-038 · test · 资料边界

当前产品是MG ZS。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:1329; data/sources/kit-battery/fixations.csv:1330; data/sources/kit-battery/fixations.csv:1331; data/sources/kit-battery/fixations.csv:1332; data/sources/kit-battery/fixations.csv:1333; data/sources/kit-battery/fixations.csv:1334

### scope-039 · test · 资料边界

查阅 kit-v1:operation:8324 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1906

### scope-040 · test · 资料边界

仅核对 kit-v1:part:8005 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:385

### scope-041 · test · 资料边界

仅根据 kit-v1:fixation:9044 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:1629

### scope-042 · test · 资料边界

Mitsubishi Outlander 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2018}`

来源：data/sources/kit-battery/battery_catalogue.csv:10

### scope-043 · test · 资料边界

当前产品是Mitsubishi Outlander。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:1585; data/sources/kit-battery/fixations.csv:1586; data/sources/kit-battery/fixations.csv:1587; data/sources/kit-battery/fixations.csv:1588; data/sources/kit-battery/fixations.csv:1589; data/sources/kit-battery/fixations.csv:1590

### scope-044 · test · 资料边界

查阅 kit-v1:operation:9040 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:1967

### scope-045 · test · 资料边界

仅核对 kit-v1:part:9013 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:490

### scope-046 · test · 资料边界

仅根据 kit-v1:fixation:10082 的原始 CSV 行，该行是否给出了拧紧扭矩？返回 documented（布尔值）和 torque_nm（没有就为 null）。

答案：`{"documented": false, "torque_nm": null}`

来源：data/sources/kit-battery/fixations.csv:1803

### scope-047 · test · 资料边界

BMW i3 的电池目录是否记录年份？返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。

答案：`{"documented": true, "year": 2014}`

来源：data/sources/kit-battery/battery_catalogue.csv:11

### scope-048 · test · 资料边界

当前产品是BMW i3。查找连接件原始编号 1007，不要切换产品。返回 found_in_current_product（布尔值）。

答案：`{"found_in_current_product": false}`

来源：data/sources/kit-battery/fixations.csv:1721; data/sources/kit-battery/fixations.csv:1722; data/sources/kit-battery/fixations.csv:1723; data/sources/kit-battery/fixations.csv:1724; data/sources/kit-battery/fixations.csv:1725; data/sources/kit-battery/fixations.csv:1726

### scope-049 · test · 资料边界

查阅 kit-v1:operation:10060 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？返回 can_infer_assembly（布尔值）和 source_scope（recorded_disassembly 或 manufacturing_plan）。

答案：`{"can_infer_assembly": false, "source_scope": "recorded_disassembly"}`

来源：data/sources/kit-battery/operations.csv:2170

### scope-050 · test · 资料边界

仅核对 kit-v1:part:10028 的原始 part_no 字段是否有值。返回 documented 和 part_no；空字段用 null，非空保留原始字符串。

答案：`{"documented": false, "part_no": null}`

来源：data/sources/kit-battery/parts.csv:561

## 变更流程

### workflow-001 · dev · 正常核对

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:37; data/sources/kit-battery/parts.csv:2; data/sources/kit-battery/parts.csv:3

### workflow-002 · test · 正常核对

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:450; data/sources/kit-battery/parts.csv:134; data/sources/kit-battery/parts.csv:136

### workflow-003 · test · 正常核对

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:903; data/sources/kit-battery/parts.csv:279; data/sources/kit-battery/parts.csv:280

### workflow-004 · test · 正常核对

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1228; data/sources/kit-battery/parts.csv:356; data/sources/kit-battery/parts.csv:357

### workflow-005 · test · 正常核对

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1602; data/sources/kit-battery/parts.csv:477; data/sources/kit-battery/parts.csv:478

### workflow-006 · dev · 补充工具卡

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "pass", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:330; data/sources/kit-battery/parts.csv:102; data/sources/kit-battery/parts.csv:104

### workflow-007 · test · 补充工具卡

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "pass", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:800; data/sources/kit-battery/parts.csv:253; data/sources/kit-battery/parts.csv:252

### workflow-008 · test · 补充工具卡

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "pass", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1022; data/sources/kit-battery/parts.csv:316; data/sources/kit-battery/parts.csv:333

### workflow-009 · test · 补充工具卡

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "pass", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1350; data/sources/kit-battery/parts.csv:381; data/sources/kit-battery/parts.csv:385

### workflow-010 · test · 补充工具卡

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "pass", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1864; data/sources/kit-battery/parts.csv:536; data/sources/kit-battery/parts.csv:534

### workflow-011 · dev · 补充指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:74; data/sources/kit-battery/parts.csv:33; data/sources/kit-battery/parts.csv:3

### workflow-012 · test · 补充指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:970; data/sources/kit-battery/parts.csv:300; data/sources/kit-battery/parts.csv:282

### workflow-013 · test · 补充指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1262; data/sources/kit-battery/parts.csv:368; data/sources/kit-battery/parts.csv:357

### workflow-014 · test · 补充指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1620; data/sources/kit-battery/parts.csv:481; data/sources/kit-battery/parts.csv:480

### workflow-015 · test · 补充指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:636; data/sources/kit-battery/parts.csv:220; data/sources/kit-battery/parts.csv:136

### workflow-016 · dev · 纠正工具冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:384; data/sources/kit-battery/parts.csv:126; data/sources/kit-battery/parts.csv:103

### workflow-017 · test · 纠正工具冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1024; data/sources/kit-battery/parts.csv:317; data/sources/kit-battery/parts.csv:333

### workflow-018 · test · 纠正工具冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1419; data/sources/kit-battery/parts.csv:385; data/sources/kit-battery/parts.csv:384

### workflow-019 · test · 纠正工具冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1872; data/sources/kit-battery/parts.csv:538; data/sources/kit-battery/parts.csv:534

### workflow-020 · test · 纠正工具冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:802; data/sources/kit-battery/parts.csv:253; data/sources/kit-battery/parts.csv:273

### workflow-021 · dev · 更新指导书规格

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:38; data/sources/kit-battery/parts.csv:2; data/sources/kit-battery/parts.csv:3

### workflow-022 · test · 更新指导书规格

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1308; data/sources/kit-battery/parts.csv:370; data/sources/kit-battery/parts.csv:357

### workflow-023 · test · 更新指导书规格

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1622; data/sources/kit-battery/parts.csv:482; data/sources/kit-battery/parts.csv:480

### workflow-024 · test · 更新指导书规格

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:641; data/sources/kit-battery/parts.csv:222; data/sources/kit-battery/parts.csv:136

### workflow-025 · test · 更新指导书规格

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:972; data/sources/kit-battery/parts.csv:301; data/sources/kit-battery/parts.csv:282

### workflow-026 · dev · 部分补齐资料

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:392; data/sources/kit-battery/parts.csv:128; data/sources/kit-battery/parts.csv:103

### workflow-027 · test · 部分补齐资料

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1486; data/sources/kit-battery/parts.csv:392; data/sources/kit-battery/parts.csv:384

### workflow-028 · test · 部分补齐资料

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1880; data/sources/kit-battery/parts.csv:540; data/sources/kit-battery/parts.csv:534

### workflow-029 · test · 部分补齐资料

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:815; data/sources/kit-battery/parts.csv:267; data/sources/kit-battery/parts.csv:277

### workflow-030 · test · 部分补齐资料

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "missing", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1026; data/sources/kit-battery/parts.csv:318; data/sources/kit-battery/parts.csv:333

### workflow-031 · dev · 部分解决冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:73; data/sources/kit-battery/parts.csv:33; data/sources/kit-battery/parts.csv:3

### workflow-032 · test · 部分解决冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1680; data/sources/kit-battery/parts.csv:484; data/sources/kit-battery/parts.csv:478

### workflow-033 · test · 部分解决冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:649; data/sources/kit-battery/parts.csv:225; data/sources/kit-battery/parts.csv:136

### workflow-034 · test · 部分解决冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:974; data/sources/kit-battery/parts.csv:302; data/sources/kit-battery/parts.csv:288

### workflow-035 · test · 部分解决冲突

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1328; data/sources/kit-battery/parts.csv:373; data/sources/kit-battery/parts.csv:372

### workflow-036 · dev · 变更目标再修订

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M10"}]`

来源：data/sources/kit-battery/fixations.csv:400; data/sources/kit-battery/parts.csv:130; data/sources/kit-battery/parts.csv:103

### workflow-037 · test · 变更目标再修订

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M10"}]`

来源：data/sources/kit-battery/fixations.csv:1888; data/sources/kit-battery/parts.csv:542; data/sources/kit-battery/parts.csv:534

### workflow-038 · test · 变更目标再修订

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M10"}]`

来源：data/sources/kit-battery/fixations.csv:862; data/sources/kit-battery/parts.csv:269; data/sources/kit-battery/parts.csv:252

### workflow-039 · test · 变更目标再修订

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M10"}]`

来源：data/sources/kit-battery/fixations.csv:1028; data/sources/kit-battery/parts.csv:319; data/sources/kit-battery/parts.csv:333

### workflow-040 · test · 变更目标再修订

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "conflict", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M10"}]`

来源：data/sources/kit-battery/fixations.csv:1494; data/sources/kit-battery/parts.csv:395; data/sources/kit-battery/parts.csv:384

### workflow-041 · dev · 撤回指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:36; data/sources/kit-battery/parts.csv:2; data/sources/kit-battery/parts.csv:3

### workflow-042 · test · 撤回指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:656; data/sources/kit-battery/parts.csv:228; data/sources/kit-battery/parts.csv:136

### workflow-043 · test · 撤回指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:976; data/sources/kit-battery/parts.csv:303; data/sources/kit-battery/parts.csv:288

### workflow-044 · test · 撤回指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1275; data/sources/kit-battery/parts.csv:375; data/sources/kit-battery/parts.csv:357

### workflow-045 · test · 撤回指导书

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "pass", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": true, "new_spec": "M8"}, {"tool_status": "pass", "instruction_status": "missing", "case_status": "awaiting_information", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1634; data/sources/kit-battery/parts.csv:488; data/sources/kit-battery/parts.csv:489

### workflow-046 · dev · 修订未解决问题

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:408; data/sources/kit-battery/parts.csv:132; data/sources/kit-battery/parts.csv:103

### workflow-047 · test · 修订未解决问题

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:870; data/sources/kit-battery/parts.csv:271; data/sources/kit-battery/parts.csv:252

### workflow-048 · test · 修订未解决问题

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1031; data/sources/kit-battery/parts.csv:320; data/sources/kit-battery/parts.csv:353

### workflow-049 · test · 修订未解决问题

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1502; data/sources/kit-battery/parts.csv:397; data/sources/kit-battery/parts.csv:384

### workflow-050 · test · 修订未解决问题

按当前变更资料评估工具卡、指导书及资料状态。返回 tool_status 和 instruction_status（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、ready_for_human_review_completion（全部规则通过且可在人工复核后完成，布尔值）和 new_spec。

答案：`[{"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}, {"tool_status": "conflict", "instruction_status": "pass", "case_status": "awaiting_review", "ready_for_human_review_completion": false, "new_spec": "M8"}]`

来源：data/sources/kit-battery/fixations.csv:1818; data/sources/kit-battery/parts.csv:555; data/sources/kit-battery/parts.csv:536
