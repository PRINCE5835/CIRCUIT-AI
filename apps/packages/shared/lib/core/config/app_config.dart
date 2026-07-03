import 'package:flutter/foundation.dart' show kIsWeb;

class AppConfig {
  AppConfig._();

  static String appName = 'BreadBoard AI';
  static String apiBaseUrl = '';
  static String aiEngineUrl = '';
  static bool isDebug = true;

  static Future<void> load() async {
    const env = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');
    isDebug = env == 'development';

    const apiFromEnv = String.fromEnvironment('API_BASE_URL');
    const aiFromEnv = String.fromEnvironment('AI_ENGINE_URL');

    apiBaseUrl = apiFromEnv.isNotEmpty
        ? apiFromEnv
        : 'http://localhost:8000';

    aiEngineUrl = aiFromEnv.isNotEmpty
        ? aiFromEnv
        : 'http://localhost:8001';

    if (isDebug) {
      // ignore: avoid_print
      print('[AppConfig] API: $apiBaseUrl | AI: $aiEngineUrl');
    }
  }
}
