import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class LocalStorage {
  LocalStorage._();

  static late final SharedPreferences _prefs;

  static void init(SharedPreferences prefs) {
    _prefs = prefs;
  }

  static String? getString(String key) => _prefs.getString(key);

  static Future<void> setString(String key, String value) => _prefs.setString(key, value);

  static bool? getBool(String key) => _prefs.getBool(key);

  static Future<void> setBool(String key, bool value) => _prefs.setBool(key, value);

  static int? getInt(String key) => _prefs.getInt(key);

  static Future<void> setInt(String key, int value) => _prefs.setInt(key, value);

  static double? getDouble(String key) => _prefs.getDouble(key);

  static Future<void> setDouble(String key, double value) => _prefs.setDouble(key, value);

  static Map<String, dynamic>? getJson(String key) {
    final raw = _prefs.getString(key);
    if (raw == null) return null;
    return jsonDecode(raw) as Map<String, dynamic>;
  }

  static Future<void> setJson(String key, Map<String, dynamic> value) {
    return _prefs.setString(key, jsonEncode(value));
  }

  static Future<void> remove(String key) => _prefs.remove(key);

  static Future<void> clear() => _prefs.clear();
}
