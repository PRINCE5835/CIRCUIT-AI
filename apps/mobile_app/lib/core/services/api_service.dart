import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ApiService {
  static Dio get _dio => ApiClient.instance.dio;

  // ── Projects ───────────────────────────────────────────

  static Future<Map<String, dynamic>> getProjects({int skip = 0, int limit = 20}) async {
    final response =
        await _dio.get(ApiEndpoints.projects, queryParameters: {'skip': skip, 'limit': limit});
    return response.data;
  }

  static Future<Map<String, dynamic>> createProject(Map<String, dynamic> data) async {
    final response = await _dio.post(ApiEndpoints.projects, data: data);
    return response.data;
  }

  // ── Circuits ───────────────────────────────────────────

  static Future<Map<String, dynamic>> getCircuits({int skip = 0, int limit = 20}) async {
    final response =
        await _dio.get(ApiEndpoints.circuits, queryParameters: {'skip': skip, 'limit': limit});
    return response.data;
  }

  static Future<Map<String, dynamic>> createCircuit(Map<String, dynamic> data) async {
    final response = await _dio.post(ApiEndpoints.circuits, data: data);
    return response.data;
  }

  // ── AI ─────────────────────────────────────────────────

  static Future<Map<String, dynamic>> aiChat(List<Map<String, dynamic>> messages,
      {String? model}) async {
    final response = await _dio.post(
      ApiEndpoints.aiChat,
      data: {'messages': messages, if (model != null) 'model': model},
    );
    return response.data;
  }

  static Future<Map<String, dynamic>> aiGenerate(String prompt, {String? model}) async {
    final response = await _dio.post(
      ApiEndpoints.aiGenerate,
      data: {'prompt': prompt, if (model != null) 'model': model},
    );
    return response.data;
  }

  static Future<Map<String, dynamic>> aiGenerateCircuit(String description,
      {String? model}) async {
    final response = await _dio.post(
      ApiEndpoints.aiCircuitGenerate,
      data: {'description': description, if (model != null) 'model': model},
    );
    return response.data;
  }

  // ── User / Profile ─────────────────────────────────────

  static Future<Map<String, dynamic>> getProfile() async {
    final response = await _dio.get(ApiEndpoints.profile);
    return response.data;
  }

  static Future<void> updateProfile(Map<String, dynamic> data) async {
    await _dio.patch(ApiEndpoints.profile, data: data);
  }

  static Future<void> deleteAccount() async {
    await _dio.delete(ApiEndpoints.profile);
  }
}
