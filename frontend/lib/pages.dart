import 'package:flutter/material.dart';

import 'api.dart';
import 'widgets.dart';

class EngineeringPage extends StatefulWidget {
  final int battery, section;
  final Map selected;
  const EngineeringPage({
    super.key,
    required this.battery,
    required this.section,
    required this.selected,
  });
  @override
  State<EngineeringPage> createState() => _EngineeringPageState();
}

class _EngineeringPageState extends State<EngineeringPage> {
  List entities = [], sequence = [], evidence = [];
  Map graphData = {};
  String kind = 'Part';
  int offset = 0, total = 0, page = 18;
  bool busy = true;
  String? error;
  final search = TextEditingController();
  Map<String, String> get scope => {'battery_id': '${widget.battery}'};
  @override
  void initState() {
    super.initState();
    load();
  }

  @override
  void dispose() {
    search.dispose();
    super.dispose();
  }

  Future<void> run(Future<void> Function() work) async {
    setState(() {
      busy = true;
      error = null;
    });
    try {
      await work();
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> load() => run(() async {
    if (widget.section == 0) {
      final data = await Future.wait([
        api.get('entities', scope),
        api.get('sequence', scope),
      ]);
      final uid = widget.battery == 1
          ? 'kit-v1:fixation:1000'
          : data[0][0]['uid'];
      final neighborhood = await api.get('graph/$uid', scope);
      if (mounted) {
        setState(() {
          entities = data[0];
          sequence = data[1]['items'];
          total = data[1]['total'];
          graphData = neighborhood;
        });
      }
    } else if (widget.section == 1) {
      final data = await api.get('documents/pem/elements', {'page': '$page'});
      if (mounted) setState(() => evidence = data);
    }
  });
  Future<void> changeGraph(String uid) => run(() async {
    final data = await api.get('graph/$uid', scope);
    if (mounted) setState(() => graphData = data);
  });
  Future<void> find() => run(() async {
    final data = widget.section == 0
        ? await api.get('entities', {...scope, 'q': search.text, 'kind': kind})
        : search.text.trim().isEmpty
        ? await api.get('documents/pem/elements', {'page': '$page'})
        : await api.get('search', {
            ...scope,
            'q': search.text,
            'scope': 'guide',
          });
    if (mounted) {
      setState(() {
        if (widget.section == 0) {
          entities = data;
        } else {
          evidence = data;
        }
      });
    }
  });
  Future<void> turn(int step) => run(() async {
    final next = (offset + step).clamp(0, total - 1);
    final data = await api.get('sequence', {...scope, 'offset': '$next'});
    if (mounted) {
      setState(() {
        sequence = data['items'];
        offset = next;
      });
    }
  });
  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      if (busy) const LinearProgressIndicator(minHeight: 2),
      if (error != null)
        Padding(
          padding: const EdgeInsets.all(12),
          child: Text(error!, style: const TextStyle(color: Colors.deepOrange)),
        ),
      if (widget.section == 0 && graphData.isNotEmpty) explorer(),
      if (widget.section == 1) documents(),
    ],
  );
  Widget stat(String label, dynamic value, IconData icon) => Expanded(
    child: Panel(
      padding: const EdgeInsets.all(17),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(label, style: const TextStyle(color: muted, fontSize: 11)),
              const Spacer(),
              Icon(icon, size: 17, color: teal),
            ],
          ),
          const SizedBox(height: 13),
          Text(
            '$value',
            style: const TextStyle(
              fontSize: 29,
              fontWeight: FontWeight.w600,
              letterSpacing: -1,
            ),
          ),
        ],
      ),
    ),
  );
  Widget explorer() => Column(
    children: [
      Row(
        children: [
          stat('部件', widget.selected['parts'], Icons.view_in_ar_outlined),
          const SizedBox(width: 12),
          stat('连接件', widget.selected['fixations'], Icons.link),
          const SizedBox(width: 12),
          stat('拆解操作', total, Icons.route_outlined),
        ],
      ),
      const SizedBox(height: 20),
      Panel(
        padding: EdgeInsets.zero,
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(18, 12, 12, 12),
              child: Row(
                children: [
                  const Text(
                    '对象关系',
                    style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
                  ),
                  const Spacer(),
                  const Tag('局部图谱'),
                  IconButton(
                    onPressed: () => showEvidence(
                      context,
                      graphData['nodes'][0]['uid'],
                      widget.battery,
                    ),
                    tooltip: '查看当前对象证据',
                    icon: const Icon(Icons.open_in_new, size: 16),
                  ),
                ],
              ),
            ),
            const Divider(height: 1),
            SizedBox(
              height: 330,
              child: Row(
                children: [
                  SizedBox(
                    width: 195,
                    child: Column(
                      children: [
                        Padding(
                          padding: const EdgeInsets.all(10),
                          child: TextField(
                            controller: search,
                            onSubmitted: (_) => find(),
                            decoration: InputDecoration(
                              hintText: '名称 / ID / 件号',
                              hintStyle: const TextStyle(fontSize: 11),
                              suffixIcon: IconButton(
                                onPressed: find,
                                tooltip: '搜索对象',
                                icon: const Icon(Icons.search, size: 18),
                              ),
                            ),
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          child: DropdownButton<String>(
                            value: kind,
                            isDense: true,
                            isExpanded: true,
                            items: [
                              for (final k in ['Part', 'Fixation', 'Operation'])
                                DropdownMenuItem(
                                  value: k,
                                  child: Text(
                                    kindName(k),
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                ),
                            ],
                            onChanged: (v) {
                              setState(() => kind = v!);
                              find();
                            },
                          ),
                        ),
                        const SizedBox(height: 8),
                        Expanded(
                          child: ListView.builder(
                            itemCount: entities.length,
                            itemBuilder: (context, index) {
                              final item = entities[index];
                              return ListTile(
                                dense: true,
                                selected:
                                    graphData['nodes'][0]['uid'] == item['uid'],
                                title: Text(
                                  item['name'],
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(fontSize: 12),
                                ),
                                subtitle: Text(
                                  '#${item['raw_id']}',
                                  style: const TextStyle(
                                    fontSize: 10,
                                    color: muted,
                                  ),
                                ),
                                onTap: () => changeGraph(item['uid']),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(width: 1, color: line),
                  Expanded(
                    child: ClipRect(
                      child: Container(
                        color: const Color(0xFFFAFCFC),
                        padding: const EdgeInsets.all(20),
                        child: LocalGraph(
                          key: ValueKey(graphData['nodes'][0]['uid']),
                          data: graphData,
                          onSelect: (uid) =>
                              showEvidence(context, uid, widget.battery),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: const BoxDecoration(
                border: Border(top: BorderSide(color: line)),
              ),
              child: const Row(
                children: [
                  Icon(Icons.info_outline, size: 14, color: muted),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      '原始连接 / 移除关系。点击节点查看出处，可拖动与缩放。',
                      style: TextStyle(fontSize: 10, color: muted),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 20),
      Panel(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text(
                  '已记录的拆解顺序',
                  style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
                ),
                const Spacer(),
                Text(
                  '共 $total 步',
                  style: const TextStyle(color: muted, fontSize: 11),
                ),
              ],
            ),
            const SizedBox(height: 6),
            const Text(
              '顺序来自数据记录，不代表全部可行顺序。',
              style: TextStyle(color: muted, fontSize: 11),
            ),
            const SizedBox(height: 16),
            for (final item in sequence.take(7))
              InkWell(
                onTap: () => showEvidence(context, item['uid'], widget.battery),
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 10),
                  child: Row(
                    children: [
                      Container(
                        width: 30,
                        height: 26,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: const Color(0xFFF0F4F5),
                          borderRadius: BorderRadius.circular(5),
                        ),
                        child: Text(
                          '${item['sequence_index']}',
                          style: const TextStyle(fontSize: 11, color: muted),
                        ),
                      ),
                      const SizedBox(width: 15),
                      SizedBox(
                        width: 90,
                        child: Text(
                          item['name'],
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      Expanded(
                        child: Text(
                          item['target_uid'],
                          style: const TextStyle(fontSize: 11, color: muted),
                        ),
                      ),
                      const Icon(Icons.north_east, size: 14, color: muted),
                    ],
                  ),
                ),
              ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: offset == 0 ? null : () => turn(-7),
                  child: const Text('上一段'),
                ),
                TextButton(
                  onPressed: offset + 7 >= total ? null : () => turn(7),
                  child: const Text('下一段 →'),
                ),
              ],
            ),
          ],
        ),
      ),
    ],
  );
  Widget documents() => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Panel(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.menu_book_outlined, color: teal),
                SizedBox(width: 10),
                Expanded(
                  child: Text(
                    'Production Process of Battery Modules and Battery Packs',
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            const Text(
              'PEM / RWTH Aachen · 通用工艺知识 · 28 页',
              style: TextStyle(color: muted, fontSize: 12),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: search,
                    onSubmitted: (_) => find(),
                    decoration: const InputDecoration(
                      hintText: '检索，例如：模组安装质量要求',
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                FilledButton(
                  onPressed: busy ? null : find,
                  child: const Text('检索'),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                for (final p in [14, 18, 21, 24])
                  ActionChip(
                    label: Text('第 $p 页'),
                    onPressed: () {
                      page = p;
                      search.clear();
                      find();
                    },
                  ),
              ],
            ),
          ],
        ),
      ),
      const SizedBox(height: 16),
      if (evidence.isEmpty && !busy) const Panel(child: Text('暂无证据元素。')),
      for (final item in evidence)
        Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: InkWell(
            onTap: () => showEvidence(context, item['uid'], widget.battery),
            borderRadius: BorderRadius.circular(14),
            child: Panel(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Tag(kindName(item['kind'])),
                      const SizedBox(width: 8),
                      Text(
                        '第 ${item['page']} 页',
                        style: const TextStyle(color: muted, fontSize: 11),
                      ),
                      const Spacer(),
                      const Icon(Icons.open_in_new, size: 15, color: teal),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    item['name'] ?? '',
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    item['text'] ?? '',
                    maxLines: 4,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: muted,
                      fontSize: 12,
                      height: 1.7,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
    ],
  );
}
