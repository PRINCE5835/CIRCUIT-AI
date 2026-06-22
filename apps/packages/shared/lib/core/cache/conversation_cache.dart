import 'dart:convert';
import 'package:breadboard_shared/core/cache/local_storage.dart';

class ConversationCache {
  ConversationCache._();

  static const _key = 'cached_conversations';

  static List<Map<String, dynamic>> getAll() {
    final raw = LocalStorage.getString(_key);
    if (raw == null) return [];
    try {
      final list = jsonDecode(raw) as List;
      return list.cast<Map<String, dynamic>>();
    } catch (_) {
      return [];
    }
  }

  static void save(List<Map<String, dynamic>> conversations) {
    LocalStorage.setString(_key, jsonEncode(conversations));
  }

  static void upsert(Map<String, dynamic> conversation) {
    final all = getAll();
    final idx = all.indexWhere((c) => c['id'] == conversation['id']);
    if (idx >= 0) {
      all[idx] = conversation;
    } else {
      all.insert(0, conversation);
    }
    save(all);
  }

  static void remove(int id) {
    final all = getAll();
    all.removeWhere((c) => c['id'] == id);
    save(all);
  }

  static void clear() {
    LocalStorage.remove(_key);
  }

  static List<Map<String, dynamic>> search(String query) {
    final q = query.toLowerCase();
    return getAll().where((c) {
      final title = (c['title'] as String? ?? '').toLowerCase();
      return title.contains(q);
    }).toList();
  }
}
