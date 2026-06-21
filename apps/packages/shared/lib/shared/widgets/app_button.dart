import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../design_system/dimensions.dart';
import '../design_system/typography.dart';

enum AppButtonVariant { primary, secondary, outlined, text, danger, tonal }
enum AppButtonSize { sm, md, lg }

class AppButton extends StatelessWidget {
  final String label;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final IconData? icon;
  final IconData? trailingIcon;
  final bool isLoading;
  final bool isDisabled;
  final bool isFullWidth;
  final double? width;
  final VoidCallback? onPressed;

  const AppButton({
    super.key,
    required this.label,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.md,
    this.icon,
    this.trailingIcon,
    this.isLoading = false,
    this.isDisabled = false,
    this.isFullWidth = true,
    this.width,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final effectiveOnPressed = (isLoading || isDisabled) ? null : onPressed;
    final s = _sizes[size]!;

    final widget = Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: effectiveOnPressed,
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        child: Container(
          height: s.height,
          padding: EdgeInsets.symmetric(horizontal: s.hPadding),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
            color: _bgColor(theme),
            border: _border(theme),
            gradient: _gradient,
            boxShadow: _shadows,
          ),
          child: _buildContent(s, theme),
        ),
      ),
    );

    final sized = isFullWidth
        ? SizedBox(width: double.infinity, child: widget)
        : width != null
            ? SizedBox(width: width, child: widget)
            : widget;

    return sized.animate().fadeIn(duration: 200.ms).scale(
      begin: const Offset(0.97, 0.97),
      duration: 200.ms,
    );
  }

  Widget _buildContent(_ButtonSize s, ThemeData theme) {
    final color = _fgColor(theme);
    final disabled = isDisabled || onPressed == null;

    if (isLoading) {
      return Center(
        child: SizedBox(
          height: s.iconSize,
          width: s.iconSize,
          child: CircularProgressIndicator(
            strokeWidth: 2.5,
            color: variant == AppButtonVariant.outlined || variant == AppButtonVariant.text
                ? theme.colorScheme.primary
                : Colors.white,
          ),
        ),
      );
    }

    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (icon != null) ...[
          Icon(icon, size: s.iconSize, color: disabled ? color.withValues(alpha: 0.5) : color),
          SizedBox(width: variant == AppButtonVariant.text ? DSDimensions.s4 : DSDimensions.s8),
        ],
        Text(
          label,
          style: DSTypography.buttonLabel(size: s.fontSize).copyWith(
            color: disabled ? color.withValues(alpha: 0.5) : color,
          ),
        ),
        if (trailingIcon != null) ...[
          SizedBox(width: DSDimensions.s8),
          Icon(trailingIcon, size: s.iconSize, color: disabled ? color.withValues(alpha: 0.5) : color),
        ],
      ],
    );
  }

  Color? _bgColor(ThemeData theme) => switch (variant) {
    AppButtonVariant.primary => theme.colorScheme.primary,
    AppButtonVariant.secondary => theme.colorScheme.secondary,
    AppButtonVariant.tonal => theme.colorScheme.secondaryContainer,
    AppButtonVariant.danger => theme.colorScheme.error,
    _ => null,
  };

  Border? _border(ThemeData theme) => switch (variant) {
    AppButtonVariant.outlined => Border.all(color: theme.colorScheme.outline),
    _ => null,
  };

  Gradient? get _gradient => null;

  List<BoxShadow>? get _shadows =>
      variant == AppButtonVariant.primary && !isDisabled
          ? [BoxShadow(
              color: const Color(0xFF00E676).withValues(alpha: 0.3),
              blurRadius: 12,
              spreadRadius: 0,
            )]
          : null;

  Color _fgColor(ThemeData theme) => switch (variant) {
    AppButtonVariant.primary => theme.colorScheme.onPrimary,
    AppButtonVariant.secondary => theme.colorScheme.onSecondary,
    AppButtonVariant.tonal => theme.colorScheme.onSecondaryContainer,
    AppButtonVariant.danger => theme.colorScheme.onError,
    AppButtonVariant.outlined => theme.colorScheme.primary,
    AppButtonVariant.text => theme.colorScheme.primary,
  };
}

class _ButtonSize {
  final double height;
  final double hPadding;
  final double fontSize;
  final double iconSize;
  const _ButtonSize({required this.height, required this.hPadding, required this.fontSize, required this.iconSize});
}

const _sizes = {
  AppButtonSize.sm: _ButtonSize(height: 36, hPadding: 16, fontSize: 13, iconSize: 16),
  AppButtonSize.md: _ButtonSize(height: 48, hPadding: 24, fontSize: 14, iconSize: 20),
  AppButtonSize.lg: _ButtonSize(height: 56, hPadding: 32, fontSize: 16, iconSize: 24),
};
