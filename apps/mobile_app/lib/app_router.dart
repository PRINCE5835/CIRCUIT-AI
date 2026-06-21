import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import 'features/splash/presentation/splash_screen.dart';
import 'features/onboarding/presentation/onboarding_screen.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/auth/presentation/screens/register_screen.dart';
import 'features/auth/presentation/screens/forgot_password_screen.dart';
import 'features/home/presentation/screens/home_screen.dart';
import 'features/home/presentation/widgets/app_shell.dart';
import 'features/voice/presentation/screens/voice_screen.dart';
import 'features/circuit/generation/presentation/screens/circuit_generation_screen.dart';
import 'features/circuit/learning/presentation/screens/circuit_learning_screen.dart';
import 'features/repair/presentation/screens/repair_assistant_screen.dart';
import 'features/verification/presentation/screens/breadboard_verification_screen.dart';
import 'features/marketplace/presentation/screens/marketplace_screen.dart';
import 'features/project/presentation/screens/project_history_screen.dart';
import 'features/cost/presentation/screens/cost_estimation_screen.dart';
import 'features/safety/presentation/screens/safety_validation_screen.dart';
import 'features/profile/presentation/screens/profile_screen.dart';
import 'features/settings/presentation/screens/settings_screen.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: RoutePaths.splash,
    debugLogDiagnostics: AppConfig.isDebug,
    routes: [
      GoRoute(
        path: RoutePaths.splash,
        name: RouteNames.splash,
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: RoutePaths.onboarding,
        name: RouteNames.onboarding,
        builder: (context, state) => const OnboardingScreen(),
      ),
      GoRoute(
        path: RoutePaths.login,
        name: RouteNames.login,
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: RoutePaths.register,
        name: RouteNames.register,
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: RoutePaths.forgotPassword,
        name: RouteNames.forgotPassword,
        builder: (context, state) => const ForgotPasswordScreen(),
      ),
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => AppShell(child: child),
        routes: [
          GoRoute(
            path: RoutePaths.home,
            name: RouteNames.home,
            builder: (context, state) => const HomeScreen(),
          ),
          GoRoute(
            path: RoutePaths.voice,
            name: RouteNames.voice,
            builder: (context, state) => const VoiceScreen(),
          ),
          GoRoute(
            path: RoutePaths.circuitGeneration,
            name: RouteNames.circuitGeneration,
            builder: (context, state) => const CircuitGenerationScreen(),
          ),
          GoRoute(
            path: RoutePaths.circuitLearning,
            name: RouteNames.circuitLearning,
            builder: (context, state) => const CircuitLearningScreen(),
          ),
          GoRoute(
            path: RoutePaths.repairAssistant,
            name: RouteNames.repairAssistant,
            builder: (context, state) => const RepairAssistantScreen(),
          ),
          GoRoute(
            path: RoutePaths.breadboardVerification,
            name: RouteNames.breadboardVerification,
            builder: (context, state) => const BreadboardVerificationScreen(),
          ),
          GoRoute(
            path: RoutePaths.componentDetection,
            name: RouteNames.componentDetection,
            builder: (context, state) => const BreadboardVerificationScreen(),
          ),
          GoRoute(
            path: RoutePaths.marketplace,
            name: RouteNames.marketplace,
            builder: (context, state) => const MarketplaceScreen(),
          ),
          GoRoute(
            path: RoutePaths.projectHistory,
            name: RouteNames.projectHistory,
            builder: (context, state) => const ProjectHistoryScreen(),
          ),
          GoRoute(
            path: RoutePaths.costEstimation,
            name: RouteNames.costEstimation,
            builder: (context, state) => const CostEstimationScreen(),
          ),
          GoRoute(
            path: RoutePaths.safetyValidation,
            name: RouteNames.safetyValidation,
            builder: (context, state) => const SafetyValidationScreen(),
          ),
          GoRoute(
            path: RoutePaths.profile,
            name: RouteNames.profile,
            builder: (context, state) => const ProfileScreen(),
          ),
          GoRoute(
            path: RoutePaths.settings,
            name: RouteNames.settings,
            builder: (context, state) => const SettingsScreen(),
          ),
        ],
      ),
    ],
  );
});
