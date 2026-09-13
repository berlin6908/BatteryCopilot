import 'package:flutter/material.dart';
import 'package:web/web.dart' as web;

import 'api.dart';
import 'widgets.dart';

class ManufacturingPage extends StatefulWidget {
  final bool modelReady;
  const ManufacturingPage({super.key, required this.modelReady});
  @override
  State<ManufacturingPage> createState() => _ManufacturingPageState();
}

class _ManufacturingPageState extends State<ManufacturingPage> {
  List cells = [], savedReports = [];
  Map? dataset, trace, test, report;
  Map<String, Map> processes = {};
  String? cellUid, testUid, error;
  String progress = '', decision = 'needs_information';
  bool loading = true, running = false;
  final question = TextEditingController(
    text:
        '生成这颗电芯的制造履历与检验复核报告：核对明确前驱、相关工序及已填写参数，'
        '读取循环统计前几行的充放电容量，指出追溯断点与作质量判断还缺少的资料。',
  );
  final reviewer = TextEditingController(), note = TextEditingController();

  @override
  void initState() {
    super.initState();
    load();
  }

  @override
  void dispose() {
    question.dispose();
    reviewer.dispose();
    note.dispose();
    super.dispose();
  }

  Future<void> load() async {
    try {
      final data = await api.get('manufacturing/cells');
      if (!mounted) return;
      setState(() {
        cells = data['cells'];
        dataset = data['dataset'];
        loading = false;
      });
      if (cells.isNotEmpty) await selectCell(cells.first['cell']['uid']);
    } catch (e) {
      if (mounted) {
        setState(() {
          error = '$e';
          loading = false;
        });
      }
    }
  }

