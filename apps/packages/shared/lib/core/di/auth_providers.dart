import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../network/api_client.dart';
import '../network/api_endpoints.dart';
import '../security/auth_storage.dart';
import '../config/app_config.dart';

class AuthState {
  final bool isAuthenticated;
  final bool isLoading;
  final String? error;
  final Map<String, dynamic>? user;

  const AuthState({
    this.isAuthenticated = false,
    this.isLoading = false,
    this.error,
    this.user,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    bool? isLoading,
    String? error,
    Map<String, dynamic>? user,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      user: user ?? this.user,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(const AuthState());

  Future<void> checkAuth() async {
    final hasTokens = await AuthStorage.hasTokens();
    if (!hasTokens) return;

    final token = await AuthStorage.getAccessToken();
    if (token == null) return;

    ApiClient.instance.setAuthToken(token);
    try {
      await fetchProfile();
      state = state.copyWith(isAuthenticated: true);
    } catch (_) {
      await AuthStorage.clearTokens();
      ApiClient.instance.clearAuthToken();
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.login,
        data: {'email': email, 'password': password},
      );
      final data = response.data;
      await AuthStorage.saveTokens(
        accessToken: data['access_token'],
        refreshToken: data['refresh_token'],
      );
      ApiClient.instance.setAuthToken(data['access_token']);
      state = state.copyWith(isAuthenticated: true, isLoading: false);
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Login failed';
      state = state.copyWith(isLoading: false, error: msg);
      throw Exception(msg);
    } catch (e) {
      final msg = e.toString();
      state = state.copyWith(isLoading: false, error: msg);
      throw Exception(msg);
    }
  }

  Future<void> register(String email, String username, String password,
      {String? displayName}) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      await ApiClient.instance.dio.post(
        ApiEndpoints.register,
        data: {
          'email': email,
          'username': username,
          'password': password,
          if (displayName != null) 'display_name': displayName,
        },
      );
      state = state.copyWith(isLoading: false);
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Registration failed';
      state = state.copyWith(isLoading: false, error: msg);
      throw Exception(msg);
    } catch (e) {
      final msg = e.toString();
      state = state.copyWith(isLoading: false, error: msg);
      throw Exception(msg);
    }
  }

  Future<void> fetchProfile() async {
    try {
      final response = await ApiClient.instance.dio.get(ApiEndpoints.profile);
      state = state.copyWith(user: response.data);
    } catch (_) {}
  }

  Future<void> logout() async {
    await AuthStorage.clearTokens();
    ApiClient.instance.clearAuthToken();
    state = const AuthState();
  }
}

final authProvider =
    StateNotifierProvider<AuthNotifier, AuthState>((ref) => AuthNotifier());
