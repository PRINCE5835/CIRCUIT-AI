import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/core/router/route_paths.dart';
import 'package:breadboard_shared/core/router/route_names.dart';
import 'package:breadboard_shared/core/di/auth_providers.dart';
import 'screens/home_screen.dart';
import 'screens/voice_screen.dart';
import 'screens/circuit_screen.dart';
import 'screens/marketplace_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/splash_screen.dart';
import 'widgets/web_shell.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();

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
        builder: (context, state) => const SplashScreen(),
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
      ShellRoute(
        builder: (context, state, child) => WebShell(child: child),
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
            builder: (context, state) => const CircuitScreen(),
          ),
          GoRoute(
            path: RoutePaths.marketplace,
            name: RouteNames.marketplace,
            builder: (context, state) => const MarketplaceScreen(),
          ),
          GoRoute(
            path: RoutePaths.profile,
            name: RouteNames.profile,
            builder: (context, state) => const ProfileScreen(),
          ),
          GoRoute(
            path: RoutePaths.settings,
            name: RouteNames.settings,
            builder: (context, state) => const ProfileScreen(),
          ),
        ],
      ),
    ],
  );
});
