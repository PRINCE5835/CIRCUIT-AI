// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:convert';
import 'dart:html' as html;

class SseClient {
  final String url;
  final Map<String, dynamic> body;
  final void Function(String token) onToken;
  final void Function(Map<String, dynamic> meta) onMeta;
  final void Function(String content, Map<String, dynamic>? meta, int? conversationId) onDone;
  final void Function(String error) onError;
  html.HttpRequest? _request;

  SseClient({
    required this.url,
    required this.body,
    required this.onToken,
    required this.onMeta,
    required this.onDone,
    required this.onError,
  });

  void connect() {
    _request = html.HttpRequest();
    _request!.open('POST', url);
    _request!.setRequestHeader('Content-Type', 'application/json');
    _request!.setRequestHeader('Accept', 'text/event-stream');
    _request!.responseType = 'text';
    _request!.send(jsonEncode(body));

    var lastIndex = 0;

    _request!.onProgress.listen((_) {
      final responseText = _request!.responseText ?? '';
      final newData = responseText.substring(lastIndex);
      lastIndex = responseText.length;

      final lines = newData.split('\n');
      for (final line in lines) {
        if (line.startsWith('data: ')) {
          final raw = line.substring(6).trim();
          if (raw.isEmpty) continue;
          try {
            final data = jsonDecode(raw) as Map<String, dynamic>;
            final type = data['type'] as String?;
            switch (type) {
              case 'token':
                onToken(data['token'] as String? ?? '');
                break;
              case 'meta':
                onMeta(data);
                break;
              case 'done':
                onDone(
                  data['content'] as String? ?? '',
                  data['meta'] as Map<String, dynamic>?,
                  data['conversation_id'] as int?,
                );
                break;
              case 'conv_id':
                onDone('', null, data['conversation_id'] as int?);
                break;
              case 'error':
                onError(data['detail'] as String? ?? 'Unknown error');
                break;
            }
          } catch (_) {}
        }
      }
    });

    _request!.onError.listen((_) {
      onError('Connection failed');
    });

    _request!.onLoadEnd.listen((_) {
      // Connection closed
    });
  }

  void close() {
    _request?.abort();
  }
}
