import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

Widget wrapWithProviders(Widget child) {
  return ProviderScope(child: MaterialApp(home: child));
}

Widget wrapWithRouter(Widget child) {
  final router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(path: '/', builder: (_, __) => child),
      GoRoute(path: '/login', builder: (_, __) => const Scaffold(body: Text('Login'))),
    ],
  );
  return ProviderScope(child: MaterialApp.router(routerConfig: router));
}
