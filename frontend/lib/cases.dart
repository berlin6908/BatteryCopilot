import 'package:flutter/material.dart';
import 'package:web/web.dart' as web;

import 'api.dart';
import 'case_form.dart';
import 'widgets.dart';

const caseStatuses = {
  'draft': '草稿',
  'awaiting_information': '待补充',
  'awaiting_review': '待复核',
  'completed': '已完成',
};
const findingStatuses = {'pass': '规则通过', 'missing': '缺少资料', 'conflict': '存在冲突'};

class CasesPage extends StatefulWidget {
  final int battery;
  const CasesPage({super.key, required this.battery});
  @override
  State<CasesPage> createState() => _CasesPageState();
}

class _CasesPageState extends State<CasesPage> {
  List items = [];
  Map? current;
  bool busy = false;
  String? error;

  @override
  void initState() {
    super.initState();
    run(refresh);
  }

  Future<void> run(Future<void> Function() action) async {
    setState(() {
      busy = true;
      error = null;
    });
    try {
      await action();
    } catch (e) {
      if (mounted) error = '$e';
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> refresh() async {
    final result =
        await api.get('cases', {'battery_id': '${widget.battery}'}) as List;
    if (!mounted) return;
    items = result;
    final id = current?['id'] ?? (items.isNotEmpty ? items.first['id'] : null);
    if (id != null) current = await api.get('cases/$id') as Map;
  }

  Future<void> edit({bool creating = false}) async {
    final input = creating
        ? await api.get('cases/example', {'battery_id': '${widget.battery}'})
              as Map
        : current!['input'] as Map;
    if (!mounted) return;
    final values = await showDialog<Map>(
      context: context,
      builder: (_) => CaseForm(input: input, creating: creating),
    );
    if (values == null || !mounted) return;
    current = creating
        ? await api.send('POST', 'cases', values)
        : await api.send('PUT', 'cases/${current!['id']}', {
            'version': current!['version'],
            'input': values,
          });
    await refresh();
  }

  Future<void> action(String name, [Map extra = const {}]) async {
    current = await api.send('POST', 'cases/${current!['id']}/$name', {
      'version': current!['version'],
      ...extra,
    });
    await refresh();
  }

  Future<void> review(Map report, Map finding) async {
    final form = GlobalKey<FormState>();
    String reviewer = '', note = '';
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('复核：${finding['title']}'),
        content: SizedBox(
          width: 460,
          child: Form(
            key: form,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('请查看条目中的证据，再记录你的复核意见。'),
                const SizedBox(height: 18),
                TextFormField(
                  decoration: const InputDecoration(labelText: '复核人'),
                  onChanged: (v) => reviewer = v.trim(),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? '请填写复核人' : null,
                ),
                const SizedBox(height: 14),
                TextFormField(
                  decoration: const InputDecoration(labelText: '复核意见'),
                  maxLines: 3,
                  onChanged: (v) => note = v.trim(),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? '请填写复核意见' : null,
                ),
              ],
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('取消'),
          ),
          FilledButton(
            onPressed: () {
              if (form.currentState!.validate()) Navigator.pop(context, true);
            },
            child: const Text('确认复核'),
          ),
        ],
      ),
    );
    if (confirmed == true) {
      await action('review', {
        'report_id': report['id'],
        'finding_id': finding['id'],
        'reviewer': reviewer,
        'note': note,
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final selected = current;
    final reports = selected?['reports'] as List? ?? [];
    final report =
        reports
                .where((r) => r['id'] == selected?['current_report_id'])
                .firstOrNull
            as Map?;
    final completed = selected?['status'] == 'completed';
    final canComplete =
        report != null &&
        (report['findings'] as List).every(
          (f) => f['status'] == 'pass' && report['reviews'][f['id']] != null,
        );
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: [
            FilledButton.icon(
              onPressed: busy ? null : () => run(() => edit(creating: true)),
              icon: const Icon(Icons.add),
              label: const Text('新建申请'),
            ),
            OutlinedButton.icon(
              onPressed: busy ? null : () => run(refresh),
              icon: const Icon(Icons.refresh),
              label: const Text('刷新变更单'),
            ),
          ],
        ),
        const SizedBox(height: 14),
        if (busy) ...[
          const LinearProgressIndicator(),
          const SizedBox(height: 8),
          const Text('正在处理，申请资料会保存在工作台中。', style: TextStyle(color: muted)),
        ],
        if (error != null)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: SelectableText(
              error!,
              style: const TextStyle(color: Colors.red),
            ),
          ),
        if (items.isEmpty && !busy)
          const Panel(child: Text('还没有变更申请。选择一个模拟示例，完成从分析到人工复核的整个流程。')),
        if (items.isNotEmpty)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: DropdownButtonFormField<String>(
              key: ValueKey(selected?['id']),
              initialValue: selected?['id'],
              isExpanded: true,
              decoration: const InputDecoration(labelText: '已保存的变更单'),
              items: [
                for (final item in items)
                  DropdownMenuItem(
                    value: item['id'],
                    child: Text(
                      '${item['title']} · ${caseStatuses[item['status']]} · ${item['id']}',
                    ),
                  ),
              ],
              onChanged: busy
                  ? null
                  : (id) => run(() async {
                      current = await api.get('cases/$id') as Map;
                    }),
            ),
          ),
        if (selected != null) ...[
          Panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Wrap(
                  spacing: 10,
                  runSpacing: 8,
                  children: [
                    Tag(caseStatuses[selected['status']]!),
                    Tag('输入版本 ${selected['input_version']}'),
                    const Tag('模拟业务资料', color: Color(0xFFB08139)),
                  ],
                ),
                const SizedBox(height: 16),
                Text(
                  selected['input']['title'],
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  '${selected['input']['old_spec']} → ${selected['input']['new_spec']}  ·  ${selected['input']['target_uid']}',
                ),
                const SizedBox(height: 8),
                Text(
                  selected['input']['reason'],
                  style: const TextStyle(color: muted),
                ),
                const SizedBox(height: 16),
                Text(
                  selected['input']['tool_card'] == null
                      ? '工具卡：待补充'
                      : '工具卡：${selected['input']['tool_card']['id']} / ${selected['input']['tool_card']['revision']} · 支持 ${selected['input']['tool_card']['supported_specs'].join('、')}',
                ),
                const SizedBox(height: 8),
                Text(
                  selected['input']['instruction'] == null
                      ? '作业指导书：待补充'
                      : '作业指导书：${selected['input']['instruction']['id']} / ${selected['input']['instruction']['revision']} · ${selected['input']['instruction']['spec']}',
                ),
                const SizedBox(height: 20),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: [
                    OutlinedButton(
                      onPressed: busy ? null : () => run(edit),
                      child: const Text('补充或修改资料'),
                    ),
                    FilledButton.icon(
                      onPressed: busy || completed
                          ? null
                          : () => run(() => action('analyze')),
                      icon: const Icon(Icons.auto_awesome_outlined, size: 18),
                      label: Text(
                        selected['analysis_status'] == 'running' ||
                                selected['analysis_status'] == 'failed'
                            ? '重试分析'
                            : '分析当前资料',
                      ),
                    ),
                    if (report != null)
                      OutlinedButton.icon(
                        onPressed: busy
                            ? null
                            : () {
                                (web.HTMLAnchorElement()
                                      ..href = api
                                          .uri('cases/${selected['id']}/export')
                                          .toString()
                                      ..download = '${selected['id']}.md')
                                    .click();
                              },
                        icon: const Icon(Icons.download, size: 18),
                        label: const Text('导出报告'),
                      ),
                  ],
                ),
                if (selected['last_error'] != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 14),
                    child: SelectableText(
                      '分析未完成：${selected['last_error']}',
                      style: const TextStyle(color: Colors.red),
                    ),
                  ),
                if (selected['analysis_status'] == 'running')
                  const Padding(
                    padding: EdgeInsets.only(top: 14),
                    child: Text(
                      '分析正在进行，可刷新查看结果；重试会替换上一次分析。',
                      style: TextStyle(color: muted),
                    ),
                  ),
              ],
            ),
          ),
          if (report != null) ...[
            const SizedBox(height: 20),
            CaseReport(
              report: report,
              battery: widget.battery,
              onReview: busy || completed
                  ? null
                  : (finding) => run(() => review(report, finding)),
            ),
            const SizedBox(height: 16),
            Align(
              alignment: Alignment.centerLeft,
              child: FilledButton.icon(
                onPressed: busy || completed || !canComplete
                    ? null
                    : () => run(() => action('complete')),
                icon: Icon(
                  completed ? Icons.check_circle_outline : Icons.task_alt,
                ),
                label: Text(completed ? '变更单已完成' : '完成变更单'),
              ),
            ),
            if (!completed)
              const Padding(
                padding: EdgeInsets.only(top: 8),
                child: Text(
                  '全部检查通过并逐项人工复核后，才能完成变更单。',
                  style: TextStyle(color: muted),
                ),
              ),
          ],
          for (final old in reports.reversed.where(
            (r) => r['id'] != selected['current_report_id'],
          ))
            Padding(
              padding: const EdgeInsets.only(top: 18),
              child: ExpansionTile(
                title: Text(
                  '历史报告 #${old['number']} · 输入版本 ${old['input_version']}',
                ),
                subtitle: Text(
                  '${old['input']['old_spec']} → ${old['input']['new_spec']} · ${old['completed_at'] != null ? '曾完成复核' : '历史记录'}',
                ),
                children: [CaseReport(report: old, battery: widget.battery)],
              ),
            ),
        ],
      ],
    );
  }
}