  Future<void> selectCell(String uid) async {
    setState(() {
      cellUid = uid;
      loading = true;
      error = null;
      report = null;
      trace = null;
      test = null;
      processes = {};
      progress = '';
      reviewer.clear();
      note.clear();
    });
    try {
      final data =
          await api.get('manufacturing/trace', {'cell_uid': uid}) as Map;
      final ids = <String>{
        for (final stage in data['stages'])
          if (stage['process'] != null) stage['process']['uid'],
      };
      final results = await Future.wait([
        for (final id in ids)
          api.get('manufacturing/process', {
            'cell_uid': uid,
            'process_uid': id,
          }),
      ]);
      final history = await api.get('manufacturing/reports', {'cell_uid': uid});
      final selectedTest = data['tests'].first['test']['uid'] as String;
      final stats = await api.get('manufacturing/test', {
        'cell_uid': uid,
        'test_uid': selectedTest,
      });
      if (!mounted) return;
      setState(() {
        trace = data;
        processes = {
          for (final p in results) p['process']['uid'] as String: p as Map,
        };
        savedReports = history;
        testUid = selectedTest;
        test = stats;
      });
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> loadTest(String uid, int offset) async {
    setState(() => loading = true);
    try {
      final data = await api.get('manufacturing/test', {
        'cell_uid': cellUid!,
        'test_uid': uid,
        'offset': '$offset',
      });
      if (mounted) {
        setState(() {
          test = data;
          testUid = uid;
        });
      }
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> evidence(String uid, {Map? saved}) async {
    try {
      final data =
          saved ??
          await api.get('manufacturing/source', {
            'cell_uid': cellUid!,
            'evidence_uid': uid,
          }) as Map;
      if (mounted) await showEvidence(context, uid, null, evidence: data);
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    }
  }

  Future<void> openReport(String id) async {
    try {
      final data = await api.get('manufacturing/reports/$id');
      if (mounted) setState(() => report = data);
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    }
  }

  Future<void> generate() async {
    setState(() {
      running = true;
      report = null;
      error = null;
      progress = '正在检索制造证据…';
    });
    try {
      await for (final event in api.stream('manufacturing/reports', {
        'cell_uid': cellUid,
        'question': question.text.trim(),
      })) {
        if (!mounted) return;
        if (event['type'] == 'tool') {
          setState(
            () => progress =
                '${event['status'] == 'started' ? '正在执行' : '已读取'} · ${event['name']}',
          );
        } else if (event['type'] == 'answer') {
          final history = await api.get('manufacturing/reports', {
            'cell_uid': cellUid!,
          });
          if (mounted) setState(() => savedReports = history);
          await openReport(event['report_id']);
        } else if (event['type'] == 'error') {
          throw Exception(event['message']);
        }
      }
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    } finally {
      if (mounted) {
        setState(() {
          running = false;
          progress = '';
        });
      }
    }
  }

  Future<void> review() async {
    if (reviewer.text.trim().isEmpty || note.text.trim().isEmpty) {
      setState(() => error = '请填写复核人和复核意见。');
      return;
    }
    try {
      final data = await api.send(
        'POST',
        'manufacturing/reports/${report!['id']}/review',
        {
          'reviewer': reviewer.text.trim(),
          'decision': decision,
          'note': note.text.trim(),
        },
      );
      if (mounted) {
        setState(() {
          report = data;
          error = null;
        });
      }
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    }
  }

  Widget heading(String text) => Padding(
    padding: const EdgeInsets.only(bottom: 14),
    child: Text(
      text,
      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
    ),
  );

  Widget citation(String uid, {String? label, Map? saved}) => TextButton.icon(
    onPressed: () => evidence(uid, saved: saved),
    icon: const Icon(Icons.manage_search, size: 16),
    label: Text(label ?? uid),
  );

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      if (error != null)
        Padding(
          padding: const EdgeInsets.only(bottom: 16),
          child: SelectableText(
            error!,
            style: const TextStyle(color: Colors.red),
          ),
        ),
      if (dataset != null)
        Wrap(
          spacing: 10,
          runSpacing: 8,
          children: [
            const Tag('KIproBatt · 实验室制造'),
            Tag('${dataset!['kinds']['process']} 个过程实例'),
            Tag('${cells.length} 个测试关联对象'),
            Tag('${dataset!['linked_stats_files']} 份循环统计'),
          ],
        ),
      const SizedBox(height: 18),
      if (loading) const LinearProgressIndicator(),
      if (cells.isEmpty && !loading)
        const Panel(child: Text('尚未导入 KIproBatt 数据，请按 README 的制造数据导入步骤初始化。')),
      if (cells.isNotEmpty) ...[
        DropdownButtonFormField<String>(
          key: ValueKey(cellUid),
          initialValue: cellUid,
          isExpanded: true,
          decoration: const InputDecoration(labelText: '选择测试关联电芯'),
          items: [
            for (final row in cells)
              DropdownMenuItem(
                value: row['cell']['uid'] as String,
                child: Text(
                  '${row['cell']['name']} · ${row['tests'].first}',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(fontSize: 12),
                ),
              ),
          ],
          onChanged: running || loading ? null : (id) => selectCell(id!),
        ),
        const SizedBox(height: 20),
      ],
      if (trace != null) ...[
        Panel(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              heading('1 · 制造履历'),
              const Text(
                '沿明确前驱追溯，按上游 → 当前对象展示。',
                style: TextStyle(color: muted),
              ),
              const SizedBox(height: 12),
              for (final stage in trace!['stages'])
                ExpansionTile(
                  tilePadding: EdgeInsets.zero,
                  title: Text(
                    '${stage['process']?['name'] ?? '来源过程未导出'} → ${stage['object']['name']}',
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  subtitle: Text(
                    stage['object']['uid'],
                    style: const TextStyle(fontSize: 11, color: muted),
                  ),
                  children: [
                    Align(
                      alignment: Alignment.centerLeft,
                      child: citation(stage['object']['uid'], label: '查看对象来源'),
                    ),
                    if (stage['process'] != null)
                      for (final step
                          in processes[stage['process']['uid']]?['steps'] ?? [])
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              step['step']['name'],
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            for (final parameter in step['parameters'])
                              ListTile(
                                dense: true,
                                contentPadding: EdgeInsets.zero,
                                title: Text(
                                  parameter['name'],
                                  style: const TextStyle(fontSize: 12),
                                ),
                                subtitle: Text(
                                  (parameter['values'] as List).isEmpty
                                      ? '值未填写'
                                      : (parameter['values'] as List).join(
                                          ' · ',
                                        ),
                                  style: const TextStyle(fontSize: 12),
                                ),
                                trailing: IconButton(
                                  icon: const Icon(Icons.manage_search),
                                  tooltip: '查看参数 ${parameter['name']}',
                                  onPressed: () => evidence(parameter['uid']),
                                ),
                              ),
                          ],
                        ),
                  ],
                ),
              const Divider(),
              Text(
                '追溯终点 ${trace!['trace_endpoints'].length} 个：原始图谱未提供更上游的明确对象前驱。'
                '同过程中的其他对象不自动归入本电芯履历。',
                style: const TextStyle(color: muted, fontSize: 12, height: 1.6),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
      ],
      if (test != null)
        Panel(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              heading('2 · 循环测试记录'),
              if ((trace!['tests'] as List).length > 1)
                DropdownButtonFormField<String>(
                  initialValue: testUid,
                  isExpanded: true,
                  decoration: const InputDecoration(labelText: '测试文件'),
                  items: [
                    for (final t in trace!['tests'])
                      DropdownMenuItem(
                        value: t['test']['uid'] as String,
                        child: Text(
                          t['test']['name'],
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                  ],
                  onChanged: loading || running
                      ? null
                      : (id) => loadTest(id!, 0),
                ),
              SelectableText(
                test!['name'],
                style: const TextStyle(
                  fontWeight: FontWeight.w600,
                  fontSize: 12,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                '共 ${test!['row_count']} 行 · 通道 ${test!['metadata']['Channel Number'] ?? '未记录'}\n'
                '${test!['metadata']['TestDesc'] ?? ''}',
                style: const TextStyle(color: muted, fontSize: 12),
              ),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  columnSpacing: 28,
                  columns: [
                    for (final title in [
                      'Cycle',
                      '充电 / Ah',
                      '放电 / Ah',
                      '放电 / Wh',
                      '原始证据',
                    ])
                      DataColumn(label: Text(title)),
                  ],
                  rows: [
                    for (final row in test!['rows'])
                      DataRow(
                        cells: [
                          for (final key in [
                            'Cycle',
                            'AH-IN',
                            'AH-OUT',
                            'WH-OUT',
                          ])
                            DataCell(
                              Text(
                                row['values'][key] == null
                                    ? '—'
                                    : key == 'Cycle'
                                    ? '${(row['values'][key] as num).toInt()}'
                                    : (row['values'][key] as num)
                                          .toStringAsPrecision(7),
                              ),
                            ),
                          DataCell(
                            citation(
                              row['uid'],
                              label: '第 ${row['source_line']} 行',
                            ),
                          ),
                        ],
                      ),
                  ],
                ),
              ),
              Row(
                children: [
                  Text(
                    '${test!['offset'] + 1}–${test!['offset'] + (test!['rows'] as List).length} / ${test!['row_count']}',
                  ),
                  const Spacer(),
                  IconButton(
                    tooltip: '上一页循环',
                    icon: const Icon(Icons.chevron_left),
                    onPressed: loading || test!['offset'] == 0
                        ? null
                        : () => loadTest(testUid!, test!['offset'] - 12),
                  ),
                  IconButton(
                    tooltip: '下一页循环',
                    icon: const Icon(Icons.chevron_right),
                    onPressed:
                        loading || test!['offset'] + 12 >= test!['row_count']
                        ? null
                        : () => loadTest(testUid!, test!['offset'] + 12),
                  ),
                ],
              ),
              Text(
                test!['scope'],
                style: const TextStyle(color: muted, fontSize: 12, height: 1.6),
              ),
            ],
          ),
        ),
      if (trace != null) ...[
        const SizedBox(height: 20),
        Panel(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              heading('3 · Agent 复核报告'),
              TextField(
                controller: question,
                minLines: 2,
                maxLines: 5,
                enabled: !running,
                decoration: const InputDecoration(labelText: '复核任务'),
              ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 14,
                runSpacing: 8,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  FilledButton.icon(
                    onPressed: running || loading || !widget.modelReady
                        ? null
                        : generate,
                    icon: const Icon(Icons.auto_awesome, size: 18),
                    label: Text(running ? '正在生成…' : '生成制造复核报告'),
                  ),
                  if (!widget.modelReady)
                    const Text('模型服务未就绪', style: TextStyle(color: muted)),
                  if (running)
                    Text(
                      progress,
                      style: const TextStyle(color: teal, fontSize: 12),
                    ),
                ],
              ),
              if (savedReports.isNotEmpty) ...[
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  key: ValueKey(
                    'report:${report?['id']}:${savedReports.length}',
                  ),
                  initialValue: report?['id'],
                  isExpanded: true,
                  decoration: const InputDecoration(labelText: '已保存报告'),
                  items: [
                    for (final r in savedReports)
                      DropdownMenuItem(
                        value: r['id'] as String,
                        child: Text(
                          '${r['created_at']} · ${r['summary']}',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontSize: 12),
                        ),
                      ),
                  ],
                  onChanged: running ? null : (id) => openReport(id!),
                ),
              ],
              if (report != null) ...[
                const Divider(height: 32),
                SelectableText(
                  report!['answer']['summary'],
                  style: const TextStyle(
                    height: 1.7,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                for (final claim in report!['answer']['claims'])
                  Padding(
                    padding: const EdgeInsets.only(top: 14),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        SelectableText(
                          claim['statement'],
                          style: const TextStyle(height: 1.7),
                        ),
                        Wrap(
                          children: [
                            for (final id in claim['evidence_ids'])
                              citation(
                                id,
                                label:
                                    '来源 ${claim['evidence_ids'].indexOf(id) + 1}',
                                saved: report!['evidence'][id],
                              ),
                          ],
                        ),
                      ],
                    ),
                  ),
                for (final pair in [
                  ['待补充资料', 'unknowns'],
                  ['下一步', 'next_actions'],
                ]) ...[
                  const SizedBox(height: 14),
                  heading(pair[0]),
                  for (final text in report!['answer'][pair[1]])
                    Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: SelectableText(
                        '• $text',
                        style: const TextStyle(height: 1.6),
                      ),
                    ),
                ],
                const Divider(height: 32),
                heading('人工复核'),
                if (report!['review'] != null)
                  Text(
                    '${report!['review']['reviewer']} · ${report!['review']['decision'] == 'verified' ? '证据已复核' : '需补充资料'}\n'
                    '${report!['review']['note']}',
                    style: const TextStyle(height: 1.7),
                  )
                else ...[
                  TextField(
                    controller: reviewer,
                    decoration: const InputDecoration(labelText: '复核人'),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: note,
                    minLines: 2,
                    maxLines: 4,
                    decoration: const InputDecoration(labelText: '复核意见'),
                  ),
                  const SizedBox(height: 10),
                  DropdownButtonFormField<String>(
                    initialValue: decision,
                    decoration: const InputDecoration(labelText: '资料复核结论'),
                    items: const [
                      DropdownMenuItem(
                        value: 'needs_information',
                        child: Text('需补充资料'),
                      ),
                      DropdownMenuItem(value: 'verified', child: Text('证据已复核')),
                    ],
                    onChanged: (value) => setState(() => decision = value!),
                  ),
                  const SizedBox(height: 10),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: OutlinedButton(
                      onPressed: review,
                      child: const Text('保存人工复核'),
                    ),
                  ),
                ],
                const SizedBox(height: 12),
                const Text(
                  '复核针对报告证据，不构成生产放行。',
                  style: TextStyle(color: muted, fontSize: 12),
                ),
                Align(
                  alignment: Alignment.centerLeft,
                  child: TextButton.icon(
                    onPressed: () {
                      (web.HTMLAnchorElement()
                            ..href = api
                                .uri(
                                  'manufacturing/reports/${report!['id']}/export',
                                )
                                .toString()
                            ..download = '${report!['id']}.md')
                          .click();
                    },
                    icon: const Icon(Icons.download_outlined),
                    label: const Text('导出含来源的 Markdown 报告'),
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    ],
  );
}
