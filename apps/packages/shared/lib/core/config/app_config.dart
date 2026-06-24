import 'dart:io' show Platform;

class AppConfig {
  AppConfig._();

  static String appName = 'BreadBoard AI';
  static String apiBaseUrl = '';
  static String aiEngineUrl = '';
  static bool isDebug = true;

  static bool get _isAndroid {
    try {
      return Platform.isAndroid;
    } catch (_) {
      return false;
    }
  }

  static String _resolveUrl(String envKey, String androidUrl, String desktopUrl) {
    const fromEnv = String.fromEnvironment(envKey);
    if (fromEnv.isNotEmpty) return fromEnv;
    if (_isAndroid) return androidUrl;
    return desktopUrl;
  }

  static Future<void> load() async {
    const env = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');
    isDebug = env == 'development';

    apiBaseUrl = _resolveUrl('API_BASE_URL', 'http://10.0.2.2:8000', 'http://localhost:8000');
    aiEngineUrl = _resolveUrl('AI_ENGINE_URL', 'http://10.0.2.2:8001', 'http://localhost:8001');

    if (isDebug) {
      // ignore: avoid_print
      print('[AppConfig] API: $apiBaseUrl | AI: $aiEngineUrl');
    }
  }
}
