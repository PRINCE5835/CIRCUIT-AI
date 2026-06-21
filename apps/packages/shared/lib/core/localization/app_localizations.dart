import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'app_localizations_en.dart';
import 'app_localizations_hi.dart';
import 'app_localizations_raj.dart';

class AppLocalizations {
  final Locale locale;
  late final Map<String, String> _strings;

  AppLocalizations(this.locale) {
    _strings = _loadMap(locale.languageCode);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();

  static const List<Locale> supportedLocales = [
    Locale('en'),
    Locale('hi'),
    Locale('raj'),
  ];

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  Map<String, String> _loadMap(String code) {
    switch (code) {
      case 'hi':
        return AppLocalizationsHi.strings;
      case 'raj':
        return AppLocalizationsRaj.strings;
      default:
        return AppLocalizationsEn.strings;
    }
  }

  String get appName => _strings['appName'] ?? 'BreadBoard AI';
  String get appTagline => _strings['appTagline'] ?? '';
  String get login => _strings['login'] ?? 'Login';
  String get register => _strings['register'] ?? 'Register';
  String get logout => _strings['logout'] ?? 'Logout';
  String get email => _strings['email'] ?? 'Email';
  String get password => _strings['password'] ?? 'Password';
  String get confirmPassword => _strings['confirmPassword'] ?? 'Confirm Password';
  String get forgotPassword => _strings['forgotPassword'] ?? 'Forgot Password';
  String get home => _strings['home'] ?? 'Home';
  String get voice => _strings['voice'] ?? 'Voice';
  String get circuits => _strings['circuits'] ?? 'Circuits';
  String get marketplace => _strings['marketplace'] ?? 'Marketplace';
  String get profile => _strings['profile'] ?? 'Profile';
  String get settings => _strings['settings'] ?? 'Settings';
  String get search => _strings['search'] ?? 'Search';
  String get cancel => _strings['cancel'] ?? 'Cancel';
  String get save => _strings['save'] ?? 'Save';
  String get delete => _strings['delete'] ?? 'Delete';
  String get edit => _strings['edit'] ?? 'Edit';
  String get submit => _strings['submit'] ?? 'Submit';
  String get loading => _strings['loading'] ?? 'Loading...';
  String get errorOccurred => _strings['errorOccurred'] ?? 'An error occurred';
  String get retry => _strings['retry'] ?? 'Retry';
  String get noInternet => _strings['noInternet'] ?? 'No internet connection';
  String get darkMode => _strings['darkMode'] ?? 'Dark Mode';
  String get lightMode => _strings['lightMode'] ?? 'Light Mode';
  String get systemMode => _strings['systemMode'] ?? 'System Mode';
  String get language => _strings['language'] ?? 'Language';
  String get english => _strings['english'] ?? 'English';
  String get hindi => _strings['hindi'] ?? 'हिन्दी';
  String get rajasthani => _strings['rajasthani'] ?? 'राजस्थानी';
  String get circuitGeneration => _strings['circuitGeneration'] ?? 'Circuit Generation';
  String get circuitLearning => _strings['circuitLearning'] ?? 'Circuit Learning';
  String get repairAssistant => _strings['repairAssistant'] ?? 'Repair Assistant';
  String get breadboardVerification => _strings['breadboardVerification'] ?? 'Breadboard Verification';
  String get componentDetection => _strings['componentDetection'] ?? 'Component Detection';
  String get projectHistory => _strings['projectHistory'] ?? 'Project History';
  String get costEstimation => _strings['costEstimation'] ?? 'Cost Estimation';
  String get safetyValidation => _strings['safetyValidation'] ?? 'Safety Validation';
  String get startVoiceInput => _strings['startVoiceInput'] ?? 'Start Voice Input';
  String get stopVoiceInput => _strings['stopVoiceInput'] ?? 'Stop Voice Input';
  String get speakNow => _strings['speakNow'] ?? 'Speak now...';
  String get processing => _strings['processing'] ?? 'Processing...';
  String get welcome => _strings['welcome'] ?? 'Welcome';
  String get getStarted => _strings['getStarted'] ?? 'Get Started';
  String get skip => _strings['skip'] ?? 'Skip';
  String get next => _strings['next'] ?? 'Next';
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'hi', 'raj'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(AppLocalizations(locale));
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
