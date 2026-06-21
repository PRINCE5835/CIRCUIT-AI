import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';
import '../../design_system/gradients.dart';
import '../../design_system/shadows.dart';

class GlassCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final double height;
  final double? width;
  final VoidCallback? onTap;

  const GlassCard({
    super.key,
    required this.child,
    this.padding,
    this.height = 160,
    this.width,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final card = Container(
      height: height,
      width: width,
      padding: padding ?? const EdgeInsets.all(DSDimensions.cardPadding),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0x33FFFFFF), const Color(0x19FFFFFF)]
              : [const Color(0x19FFFFFF), const Color(0x0DFFFFFF)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(
          color: isDark ? DSColors.white.withValues(alpha: 0.08) : DSColors.white.withValues(alpha: 0.3),
          width: 0.5,
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: child,
    );

    if (onTap != null) {
      return GestureDetector(
        onTap: onTap,
        child: card,
      );
    }

    return card;
  }
}

class GlowCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final double height;
  final double? width;
  final Color glowColor;
  final double glowIntensity;
  final VoidCallback? onTap;

  const GlowCard({
    super.key,
    required this.child,
    this.padding,
    this.height = 160,
    this.width,
    this.glowColor = DSColors.circuitCyan,
    this.glowIntensity = 0.15,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final card = Container(
      height: height,
      width: width,
      padding: padding ?? const EdgeInsets.all(DSDimensions.cardPadding),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        color: isDark ? DSColors.surfaceDarkCard : DSColors.surfaceLightCard,
        border: Border.all(color: glowColor.withValues(alpha: 0.3), width: 1),
        boxShadow: [
          BoxShadow(
            color: glowColor.withValues(alpha: glowIntensity),
            blurRadius: 24,
            spreadRadius: 2,
          ),
          if (isDark) DSShadows.cardDark else DSShadows.card,
        ],
      ),
      child: child,
    );

    if (onTap != null) {
      return GestureDetector(onTap: onTap, child: card);
    }

    return card;
  }
}
