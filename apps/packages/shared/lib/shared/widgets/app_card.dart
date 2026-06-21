import 'package:flutter/material.dart';
import '../design_system/dimensions.dart';
import '../design_system/colors.dart';

enum AppCardVariant { elevated, outlined, glass }

class AppCard extends StatelessWidget {
  final Widget child;
  final AppCardVariant variant;
  final EdgeInsetsGeometry? padding;
  final double? elevation;
  final Color? color;
  final BorderRadius? borderRadius;
  final VoidCallback? onTap;
  final Color? borderColor;
  final List<BoxShadow>? boxShadow;

  const AppCard({
    super.key,
    required this.child,
    this.variant = AppCardVariant.elevated,
    this.padding,
    this.elevation,
    this.color,
    this.borderRadius,
    this.onTap,
    this.borderColor,
    this.boxShadow,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final radius = borderRadius ?? BorderRadius.circular(DSDimensions.cardRadius);

    final card = Container(
      decoration: BoxDecoration(
        borderRadius: radius,
        color: color ?? _defaultColor(theme, isDark),
        border: Border.all(
          color: borderColor ?? _defaultBorderColor(theme, isDark),
          width: variant == AppCardVariant.outlined ? 1.0 : 0.5,
        ),
        gradient: variant == AppCardVariant.glass
            ? LinearGradient(
                colors: [
                  (isDark ? DSColors.white : DSColors.black).withValues(alpha: isDark ? 0.08 : 0.03),
                  (isDark ? DSColors.white : DSColors.black).withValues(alpha: isDark ? 0.03 : 0.01),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              )
            : null,
        boxShadow: boxShadow ?? _defaultShadow(theme, isDark),
      ),
      child: ClipRRect(
        borderRadius: radius,
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onTap,
            borderRadius: radius,
            child: Padding(
              padding: padding ?? EdgeInsets.all(variant == AppCardVariant.glass ? DSDimensions.s20 : DSDimensions.s16),
              child: child,
            ),
          ),
        ),
      ),
    );

    return card;
  }

  Color _defaultColor(ThemeData theme, bool isDark) => switch (variant) {
    AppCardVariant.elevated => theme.colorScheme.surface,
    AppCardVariant.outlined => Colors.transparent,
    AppCardVariant.glass => Colors.transparent,
  };

  Color _defaultBorderColor(ThemeData theme, bool isDark) => switch (variant) {
    AppCardVariant.elevated => isDark
        ? DSColors.white.withValues(alpha: 0.06)
        : DSColors.black.withValues(alpha: 0.06),
    AppCardVariant.outlined => theme.colorScheme.outline.withValues(alpha: 0.5),
    AppCardVariant.glass => isDark
        ? DSColors.white.withValues(alpha: 0.10)
        : DSColors.black.withValues(alpha: 0.06),
  };

  List<BoxShadow>? _defaultShadow(ThemeData theme, bool isDark) => switch (variant) {
    AppCardVariant.elevated => [
      BoxShadow(
        color: isDark ? Colors.black.withValues(alpha: 0.3) : Colors.black.withValues(alpha: 0.08),
        blurRadius: 12,
        offset: const Offset(0, 2),
      ),
    ],
    _ => null,
  };
}
