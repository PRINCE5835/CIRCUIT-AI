import 'package:flutter/material.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

enum AppIconButtonVariant { standard, filled, outlined, glass }

class AppIconButton extends StatelessWidget {
  final IconData icon;
  final String? tooltip;
  final AppIconButtonVariant variant;
  final double size;
  final Color? color;
  final VoidCallback? onPressed;

  const AppIconButton({
    super.key,
    required this.icon,
    this.tooltip,
    this.variant = AppIconButtonVariant.standard,
    this.size = 40,
    this.color,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final iconColor = color ?? (isDark ? DSColors.white : DSColors.grey800);
    final effectiveSize = size.clamp(32, 56).toDouble();

    Widget button;

    switch (variant) {
      case AppIconButtonVariant.standard:
        button = IconButton(
          icon: Icon(icon, size: effectiveSize * 0.5),
          tooltip: tooltip,
          onPressed: onPressed,
          color: iconColor,
          splashRadius: effectiveSize * 0.55,
        );
      case AppIconButtonVariant.filled:
        button = Container(
          width: effectiveSize,
          height: effectiveSize,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              colors: [DSColors.primary, Color(0xFF00B0FF)],
            ),
            boxShadow: [BoxShadow(color: DSColors.primary.withValues(alpha: 0.3), blurRadius: 8, spreadRadius: 1)],
          ),
          child: IconButton(
            icon: Icon(icon, size: effectiveSize * 0.5),
            tooltip: tooltip,
            onPressed: onPressed,
            color: DSColors.white,
            splashRadius: effectiveSize * 0.55,
          ),
        );
      case AppIconButtonVariant.outlined:
        button = Container(
          width: effectiveSize,
          height: effectiveSize,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: iconColor.withValues(alpha: 0.3), width: 1.5),
          ),
          child: IconButton(
            icon: Icon(icon, size: effectiveSize * 0.5),
            tooltip: tooltip,
            onPressed: onPressed,
            color: iconColor,
            splashRadius: effectiveSize * 0.55,
          ),
        );
      case AppIconButtonVariant.glass:
        button = Container(
          width: effectiveSize,
          height: effectiveSize,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: isDark ? DSColors.glassMedium : DSColors.glassDarkMedium,
            border: Border.all(color: isDark ? DSColors.white.withValues(alpha: 0.08) : DSColors.black.withValues(alpha: 0.08)),
          ),
          child: IconButton(
            icon: Icon(icon, size: effectiveSize * 0.5),
            tooltip: tooltip,
            onPressed: onPressed,
            color: iconColor,
            splashRadius: effectiveSize * 0.55,
          ),
        );
    }

    return button;
  }
}
