import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class AppChip extends StatelessWidget {
  final String label;
  final IconData? icon;
  final Color? color;
  final bool isSelected;
  final bool isSmall;
  final VoidCallback? onTap;

  const AppChip({
    super.key,
    required this.label,
    this.icon,
    this.color,
    this.isSelected = false,
    this.isSmall = false,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final col = color ?? DSColors.circuitCyan;

    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: 200.ms,
        padding: EdgeInsets.symmetric(
          horizontal: isSmall ? 12 : 16,
          vertical: isSmall ? 6 : 10,
        ),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(isSmall ? 8 : 10),
          color: isSelected ? col.withValues(alpha: 0.15) : (isDark ? DSColors.glassMedium : DSColors.glassDarkMedium),
          border: Border.all(
            color: isSelected ? col.withValues(alpha: 0.5) : (isDark ? DSColors.white.withValues(alpha: 0.08) : DSColors.black.withValues(alpha: 0.08)),
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (icon != null) ...[
              Icon(icon, size: isSmall ? 14 : 16, color: isSelected ? col : (isDark ? DSColors.white : DSColors.grey700)),
              SizedBox(width: DSDimensions.s6),
            ],
            Text(label, style: TextStyle(
              fontSize: isSmall ? 12 : 13,
              fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
              color: isSelected ? col : (isDark ? DSColors.white : DSColors.grey700),
            )),
          ],
        ),
      ),
    );
  }
}

class AppBadge extends StatelessWidget {
  final String label;
  final Color? color;
  final double fontSize;

  const AppBadge({
    super.key,
    required this.label,
    this.color,
    this.fontSize = 11,
  });

  @override
  Widget build(BuildContext context) {
    final col = color ?? DSColors.circuitCyan;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(6),
        color: col.withValues(alpha: 0.12),
        border: Border.all(color: col.withValues(alpha: 0.3)),
      ),
      child: Text(label, style: TextStyle(
        fontSize: fontSize,
        fontWeight: FontWeight.w600,
        color: col,
      )),
    );
  }
}

class AppDivider extends StatelessWidget {
  final double? height;
  final Color? color;
  final double indent;
  final double endIndent;

  const AppDivider({
    super.key,
    this.height,
    this.color,
    this.indent = 0,
    this.endIndent = 0,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Divider(
      height: height ?? 1,
      color: color ?? (isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
      indent: indent,
      endIndent: endIndent,
    );
  }
}

class AppProgressBar extends StatelessWidget {
  final double value;
  final Color? color;
  final double height;
  final bool showLabel;

  const AppProgressBar({
    super.key,
    required this.value,
    this.color,
    this.height = 6,
    this.showLabel = false,
  });

  @override
  Widget build(BuildContext context) {
    final col = color ?? DSColors.circuitCyan;
    final clamped = value.clamp(0.0, 1.0);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(height / 2),
          child: LinearProgressIndicator(
            value: clamped,
            backgroundColor: col.withValues(alpha: 0.1),
            valueColor: AlwaysStoppedAnimation<Color>(col),
            minHeight: height,
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 4),
          Align(
            alignment: Alignment.centerRight,
            child: Text('${(clamped * 100).round()}%', style: TextStyle(
              fontSize: 12, fontWeight: FontWeight.w600, color: col,
            )),
          ),
        ],
      ],
    );
  }
}

class AppToggle extends StatelessWidget {
  final bool value;
  final ValueChanged<bool> onChanged;
  final String? label;

  const AppToggle({
    super.key,
    required this.value,
    required this.onChanged,
    this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (label != null) ...[
          Text(label!, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(width: 12),
        ],
        SizedBox(
          height: 32,
          child: Switch(
            value: value,
            onChanged: onChanged,
            activeTrackColor: DSColors.circuitCyan.withValues(alpha: 0.5),
            activeThumbColor: DSColors.circuitCyan,
          ),
        ),
      ],
    );
  }
}
