import 'package:flutter/material.dart';

import 'api.dart';
import 'widgets.dart';

class Copilot extends StatefulWidget {
  final int battery;
  final String scenario;
  final bool ready;
  const Copilot({
    super.key,
    required this.battery,
    required this.scenario,
    required this.ready,
  });
  @override
  State<Copilot> createState() => _CopilotState();
}

class _CopilotState extends State<Copilot> {
  final input = TextEditingController();
  final events = <Map<String, dynamic>>[];
  bool busy = false;
  String? question;
  @override
  void dispose() {
    input.dispose();
    super.dispose();
  }

  Future<void> send() async {
    if (input.text.trim().isEmpty || busy) return;
    setState(() {
      question = input.text.trim();
      events.clear();
      busy = true;
    });
    input.clear();
    try {
      await for (final event in api.ask(
        question!,
        widget.battery,
        widget.scenario,
      )) {
        if (!mounted) return;
        setState(() => events.add(event));
      }
    } catch (e) {
      if (mounted) {
        setState(() => events.add({'type': 'error', 'message': '$e'}));
      }
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => Container(
    width: 330,
    color: Colors.white,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Padding(
          padding: EdgeInsets.all(22),
          child: Row(
            children: [
              Icon(Icons.auto_awesome_outlined, color: teal),
              SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '工程助手',
                    style: TextStyle(fontWeight: FontWeight.w700, fontSize: 17),
                  ),
                  Text(
                    'Agent · 基于证据回答',
                    style: TextStyle(color: muted, fontSize: 11),
                  ),
                ],
              ),
            ],
          ),
        ),
        const Divider(height: 1),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              if (question == null) ...[
                const SizedBox(height: 12),
                const Text(
                  '从一个工程问题开始',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 10),
                const Text(
                  '查询对象、追踪关系、检索工艺资料。每条结论都可以回到原始证据。',
                  style: TextStyle(color: muted, height: 1.7, fontSize: 13),
                ),
                const SizedBox(height: 24),
                for (final example in [
                  '当前电池包有哪些连接方式？',
                  '螺钉 1000 连接哪些部件，如何拆除？',
                  '模组安装有哪些通用质量要求？',
                  '分析当前模拟变更的工具适配问题',
                ])
                  Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: OutlinedButton(
                      onPressed: () => input.text = example,
                      style: OutlinedButton.styleFrom(
                        alignment: Alignment.centerLeft,
                        padding: const EdgeInsets.all(14),
                      ),
                      child: Text(
                        example,
                        style: const TextStyle(fontSize: 12, color: ink),
                      ),
                    ),
                  ),
              ],
              if (!widget.ready)
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 20),
                  child: Panel(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Tag('等待连接模型', color: Color(0xFF9B742D)),
                        SizedBox(height: 10),
                        Text(
                          '连接模型并重启后端后，即可运行工具调用与证据问答。配置方式见项目说明。',
                          style: TextStyle(fontSize: 12, height: 1.6),
                        ),
                      ],
                    ),
                  ),
                ),
              if (question != null) ...[
                Tag(widget.scenario),
                const SizedBox(height: 14),
                Text(
                  question!,
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                    height: 1.6,
                  ),
                ),
                const SizedBox(height: 20),
              ],
              for (final event in events)
                if (event['type'] == 'tool')
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(
                      children: [
                        Icon(
                          event['status'] == 'completed'
                              ? Icons.check_circle_outline
                              : Icons.play_circle_outline,
                          size: 16,
                          color: teal,
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            event['name'],
                            style: const TextStyle(fontSize: 12, color: muted),
                          ),
                        ),
                      ],
                    ),
                  )
                else if (event['type'] == 'validation')
                  const Text('正在补查引用证据…', style: TextStyle(color: muted))
                else if (event['type'] == 'answer') ...[
                  const Divider(height: 30),
                  SelectableText(
                    event['summary'],
                    style: const TextStyle(
                      height: 1.7,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  for (final claim in event['claims'])
                    Padding(
                      padding: const EdgeInsets.only(top: 16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SelectableText(
                            claim['statement'],
                            style: const TextStyle(fontSize: 13, height: 1.7),
                          ),
                          Wrap(
                            spacing: 4,
                            children: [
                              for (final id in claim['evidence_ids'])
                                ActionChip(
                                  label: Text(
                                    id,
                                    style: const TextStyle(fontSize: 10),
                                  ),
                                  onPressed: () =>
                                      showEvidence(context, id, widget.battery),
                                ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  if ((event['unknowns'] as List).isNotEmpty) ...[
                    const SizedBox(height: 20),
                    const Text(
                      '资料缺口',
                      style: TextStyle(fontWeight: FontWeight.w600),
                    ),
                    for (final gap in event['unknowns'])
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Text(
                          '• $gap',
                          style: const TextStyle(fontSize: 12, height: 1.6),
                        ),
                      ),
                  ],
                  const SizedBox(height: 16),
                  Text(
                    '${event['seconds']} s · ${event['usage']['input_tokens']} 输入 tokens',
                    style: const TextStyle(color: muted, fontSize: 10),
                  ),
                ] else if (event['type'] == 'error')
                  Text(
                    event['message'],
                    style: const TextStyle(
                      color: Colors.deepOrange,
                      height: 1.6,
                    ),
                  ),
            ],
          ),
        ),
        if (busy) const LinearProgressIndicator(minHeight: 2),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              TextField(
                controller: input,
                minLines: 2,
                maxLines: 4,
                enabled: !busy,
                decoration: const InputDecoration(
                  hintText: '输入工程问题…',
                  hintStyle: TextStyle(fontSize: 13),
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  const Expanded(
                    child: Text(
                      '产品与场景已绑定',
                      style: TextStyle(fontSize: 10, color: muted),
                    ),
                  ),
                  FilledButton.icon(
                    onPressed: widget.ready && !busy ? send : null,
                    icon: const Icon(Icons.arrow_upward, size: 15),
                    label: const Text('运行'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    ),
  );
}
