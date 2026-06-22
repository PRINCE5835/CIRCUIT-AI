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
  static const String aiChatStream = '/v1/ai/chat/stream';
  static const String aiGenerate = '/v1/ai/generate';
  static const String aiCircuitGenerate = '/v1/ai/circuit/generate';
  static const String aiSpeechStt = '/v1/ai/speech/stt';
  static const String aiSpeechTts = '/v1/ai/speech/tts';
  static const String aiVisionDetect = '/v1/ai/vision/detect';
  static const String aiCostEstimate = '/v1/ai/cost/estimate';

  // Health
  static const String health = '/health';

  // Wikipedia
  static const String wikiSearch = '/v1/wikipedia/search';
  static const String wikiComponentInfo = '/v1/wikipedia/component';
  static const String wikiComponentDetails = '/v1/wikipedia/component/{name}/details';

  static String wikiComponentInfoPath(String name) => '/v1/wikipedia/component/$name';
  static String wikiComponentDetailsPath(String name) => '/v1/wikipedia/component/$name/details';

  // Conversations
  static const String conversations = '/v1/conversations';
  static String conversation(int id) => '/v1/conversations/$id';
  static String conversationMessages(int id) => '/v1/conversations/$id/messages';
  static String conversationTitle(int id) => '/v1/conversations/$id/title';
  static String conversationSearch(String query) => '/v1/conversations?q=${Uri.encodeComponent(query)}';

  // Files / Upload
  static const String upload = '/v1/files/upload';

  // BOM
  static String projectBom(int id) => '/v1/projects/$id/bom';
  static String projectBomItem(int projectId, int itemId) => '/v1/projects/$projectId/bom/$itemId';

  // Safety Reports
  static const String safetyReports = '/v1/safety-reports';
  static String safetyReport(int id) => '/v1/safety-reports/$id';

  // Cost Estimates
  static const String costEstimates = '/v1/cost-estimates';
  static String costEstimate(int id) => '/v1/cost-estimates/$id';

  // Export
  static String exportProject(int id, {String format = 'json'}) => '/v1/projects/$id/export?fmt=$format';
}
