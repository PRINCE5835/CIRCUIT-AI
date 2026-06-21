import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

abstract class TokenStorage {
  Future<void> write(String key, String value);
  Future<String?> read(String key);
  Future<void> delete(String key);
}

class SecureTokenStorage implements TokenStorage {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  @override
  Future<void> write(String key, String value) => _storage.write(key: key, value: value);

  @override
  Future<String?> read(String key) => _storage.read(key: key);

  @override
  Future<void> delete(String key) => _storage.delete(key: key);
}

class PrefsTokenStorage implements TokenStorage {
  final SharedPreferences _prefs;
  PrefsTokenStorage(this._prefs);

  @override
  Future<void> write(String key, String value) async => await _prefs.setString(key, value);

  @override
  Future<String?> read(String key) async => _prefs.getString(key);

  @override
  Future<void> delete(String key) async => await _prefs.remove(key);
}

class AuthStorage {
  AuthStorage._();

  static late final TokenStorage _storage;

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';

  static void init(TokenStorage storage) {
    _storage = storage;
  }

  static Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _storage.write(_accessTokenKey, accessToken);
    await _storage.write(_refreshTokenKey, refreshToken);
  }

  static Future<String?> getAccessToken() async {
    return await _storage.read(_accessTokenKey);
  }

  static Future<String?> getRefreshToken() async {
    return await _storage.read(_refreshTokenKey);
  }

  static Future<void> clearTokens() async {
    await _storage.delete(_accessTokenKey);
    await _storage.delete(_refreshTokenKey);
  }

  static Future<bool> hasTokens() async {
    final access = await _storage.read(_accessTokenKey);
    return access != null && access.isNotEmpty;
  }
}
