// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:html' as html;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

Future<void> bootstrap() async {
  await AppConfig.load();
  ApiClient.init();
  final prefs = await SharedPreferences.getInstance();
  LocalStorage.init(prefs);
  AuthStorage.init(PrefsTokenStorage(prefs));
  _registerServiceWorker();
}

void _registerServiceWorker() {
  if (html.window.navigator.serviceWorker != null) {
    html.window.navigator.serviceWorker!.register('service_worker.js').then((reg) {
      reg.update();
    });
  }
}
