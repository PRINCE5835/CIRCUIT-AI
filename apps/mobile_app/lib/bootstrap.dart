import 'package:shared_preferences/shared_preferences.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

Future<void> bootstrap() async {
  await AppConfig.load();
  ApiClient.init();
  final prefs = await SharedPreferences.getInstance();
  LocalStorage.init(prefs);
  AuthStorage.init(PrefsTokenStorage(prefs));
}
