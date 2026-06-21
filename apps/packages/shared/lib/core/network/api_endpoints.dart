abstract class ApiEndpoints {
  ApiEndpoints._();

  // Auth
  static const String login = '/v1/auth/login';
  static const String register = '/v1/auth/register';
  static const String refreshToken = '/v1/auth/refresh';
  static const String forgotPassword = '/v1/auth/forgot-password';
  static const String resetPassword = '/v1/auth/reset-password';

  // Users
  static const String users = '/v1/users';
  static const String profile = '/v1/users/me';

  // Projects
  static const String projects = '/v1/projects';

  // Circuits (CRUD)
  static const String circuits = '/v1/circuits';

  // Components
  static const String components = '/v1/components';

  // Marketplace
  static const String marketplace = '/v1/marketplace';

  // AI (via backend proxy)
  static const String aiHealth = '/v1/ai/health';
  static const String aiChat = '/v1/ai/chat';
  static const String aiGenerate = '/v1/ai/generate';
  static const String aiCircuitGenerate = '/v1/ai/circuit/generate';
  static const String aiSpeechStt = '/v1/ai/speech/stt';
  static const String aiSpeechTts = '/v1/ai/speech/tts';
  static const String aiVisionDetect = '/v1/ai/vision/detect';
  static const String aiCostEstimate = '/v1/ai/cost/estimate';

  // Health
  static const String health = '/health';
}
