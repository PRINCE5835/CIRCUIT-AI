// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:js' as js;
import 'dart:html' as html;

class SpeechService {
  js.JsObject? _recognition;
  bool _isListening = false;
  bool _supported = false;
  void Function(String text)? onResult;
  void Function(String error)? onError;
  void Function()? onEnd;

  SpeechService() {
    _checkSupport();
  }

  void _checkSupport() {
    try {
      final ctx = js.context;
      final hasWebkit = ctx.callMethod('hasOwnProperty', ['webkitSpeechRecognition']) as bool? ?? false;
      final hasStandard = ctx.callMethod('hasOwnProperty', ['SpeechRecognition']) as bool? ?? false;
      if (hasWebkit || hasStandard) {
        _supported = true;
        final ctorName = hasWebkit ? 'webkitSpeechRecognition' : 'SpeechRecognition';
        final ctor = ctx[ctorName];
        if (ctor != null) {
          _recognition = js.JsObject(ctor as js.JsFunction);
          _recognition!['lang'] = 'en-US';
          _recognition!['continuous'] = false;
          _recognition!['interimResults'] = false;

          _recognition!['onresult'] = (event) {
            try {
              final results = (event as js.JsObject)['results'] as js.JsObject;
              final len = results['length'] as int? ?? 0;
              if (len > 0) {
                final result = results[0] as js.JsObject;
                final isFinal = result['isFinal'] as bool? ?? false;
                if (isFinal) {
                  final transcript = (result[0] as js.JsObject)['transcript'] as String? ?? '';
                  if (transcript.isNotEmpty && onResult != null) {
                    onResult!(transcript);
                  }
                }
              }
            } catch (_) {}
          };

          _recognition!['onerror'] = (event) {
            _isListening = false;
            try {
              final err = (event as js.JsObject)['error'] as String? ?? 'Unknown error';
              if (onError != null) onError!(err);
            } catch (_) {
              if (onError != null) onError!('Unknown error');
            }
          };

          _recognition!['onend'] = () {
            _isListening = false;
            if (onEnd != null) onEnd!();
          };
        }
      }
    } catch (_) {
      _supported = false;
    }
  }

  bool get isSupported => _supported;
  bool get isListening => _isListening;

  void start() {
    if (!_supported || _recognition == null) {
      if (onError != null) onError!('Speech recognition not supported. Use Chrome or Edge.');
      return;
    }
    if (_isListening) return;
    _isListening = true;
    try {
      _recognition!['lang'] = 'en-US';
      _recognition!.callMethod('start');
    } catch (e) {
      _isListening = false;
      if (onError != null) onError!('Failed to start: $e');
    }
  }

  void stop() {
    if (!_isListening || _recognition == null) return;
    _isListening = false;
    try {
      _recognition!.callMethod('stop');
    } catch (_) {}
  }
}
