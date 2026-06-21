import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:breadboard_shared/core/theme/app_theme.dart';
import 'package:breadboard_shared/core/theme/theme_provider.dart';
import 'package:breadboard_shared/core/localization/app_localizations.dart';
import 'package:breadboard_shared/core/localization/locale_provider.dart';
import 'package:breadboard_shared/shared/widgets/responsive_layout.dart';
import 'bootstrap.dart';
import 'app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await bootstrap();
  runApp(const ProviderScope(child: BreadBoardWebApp()));
}

class BreadBoardWebApp extends ConsumerWidget {
  const BreadBoardWebApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    final themeMode = ref.watch(themeModeProvider);
    final locale = ref.watch(localeProvider);

    return ResponsiveLayout(
      child: MaterialApp.router(
        title: 'BreadBoard AI',
        debugShowCheckedModeBanner: false,
        locale: locale,
        supportedLocales: AppLocalizations.supportedLocales,
        localizationsDelegates: const [
          AppLocalizations.delegate,
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
        ],
        themeMode: themeMode,
        theme: AppTheme.light,
        darkTheme: AppTheme.dark,
        routerConfig: router,
      ),
    );
  }
}
