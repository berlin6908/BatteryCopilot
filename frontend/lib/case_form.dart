import 'package:flutter/material.dart';

import 'widgets.dart';

class CaseForm extends StatefulWidget {
  final Map input;
  final bool creating;
  const CaseForm({super.key, required this.input, required this.creating});
  @override
  State<CaseForm> createState() => _CaseFormState();
}

class _CaseFormState extends State<CaseForm> {
  final form = GlobalKey<FormState>();
  late final Map<String, TextEditingController> fields;
  late bool hasTool, hasInstruction;
  @override
  void initState() {
    super.initState();
    final input = widget.input;
    hasTool = input['tool_card'] != null;
    hasInstruction = input['instruction'] != null;
    fields = {
      for (final key in [
        'title',
        'target_uid',
        'reason',
        'old_spec',
        'new_spec',
      ])
        key: TextEditingController(text: input[key]),
      'tool_id': TextEditingController(
        text: input['tool_card']?['id'] ?? 'TOOL-01',
      ),
      'tool_revision': TextEditingController(
        text: input['tool_card']?['revision'] ?? 'B',
      ),
      'specs': TextEditingController(
        text:
            (input['tool_card']?['supported_specs'] as List?)?.join(', ') ??
            'M6, M8',
      ),
      'instruction_id': TextEditingController(
        text: input['instruction']?['id'] ?? 'WI-01',
      ),
      'instruction_revision': TextEditingController(
        text: input['instruction']?['revision'] ?? 'B',
      ),
      'instruction_spec': TextEditingController(
        text: input['instruction']?['spec'] ?? 'M8',
      ),
    };
  }

  @override
  void dispose() {
    for (final controller in fields.values) {
      controller.dispose();
    }
    super.dispose();
  }

  String value(String key) => fields[key]!.text.trim();
  Widget field(String key, String label, {int lines = 1}) => Padding(
    padding: const EdgeInsets.only(bottom: 14),
    child: TextFormField(
      controller: fields[key],
      decoration: InputDecoration(labelText: label),
      maxLines: lines,
      validator: (text) =>
          text == null || text.trim().isEmpty ? '请填写$label' : null,
    ),
  );

  void preset(int index) => setState(() {
    hasTool = index != 1;
    hasInstruction = true;
    fields['title']!.text = ['正常变更示例', '缺少资料示例', '规格冲突示例'][index];
    fields['old_spec']!.text = 'M6';
    fields['new_spec']!.text = 'M8';
    fields['specs']!.text = index == 2 ? 'M6' : 'M6, M8';
    fields['tool_revision']!.text = index == 2 ? 'A' : 'B';
    fields['instruction_spec']!.text = 'M8';
  });

  void save() {
    if (!form.currentState!.validate()) return;
    Navigator.pop(context, {
      'battery_id': widget.input['battery_id'],
      for (final key in [
        'title',
        'target_uid',
        'reason',
        'old_spec',
        'new_spec',
      ])
        key: value(key),
      'tool_card': hasTool
          ? {
              'id': value('tool_id'),
              'revision': value('tool_revision'),
              'supported_specs': value('specs')
                  .split(RegExp(r'[,，]'))
                  .map((s) => s.trim())
                  .where((s) => s.isNotEmpty)
                  .toList(),
            }
          : null,
      'instruction': hasInstruction
          ? {
              'id': value('instruction_id'),
              'revision': value('instruction_revision'),
              'spec': value('instruction_spec'),
            }
          : null,
    });
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: Text(widget.creating ? '新建变更申请' : '补充或修改资料'),
    content: SizedBox(
      width: 620,
      child: SingleChildScrollView(
        child: Form(
          key: form,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (widget.creating) ...[
                const Text(
                  '从模拟示例开始，也可以直接编辑资料。',
                  style: TextStyle(color: muted),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    for (int i = 0; i < 3; i++)
                      OutlinedButton(
                        onPressed: () => preset(i),
                        child: Text(['正常示例', '缺资料示例', '冲突示例'][i]),
                      ),
                  ],
                ),
                const SizedBox(height: 20),
              ],
              field('title', '申请标题'),
              field('target_uid', '连接件标识'),
              field('reason', '变更原因', lines: 2),
              Row(
                children: [
                  Expanded(child: field('old_spec', '原规格')),
                  const SizedBox(width: 12),
                  Expanded(child: field('new_spec', '新规格')),
                ],
              ),
              SwitchListTile.adaptive(
                contentPadding: EdgeInsets.zero,
                title: const Text('已提供工具卡'),
                value: hasTool,
                onChanged: (v) => setState(() => hasTool = v),
              ),
              if (hasTool) ...[
                field('tool_id', '工具卡编号'),
                field('tool_revision', '工具卡版次'),
                field('specs', '支持规格（逗号分隔）'),
              ],
              SwitchListTile.adaptive(
                contentPadding: EdgeInsets.zero,
                title: const Text('已提供作业指导书'),
                value: hasInstruction,
                onChanged: (v) => setState(() => hasInstruction = v),
              ),
              if (hasInstruction) ...[
                field('instruction_id', '指导书编号'),
                field('instruction_revision', '指导书版次'),
                field('instruction_spec', '指导书引用规格'),
              ],
              if (!widget.creating)
                const Text(
                  '保存后需要重新分析和复核；之前的报告仍可查看。',
                  style: TextStyle(color: muted),
                ),
            ],
          ),
        ),
      ),
    ),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: const Text('取消'),
      ),
      FilledButton(onPressed: save, child: const Text('保存申请')),
    ],
  );
}
