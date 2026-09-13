import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:graphview/GraphView.dart' as gv;

import 'api.dart';

const ink = Color(0xFF172D37),
    teal = Color(0xFF087F74),
    muted = Color(0xFF71818A),
    line = Color(0xFFE2E9EC);

class Panel extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;
  const Panel({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(20),
  });
  @override
  Widget build(BuildContext context) => Container(
    padding: padding,
    decoration: BoxDecoration(
      color: Colors.white,
      border: Border.all(color: line),
      borderRadius: BorderRadius.circular(14),
    ),
    child: child,
  );
}

class Tag extends StatelessWidget {
  final String text;
  final Color color;
  const Tag(this.text, {super.key, this.color = teal});
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 5),
    decoration: BoxDecoration(
      color: color.withValues(alpha: .09),
      borderRadius: BorderRadius.circular(6),
    ),
    child: Text(
      text,
      style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.w600),
    ),
  );
}

String kindName(dynamic kind) => switch (kind) {
  'Part' => '部件',
  'Fixation' => '连接件',
  'Operation' => '拆解操作',
  'Battery' => '电池包',
  'picture' => '图像',
  'table' => '表格',
  _ => '文本',
};

class LocalGraph extends StatelessWidget {
  final Map data;
  final void Function(String) onSelect;
  const LocalGraph({super.key, required this.data, required this.onSelect});
  @override
  Widget build(BuildContext context) {
    final graph = gv.Graph();
    final nodes = <String, Map>{
      for (final n in data['nodes']) n['uid'] as String: n as Map,
    };
    final graphNodes = {for (final id in nodes.keys) id: gv.Node.Id(id)};
    for (final node in graphNodes.values) {
      graph.addNode(node);
    }
    for (final edge in data['edges']) {
      graph.addEdge(
        graphNodes[edge['source']]!,
        graphNodes[edge['target']]!,
        paint: Paint()
          ..color = const Color(0xFFB4C8CC)
          ..strokeWidth = 1.5,
      );
    }
    final config = gv.SugiyamaConfiguration()
      ..orientation = gv.SugiyamaConfiguration.ORIENTATION_LEFT_RIGHT
      ..levelSeparation = 38
      ..nodeSeparation = 20;
    return gv.GraphView.builder(
      animated: false,
      graph: graph,
      algorithm: gv.SugiyamaAlgorithm(config),
      builder: (node) {
        final item = nodes[node.key!.value]!;
        final color = item['kind'] == 'Operation'
            ? const Color(0xFF5D67AC)
            : item['kind'] == 'Fixation'
            ? const Color(0xFFBC853A)
            : teal;
        return Semantics(
          button: true,
          label: '${item['name']} ${item['raw_id']}',
          child: InkWell(
            onTap: () => onSelect(item['uid']),
            borderRadius: BorderRadius.circular(10),
            child: Container(
              width: 144,
              height: 88,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: color.withValues(alpha: .5)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '${kindName(item['kind'])} · ${item['raw_id']}',
                    style: TextStyle(color: color, fontSize: 11),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    item['name'],
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

Future<void> showEvidence(BuildContext context, String uid, int battery) async {
  try {
    final data = await api.get('evidence/${Uri.encodeComponent(uid)}', {
      'battery_id': '$battery',
    }) as Map;
    if (!context.mounted) return;
    await showDialog<void>(
      context: context,
      builder: (context) => Dialog(
        child: SizedBox(
          width: 1100,
          height: 760,
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 16, 12, 12),
                child: Row(
                  children: [
                    const Icon(Icons.fact_check_outlined, color: teal),
                    const SizedBox(width: 10),
                    const Text(
                      '证据溯源',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const Spacer(),
                    Tag(
                      data['source_kind'] == 'guide'
                          ? '通用工艺指南'
                          : data['source_kind'] == 'simulation'
                          ? '模拟设定'
                          : 'KIT 原始记录',
                    ),
                    IconButton(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(Icons.close),
                      tooltip: '关闭证据',
                    ),
                  ],
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (data['image_url'] != null)
                      Expanded(
                        flex: 3,
                        child: Container(
                          color: const Color(0xFFF1F4F5),
                          child: InteractiveViewer(
                            minScale: .5,
                            maxScale: 4,
                            child: Center(
                              child: AspectRatio(
                                aspectRatio:
                                    (data['page_width'] as num) /
                                    (data['page_height'] as num),
                                child: LayoutBuilder(
                                  builder: (context, size) {
                                    final box = List<num>.from(data['bbox']);
                                    return Stack(
                                      children: [
                                        Positioned.fill(
                                          child: Image.network(
                                            data['image_url'],
                                            fit: BoxFit.fill,
                                          ),
                                        ),
                                        Positioned(
                                          left: box[0] * size.maxWidth,
                                          top: box[1] * size.maxHeight,
                                          width:
                                              (box[2] - box[0]) * size.maxWidth,
                                          height:
                                              (box[3] - box[1]) *
                                              size.maxHeight,
                                          child: Container(
                                            decoration: BoxDecoration(
                                              color: teal.withValues(alpha: .1),
                                              border: Border.all(
                                                color: teal,
                                                width: 2,
                                              ),
                                            ),
                                          ),
                                        ),
                                      ],
                                    );
                                  },
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    Expanded(
                      flex: 2,
                      child: SingleChildScrollView(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              data['name'] ?? data['tool_card'] ?? uid,
                              style: const TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            const SizedBox(height: 12),
                            SelectableText(
                              uid,
                              style: const TextStyle(
                                color: muted,
                                fontSize: 12,
                              ),
                            ),
                            const SizedBox(height: 18),
                            Text(
                              '${data['source_file'] ?? 'data/scenarios.json'}${data['page'] != null
                                  ? ' · 第 ${data['page']} 页'
                                  : data['source_line'] != null
                                  ? ' · 第 ${data['source_line']} 行'
                                  : ''}',
                              style: const TextStyle(
                                color: teal,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            const SizedBox(height: 20),
                            SelectableText(
                              data['text'] ?? data['description'] ?? '',
                              style: const TextStyle(height: 1.7),
                            ),
                            if (data['raw_record'] != null) ...[
                              const SizedBox(height: 24),
                              const Text(
                                '原始 CSV 行',
                                style: TextStyle(fontWeight: FontWeight.w600),
                              ),
                              const SizedBox(height: 8),
                              SelectableText(
                                const JsonEncoder.withIndent('  ')
                                    .convert(jsonDecode(data['raw_record'])),
                                style: const TextStyle(
                                  fontFamily: 'monospace',
                                  fontSize: 12,
                                  height: 1.6,
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  } catch (e) {
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e')));
    }
  }
}
