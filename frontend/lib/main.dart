import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';

import 'api.dart';
import 'cases.dart';
import 'copilot.dart';
import 'pages.dart';
import 'manufacturing.dart';
import 'widgets.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SemanticsBinding.instance.ensureSemantics();
  runApp(const BatteryApp());
}

class BatteryApp extends StatelessWidget {
  const BatteryApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'Battery Engineering Copilot',
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: teal),
      scaffoldBackgroundColor: const Color(0xFFF5F7F8),
      textTheme: ThemeData.light().textTheme.apply(
        bodyColor: ink,
        displayColor: ink,
      ),
      inputDecorationTheme: InputDecorationTheme(
        isDense: true,
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(9),
          borderSide: const BorderSide(color: line),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: line),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(9)),
        ),
      ),
    ),
    home: const Workbench(),
  );
}

class Workbench extends StatefulWidget {
  const Workbench({super.key});
  @override
  State<Workbench> createState() => _WorkbenchState();
}

class _WorkbenchState extends State<Workbench> {
  int battery = 1, section = 3;
  String scenario = 'kit-v1';
  List batteries = [];
  Map health = {};
  String? error;
  final titles = ['结构与记录', '工艺证据', '变更复核', '制造履历'];
  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    try {
      final data = await Future.wait([api.get('health'), api.get('batteries')]);
      if (mounted) {
        setState(() {
          health = data[0];
          batteries = data[1];
          error = null;
        });
      }
    } catch (e) {
      if (mounted) setState(() => error = '$e');
    }
  }

  void navigate(int value) => setState(() {
    section = value;
  });
  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width, wide = width > 1200;
    return Scaffold(
      body: Row(
        children: [
          if (width > 800)
            Container(
              width: 190,
              color: ink,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 28),
                  Row(
                    children: [
                      Container(
                        width: 34,
                        height: 34,
                        decoration: BoxDecoration(
                          color: teal,
                          borderRadius: BorderRadius.circular(9),
                        ),
                        child: const Icon(
                          Icons.battery_charging_full,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(width: 10),
                      const Text(
                        'BATTERY\nCOPILOT',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.5,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 54),
                  const Padding(
                    padding: EdgeInsets.only(left: 12),
                    child: Text(
                      '工作台',
                      style: TextStyle(color: Color(0xFF81969F), fontSize: 11),
                    ),
                  ),
                  const SizedBox(height: 16),
                  for (int i = 0; i < titles.length; i++)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Material(
                        color: section == i
                            ? const Color(0xFF2B424B)
                            : Colors.transparent,
                        borderRadius: BorderRadius.circular(9),
                        child: ListTile(
                          dense: true,
                          contentPadding: const EdgeInsets.symmetric(
                            horizontal: 12,
                          ),
                          leading: Icon(
                            [
                              Icons.hub_outlined,
                              Icons.description_outlined,
                              Icons.compare_arrows,
                              Icons.precision_manufacturing_outlined,
                            ][i],
                            size: 19,
                            color: section == i
                                ? const Color(0xFF6DD8C5)
                                : const Color(0xFF9BAEB6),
                          ),
                          title: Text(
                            titles[i],
                            style: TextStyle(
                              color: section == i
                                  ? Colors.white
                                  : const Color(0xFF9BAEB6),
                              fontSize: 13,
                            ),
                          ),
                          onTap: () => navigate(i),
                        ),
                      ),
                    ),
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      border: Border.all(color: const Color(0xFF344B55)),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '可追溯的工程知识',
                          style: TextStyle(
                            color: Color(0xFFD4E4E7),
                            fontSize: 12,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          '电芯制造履历 + 测试证据\n电池包拆解记录 + 工艺指南',
                          style: TextStyle(
                            color: Color(0xFF81969F),
                            height: 1.8,
                            fontSize: 10,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 26),
                ],
              ),
            ),
          Expanded(
            child: Column(
              children: [
                Container(
                  height: 64,
                  color: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 28),
                  child: Row(
                    children: [
                      const Text(
                        'ENGINEERING WORKSPACE',
                        style: TextStyle(
                          fontSize: 10,
                          letterSpacing: 1.5,
                          color: muted,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const Spacer(),
                      Tag(section == 3 ? 'KIproBatt · v0.3.2' : 'KIT · v1'),
                      IconButton(
                        onPressed: load,
                        tooltip: '刷新数据',
                        icon: const Icon(Icons.refresh, size: 20),
                      ),
                      if (!wide && section < 2)
                        IconButton(
                          tooltip: '打开工程助手',
                          icon: const Icon(Icons.auto_awesome_outlined),
                          onPressed: () => showModalBottomSheet(
                            context: context,
                            isScrollControlled: true,
                            builder: (_) => SizedBox(
                              height: MediaQuery.sizeOf(context).height * .9,
                              child: Copilot(
                                battery: battery,
                                scenario: scenario,
                                ready: health['model_ready'] == true,
                              ),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
                Expanded(
                  child: error != null
                      ? Center(child: Text(error!))
                      : batteries.isEmpty && section != 3
                      ? const Center(child: CircularProgressIndicator())
                      : SingleChildScrollView(
                          padding: const EdgeInsets.all(26),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                [
                                  '结构与拆解记录',
                                  '工艺证据库',
                                  '变更申请与复核',
                                  '电芯制造履历与检验复核',
                                ][section],
                                style: const TextStyle(
                                  fontSize: 28,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: -.8,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                [
                                  '沿真实关系查找对象，让每一步都有出处。',
                                  '查看文本、表格与图像，定位到原始页面。',
                                  '创建申请、补充资料并完成复核。业务资料为模拟设定。',
                                  '选择电芯，追溯制造记录、核对测试结果并生成有来源的复核报告。',
                                ][section],
                                style: const TextStyle(
                                  color: muted,
                                  fontSize: 12,
                                  height: 1.6,
                                ),
                              ),
                              const SizedBox(height: 22),
                              if (section != 3)
                                Wrap(
                                  spacing: 12,
                                  runSpacing: 12,
                                  crossAxisAlignment: WrapCrossAlignment.center,
                                  children: [
                                    SizedBox(
                                      width: 235,
                                      child: DropdownButtonFormField<int>(
                                        initialValue: battery,
                                        decoration: const InputDecoration(
                                          labelText: '当前电池包',
                                          prefixIcon: Icon(
                                            Icons.battery_5_bar_outlined,
                                            size: 18,
                                          ),
                                        ),
                                        items: [
                                          for (final item in batteries)
                                            DropdownMenuItem(
                                              value:
                                                  item['battery']['raw_id']
                                                      as int,
                                              child: Text(
                                                item['battery']['name'],
                                                style: const TextStyle(
                                                  fontSize: 13,
                                                ),
                                              ),
                                            ),
                                        ],
                                        onChanged: (value) => setState(() {
                                          battery = value!;
                                          scenario = 'kit-v1';
                                        }),
                                      ),
                                    ),
                                    if (section < 2)
                                      SizedBox(
                                        width: 220,
                                        child: DropdownButtonFormField<String>(
                                          key: ValueKey('$battery:$scenario'),
                                          initialValue: scenario,
                                          isExpanded: true,
                                          decoration: const InputDecoration(
                                            labelText: '数据场景',
                                          ),
                                          items: [
                                            const DropdownMenuItem(
                                              value: 'kit-v1',
                                              child: Text(
                                                '原始记录 · KIT v1',
                                                style: TextStyle(fontSize: 12),
                                              ),
                                            ),
                                            if (battery == 1) ...[
                                              const DropdownMenuItem(
                                                value: 'demo-change-01',
                                                child: Text(
                                                  '模拟变更 · 原工具卡',
                                                  style: TextStyle(
                                                    fontSize: 12,
                                                  ),
                                                ),
                                              ),
                                              const DropdownMenuItem(
                                                value: 'demo-change-02',
                                                child: Text(
                                                  '模拟变更 · 已更新工具卡',
                                                  style: TextStyle(
                                                    fontSize: 12,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ],
                                          onChanged: (value) =>
                                              setState(() => scenario = value!),
                                        ),
                                      ),
                                    if (section < 2)
                                      Tag(
                                        scenario == 'kit-v1' ? '原始数据' : '含模拟设定',
                                        color: scenario == 'kit-v1'
                                            ? teal
                                            : const Color(0xFFB08139),
                                      ),
                                  ],
                                ),
                              const SizedBox(height: 24),
                              if (width <= 800)
                                Wrap(
                                  spacing: 8,
                                  children: [
                                    for (int i = 0; i < titles.length; i++)
                                      ChoiceChip(
                                        label: Text(titles[i]),
                                        selected: section == i,
                                        onSelected: (_) => navigate(i),
                                      ),
                                  ],
                                ),
                              if (section == 3)
                                ManufacturingPage(
                                  modelReady: health['model_ready'] == true,
                                )
                              else if (section == 2)
                                CasesPage(
                                  key: ValueKey(battery),
                                  battery: battery,
                                )
                              else
                                EngineeringPage(
                                  key: ValueKey('$battery:$section:$scenario'),
                                  battery: battery,
                                  section: section,
                                  selected: batteries.firstWhere(
                                    (v) => v['battery']['raw_id'] == battery,
                                  ),
                                ),
                            ],
                          ),
                        ),
                ),
              ],
            ),
          ),
          if (wide && section < 2) Container(width: 1, color: line),
          if (wide && section < 2)
            Copilot(
              key: ValueKey('$battery:$scenario'),
              battery: battery,
              scenario: scenario,
              ready: health['model_ready'] == true,
            ),
        ],
      ),
    );
  }
}