class CaseReport extends StatelessWidget {
  final Map report;
  final int battery;
  final void Function(Map)? onReview;
  const CaseReport({
    super.key,
    required this.report,
    required this.battery,
    this.onReview,
  });

  Widget citations(BuildContext context, List ids) => Wrap(
    spacing: 8,
    runSpacing: 6,
    children: [
      for (final uid in ids)
        Builder(
          builder: (context) {
            final source =
                (report['evidence'] as List)
                        .where((e) => e['uid'] == uid)
                        .firstOrNull
                    as Map?;
            return ActionChip(
              tooltip: uid,
              label: Text(
                source?['name'] ?? uid,
                style: const TextStyle(fontSize: 11),
              ),
              avatar: const Icon(Icons.source_outlined, size: 15),
              onPressed: () =>
                  showEvidence(context, uid, battery, evidence: source),
            );
          },
        ),
    ],
  );

  @override
  Widget build(BuildContext context) => Panel(
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '复核清单 · 报告 #${report['number']}',
          style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w700),
        ),
        for (final finding in report['findings']) ...[
          const Divider(height: 30),
          Wrap(
            spacing: 12,
            runSpacing: 8,
            crossAxisAlignment: WrapCrossAlignment.center,
            children: [
              Text(
                finding['title'],
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
              Tag(
                findingStatuses[finding['status']]!,
                color: finding['status'] == 'pass'
                    ? teal
                    : const Color(0xFFB66D32),
              ),
              if (report['reviews'][finding['id']] != null) const Tag('已人工复核'),
            ],
          ),
          const SizedBox(height: 12),
          Text(finding['detail']),
          const SizedBox(height: 8),
          Text(finding['action'], style: const TextStyle(color: muted)),
          const SizedBox(height: 12),
          citations(context, finding['evidence_ids']),
          if (report['reviews'][finding['id']] case final Map review)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: SelectableText(
                '${review['reviewer']}：${review['note']}\n${review['at']}',
                style: const TextStyle(color: teal, fontSize: 12),
              ),
            )
          else if (finding['status'] == 'pass')
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: OutlinedButton(
                onPressed: onReview == null ? null : () => onReview!(finding),
                child: Text('复核${finding['title']}'),
              ),
            ),
        ],
        const Divider(height: 36),
        const Text(
          'Agent 分析说明',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        SelectableText(
          report['answer']['summary'],
          style: const TextStyle(height: 1.7),
        ),
        for (final claim in report['answer']['claims']) ...[
          const SizedBox(height: 16),
          SelectableText(
            claim['statement'],
            style: const TextStyle(height: 1.7),
          ),
          const SizedBox(height: 6),
          citations(context, claim['evidence_ids']),
        ],
        if ((report['answer']['unknowns'] as List).isNotEmpty) ...[
          const SizedBox(height: 18),
          const Text('仍需进一步确认', style: TextStyle(fontWeight: FontWeight.w600)),
          for (final gap in report['answer']['unknowns'])
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text('• $gap', style: const TextStyle(color: muted)),
            ),
        ],
      ],
    ),
  );
}
