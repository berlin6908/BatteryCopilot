import 'dart:convert';

import 'package:http/http.dart' as http;

class Api {
  final client = http.Client();
  Uri uri(String path, [Map<String, String>? query]) =>
      Uri.base.resolve('/api/$path').replace(queryParameters: query);
  Future<dynamic> get(String path, [Map<String, String>? query]) async {
    final response = await client.get(uri(path, query));
    final data = jsonDecode(utf8.decode(response.bodyBytes));
    if (response.statusCode != 200) throw Exception(data['detail'] ?? '请求失败');
    return data;
  }

  Stream<Map<String, dynamic>> ask(
    String question,
    int battery,
    String scenario,
  ) async* {
    final request = http.Request('POST', uri('agent/run'))
      ..headers['Content-Type'] = 'application/json'
      ..body = jsonEncode({
        'question': question,
        'battery_id': battery,
        'scenario_id': scenario,
      });
    final response = await client.send(request);
    if (response.statusCode != 200) {
      throw Exception(
        jsonDecode(await response.stream.bytesToString())['detail'],
      );
    }
    await for (final line
        in response.stream
            .transform(utf8.decoder)
            .transform(const LineSplitter())) {
      if (line.isNotEmpty) yield jsonDecode(line) as Map<String, dynamic>;
    }
  }
}

final api = Api();
