import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../core/constants/app_constants.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _traceController;
  late Animation<double> _traceAnimation;

  @override
  void initState() {
    super.initState();
    _traceController = AnimationController(
      vsync: this,
      duration: 2000.ms,
    );
    _traceAnimation = CurvedAnimation(
      parent: _traceController,
      curve: Curves.easeInOut,
    );
    _traceController.forward();
    _navigateAfterDelay();
  }

  @override
  void dispose() {
    _traceController.dispose();
    super.dispose();
  }

  Future<void> _navigateAfterDelay() async {
    await Future.delayed(const Duration(seconds: AppConstants.splashDurationSeconds));
    if (!mounted) return;
    await ref.read(authProvider.notifier).checkAuth();
    if (!mounted) return;
    final auth = ref.read(authProvider);
    if (auth.isAuthenticated) {
      context.go(RoutePaths.home);
    } else {
      final hasOnboarded = ref.read(authStateProvider);
      context.go(hasOnboarded ? RoutePaths.login : RoutePaths.onboarding);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final isMobile = MediaQuery.of(context).size.width < DSDimensions.tablet;
    final logoSize = isMobile ? 120.0 : 160.0;

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: isDark
              ? DSGradients.darkSurfaceGradient
              : DSGradients.lightSurfaceGradient,
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    width: logoSize,
                    height: logoSize,
                    child: AnimatedBuilder(
                      animation: _traceAnimation,
                      builder: (context, child) {
                        return CustomPaint(
                          size: Size(logoSize, logoSize),
                          painter: _CircuitLogoPainter(
                            color: DSColors.primary,
                            accentColor: isDark
                                ? DSColors.neonVioletGlow
                                : DSColors.neonViolet,
                            traceProgress: _traceAnimation.value,
                          ),
                        );
                      },
                    ),
                  ).animate().scale(
                    duration: 1200.ms,
                    curve: Curves.elasticOut,
                  ),
                  SizedBox(height: isMobile ? DSDimensions.s24 : DSDimensions.s32),
                  Text(
                    'BreadBoard AI',
                    style: (isMobile
                            ? theme.textTheme.displaySmall
                            : theme.textTheme.displayMedium)
                        ?.copyWith(
                      fontWeight: FontWeight.w800,
                      letterSpacing: -1,
                    ),
                  ).animate().fadeIn(duration: 800.ms).slideY(begin: 0.2),
                  SizedBox(height: isMobile ? DSDimensions.s8 : DSDimensions.s12),
                  Text(
                    'Build Circuits with Voice',
                    style: theme.textTheme.titleMedium?.copyWith(
                      color: theme.colorScheme.primary,
                      fontWeight: FontWeight.w600,
                    ),
                  ).animate().fadeIn(duration: 800.ms, delay: 400.ms),
                  SizedBox(height: isMobile ? DSDimensions.s40 : DSDimensions.s48),
                  const CircuitSpinner(size: 28)
                      .animate()
                      .fadeIn(duration: 600.ms, delay: 2000.ms),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _CircuitLogoPainter extends CustomPainter {
  final Color color;
  final Color accentColor;
  final double traceProgress;

  _CircuitLogoPainter({
    required this.color,
    required this.accentColor,
    required this.traceProgress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final r = size.width / 3;
    final extLength = r * 0.5;

    final glowPaint = Paint()
      ..color = color.withValues(alpha: 0.12)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 15);

    canvas.drawCircle(center, r + 10, glowPaint);

    final circlePaint = Paint()
      ..color = color
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    canvas.drawCircle(center, r, circlePaint);

    for (int i = 0; i < 4; i++) {
      final angle = i * pi / 2;
      final node = Offset(
        center.dx + r * cos(angle),
        center.dy + r * sin(angle),
      );

      final innerProgress = min(1.0, traceProgress * 2.0);
      final innerEnd = Offset.lerp(center, node, innerProgress)!;

      final tracePaint = Paint()
        ..color = i == 0 ? accentColor : color
        ..strokeWidth = i == 0 ? 2.5 : 2.0
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round;

      canvas.drawLine(center, innerEnd, tracePaint);

      if (traceProgress > 0.5) {
        final outerProgress = (traceProgress - 0.5) * 2.0;
        final extEnd = Offset(
          node.dx + extLength * cos(angle),
          node.dy + extLength * sin(angle),
        );
        final actualOuterEnd = Offset.lerp(node, extEnd, outerProgress)!;

        final extPaint = Paint()
          ..color = color.withValues(alpha: 0.7)
          ..strokeWidth = 2.0
          ..style = PaintingStyle.stroke
          ..strokeCap = StrokeCap.round;

        canvas.drawLine(node, actualOuterEnd, extPaint);
      }

      if (traceProgress > 0.45) {
        final dotPaint = Paint()..color = i == 0 ? accentColor : color;
        canvas.drawCircle(node, i == 0 ? 5 : 3.5, dotPaint);
      }
    }

    if (traceProgress > 0.1) {
      canvas.drawCircle(center, 4, Paint()..color = accentColor);
    }
  }

  @override
  bool shouldRepaint(_CircuitLogoPainter old) =>
      old.traceProgress != traceProgress;
}
