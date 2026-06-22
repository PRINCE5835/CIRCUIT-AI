import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/core/router/route_paths.dart';
import 'package:breadboard_shared/core/router/route_names.dart';
import 'package:breadboard_shared/core/di/auth_providers.dart';
import 'screens/home_screen.dart';
import 'screens/voice_screen.dart';
import 'screens/circuit_screen.dart';
import 'screens/circuit_learning_screen.dart';
import 'screens/repair_assistant_screen.dart';
import 'screens/safety_validation_screen.dart';
import 'screens/cost_estimation_screen.dart';
import 'screens/breadboard_verification_screen.dart';
import 'screens/component_catalog_screen.dart';
import 'screens/project_history_screen.dart';
import 'screens/marketplace_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/forgot_password_screen.dart';
import 'screens/onboarding_screen.dart';
import 'screens/splash_screen.dart';
import 'widgets/web_shell.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();

Page _fadePage(Widget child) => CustomTransitionPage(
      child: child,
      transitionsBuilder: (context, animation, secondaryAnimation, child) =>
          FadeTransition(opacity: animation, child: child),
    );

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: RoutePaths.splash,
    redirect: (context, state) {
      final auth = ProviderScope.containerOf(context).read(authProvider);
      final isLoggedIn = auth.isAuthenticated;
      final location = state.matchedLocation;
      final isAuthRoute = location == RoutePaths.login ||
          location == RoutePaths.register ||
          location == RoutePaths.forgotPassword ||
          location == RoutePaths.onboarding ||
          location == RoutePaths.splash;

      if (!isLoggedIn && !isAuthRoute) return RoutePaths.login;
      if (isLoggedIn && isAuthRoute && location != RoutePaths.splash) {
        return RoutePaths.home;
      }
      return null;
    },
    routes: [
      GoRoute(
        path: RoutePaths.splash,
        name: RouteNames.splash,
        pageBuilder: (context, state) => _fadePage(const SplashScreen()),
      ),
      GoRoute(
        path: RoutePaths.onboarding,
        name: RouteNames.onboarding,
        pageBuilder: (context, state) => _fadePage(const OnboardingScreen()),
      ),
      GoRoute(
        path: RoutePaths.login,
        name: RouteNames.login,
        pageBuilder: (context, state) => _fadePage(const LoginScreen()),
      ),
      GoRoute(
        path: RoutePaths.register,
        name: RouteNames.register,
        pageBuilder: (context, state) => _fadePage(const RegisterScreen()),
      ),
      GoRoute(
        path: RoutePaths.forgotPassword,
        name: RouteNames.forgotPassword,
        pageBuilder: (context, state) => _fadePage(const ForgotPasswordScreen()),
      ),
      ShellRoute(
        builder: (context, state, child) => WebShell(child: child),
        routes: [
          GoRoute(
            path: RoutePaths.home,
            name: RouteNames.home,
            pageBuilder: (context, state) => _fadePage(const HomeScreen()),
          ),
          GoRoute(
            path: RoutePaths.voice,
            name: RouteNames.voice,
            pageBuilder: (context, state) => _fadePage(const VoiceScreen()),
          ),
          GoRoute(
            path: RoutePaths.circuitGeneration,
            name: RouteNames.circuitGeneration,
            pageBuilder: (context, state) => _fadePage(const CircuitScreen()),
          ),
          GoRoute(
            path: RoutePaths.circuitLearning,
            name: RouteNames.circuitLearning,
            pageBuilder: (context, state) => _fadePage(const CircuitLearningScreen()),
          ),
          GoRoute(
            path: RoutePaths.repairAssistant,
            name: RouteNames.repairAssistant,
            pageBuilder: (context, state) => _fadePage(const RepairAssistantScreen()),
          ),
          GoRoute(
            path: RoutePaths.breadboardVerification,
            name: RouteNames.breadboardVerification,
            pageBuilder: (context, state) => _fadePage(const BreadboardVerificationScreen()),
          ),
          GoRoute(
            path: RoutePaths.componentDetection,
            name: RouteNames.componentDetection,
            pageBuilder: (context, state) => _fadePage(const BreadboardVerificationScreen()),
          ),
          GoRoute(
            path: RoutePaths.marketplace,
            name: RouteNames.marketplace,
            pageBuilder: (context, state) => _fadePage(const MarketplaceScreen()),
          ),
          GoRoute(
            path: RoutePaths.projectHistory,
            name: RouteNames.projectHistory,
            pageBuilder: (context, state) => _fadePage(const ProjectHistoryScreen()),
          ),
          GoRoute(
            path: RoutePaths.costEstimation,
            name: RouteNames.costEstimation,
            pageBuilder: (context, state) => _fadePage(const CostEstimationScreen()),
          ),
          GoRoute(
            path: RoutePaths.safetyValidation,
            name: RouteNames.safetyValidation,
            pageBuilder: (context, state) => _fadePage(const SafetyValidationScreen()),
          ),
          GoRoute(
            path: RoutePaths.componentCatalog,
            name: RouteNames.componentCatalog,
            pageBuilder: (context, state) => _fadePage(const ComponentCatalogScreen()),
          ),
          GoRoute(
            path: RoutePaths.profile,
            name: RouteNames.profile,
            pageBuilder: (context, state) => _fadePage(const ProfileScreen()),
          ),
          GoRoute(
            path: RoutePaths.settings,
            name: RouteNames.settings,
            pageBuilder: (context, state) => _fadePage(const SettingsScreen()),
          ),
        ],
      ),
    ],
  );
});
