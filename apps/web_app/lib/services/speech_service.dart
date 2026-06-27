// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:js' as js;

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
    if (js.context.hasProperty('webkitSpeechRecognition') ||
        js.context.hasProperty('SpeechRecognition')) {
      _supported = true;
      final ctor = js.context.hasProperty('webkitSpeechRecognition')
          ? js.context['webkitSpeechRecognition']
          : js.context['SpeechRecognition'];
      _recognition = js.JsObject(ctor as js.JsFunction);
      _recognition!['lang'] = 'en-US';
      _recognition!['continuous'] = false;
      _recognition!['interimResults'] = false;

      _recognition!['onresult'] = (js.JsObject event) {
        final results = event['results'] as js.JsObject;
        if (results['length'] > 0) {
          final result = results[0] as js.JsObject;
          if (result['isFinal'] == true) {
            final transcript = result[0]['transcript'] as String? ?? '';
            if (transcript.isNotEmpty && onResult != null) {
              onResult!(transcript);
            }
          }
        }
      };

      _recognition!['onerror'] = (js.JsObject event) {
        final error = event['error'] as String? ?? 'Unknown error';
        _isListening = false;
        if (onError != null) onError!(error);
      };

      _recognition!['onend'] = () {
        _isListening = false;
        if (onEnd != null) onEnd!();
      };
    }
  }

  bool get isSupported => _supported;
  bool get isListening => _isListening;

  void start() {
    if (!_supported || _recognition == null) {
      if (onError != null) onError!('Speech recognition not supported in this browser');
      return;
    }
    if (_isListening) return;
    _isListening = true;
    _recognition!['lang'] = 'en-US';
    _recognition!.callMethod('start');
  }

  void stop() {
    if (!_isListening || _recognition == null) return;
    _isListening = false;
    _recognition!.callMethod('stop');
  }
}
