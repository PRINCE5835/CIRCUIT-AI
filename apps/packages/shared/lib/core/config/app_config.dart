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

  static Future<void> load() async {
    const env = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');
    isDebug = env == 'development';

    const apiFromEnv = String.fromEnvironment('API_BASE_URL');
    const aiFromEnv = String.fromEnvironment('AI_ENGINE_URL');

    apiBaseUrl = apiFromEnv.isNotEmpty
        ? apiFromEnv
        : _isAndroid ? 'http://10.0.2.2:8000' : 'http://localhost:8000';

    aiEngineUrl = aiFromEnv.isNotEmpty
        ? aiFromEnv
        : _isAndroid ? 'http://10.0.2.2:8001' : 'http://localhost:8001';

    if (isDebug) {
      // ignore: avoid_print
      print('[AppConfig] API: $apiBaseUrl | AI: $aiEngineUrl');
    }
  }
}
