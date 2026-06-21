import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';
import '../../design_system/gradients.dart';
import '../../design_system/shadows.dart';

enum NeoButtonVariant {
  primary,
  secondary,
  tertiary,
  outline,
  ghost,
  danger,
  glass,
}

enum NeoButtonSize { sm, md, lg }

class NeoButton extends StatefulWidget {
  final String label;
  final NeoButtonVariant variant;
  final NeoButtonSize size;
  final IconData? icon;
  final IconData? trailingIcon;
  final bool isLoading;
  final bool isDisabled;
  final bool isFullWidth;
  final double? width;
  final VoidCallback? onPressed;

  const NeoButton({
    super.key,
    required this.label,
    this.variant = NeoButtonVariant.primary,
    this.size = NeoButtonSize.md,
    this.icon,
    this.trailingIcon,
    this.isLoading = false,
    this.isDisabled = false,
    this.isFullWidth = true,
    this.width,
    this.onPressed,
  });

  @override
  State<NeoButton> createState() => _NeoButtonState();
}

class _NeoButtonState extends State<NeoButton> with SingleTickerProviderStateMixin {
  bool _isHovered = false;
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: 1500.ms,
    )..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.04).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final effectiveOnPressed = (widget.isLoading || widget.isDisabled) ? null : widget.onPressed;
    final sizeConfig = _sizeConfig(widget.size);

    Widget button = AnimatedBuilder(
      animation: _pulseAnimation,
      builder: (context, child) {
        final shouldGlow = widget.variant == NeoButtonVariant.primary && !widget.isDisabled && !widget.isLoading;
        return Transform.scale(
          scale: shouldGlow ? _pulseAnimation.value : 1.0,
          child: child,
        );
      },
      child: _buildButton(context, sizeConfig, effectiveOnPressed),
    );

    if (widget.isFullWidth) {
      button = SizedBox(width: double.infinity, child: button);
    } else if (widget.width != null) {
      button = SizedBox(width: widget.width, child: button);
    }

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: button
          .animate(target: _isHovered ? 1 : 0)
          .scale(begin: const Offset(1, 1), end: const Offset(1.02, 1.02), duration: 200.ms)
          .fadeIn(duration: 300.ms),
    );
  }

  Widget _buildButton(BuildContext context, _SizeConfig s, VoidCallback? onPressed) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return switch (widget.variant) {
      NeoButtonVariant.primary => _glassPrimaryButton(s, onPressed, isDark),
      NeoButtonVariant.secondary => _glassSecondaryButton(s, onPressed, isDark),
      NeoButtonVariant.tertiary => _tertiaryButton(s, onPressed, isDark),
      NeoButtonVariant.outline => _outlineButton(s, onPressed, isDark),
      NeoButtonVariant.ghost => _ghostButton(s, onPressed, isDark),
      NeoButtonVariant.danger => _dangerButton(s, onPressed, isDark),
      NeoButtonVariant.glass => _glassButton(s, onPressed, isDark),
    };
  }

  Widget _glassPrimaryButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        gradient: DSGradients.primaryGradient,
        boxShadow: onPressed != null ? [DSShadows.glowCyan(radius: 16)] : null,
      ),
      child: _buildMaterial(onPressed, s, DSColors.white, Colors.black87),
    );
  }

  Widget _glassSecondaryButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        gradient: DSGradients.neonVioletGradient,
        boxShadow: onPressed != null ? [DSShadows.glowViolet(radius: 16)] : null,
      ),
      child: _buildMaterial(onPressed, s, DSColors.white, Colors.black87),
    );
  }

  Widget _tertiaryButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        gradient: DSGradients.amberGradient,
        boxShadow: onPressed != null ? [DSShadows.glowAmber(radius: 16)] : null,
      ),
      child: _buildMaterial(onPressed, s, Colors.black87, Colors.white),
    );
  }

  Widget _outlineButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        border: Border.all(
          color: isDark ? DSColors.circuitCyan : DSColors.primary,
          width: 1.5,
        ),
        color: Colors.transparent,
      ),
      child: _buildMaterial(
        onPressed, s,
        isDark ? DSColors.circuitCyan : DSColors.primary,
        isDark ? DSColors.circuitCyan.withValues(alpha: 0.5) : DSColors.primary.withValues(alpha: 0.5),
      ),
    );
  }

  Widget _ghostButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return SizedBox(
      height: s.height,
      child: _buildMaterial(
        onPressed, s,
        isDark ? DSColors.white : DSColors.grey800,
        isDark ? DSColors.white.withValues(alpha: 0.5) : DSColors.grey800.withValues(alpha: 0.5),
      ),
    );
  }

  Widget _dangerButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        gradient: DSGradients.dangerGradient,
        boxShadow: onPressed != null ? [DSShadows.glowDanger(radius: 16)] : null,
      ),
      child: _buildMaterial(onPressed, s, DSColors.white, Colors.white.withValues(alpha: 0.5)),
    );
  }

  Widget _glassButton(_SizeConfig s, VoidCallback? onPressed, bool isDark) {
    return Container(
      height: s.height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        color: isDark ? DSColors.glassMedium : DSColors.glassDarkMedium,
        border: Border.all(
          color: isDark ? DSColors.white.withValues(alpha: 0.08) : DSColors.black.withValues(alpha: 0.08),
        ),
      ),
      child: _buildMaterial(
        onPressed, s,
        isDark ? DSColors.white : DSColors.grey800,
        isDark ? DSColors.white.withValues(alpha: 0.5) : DSColors.grey800.withValues(alpha: 0.5),
      ),
    );
  }

  Widget _buildMaterial(VoidCallback? onPressed, _SizeConfig s, Color textColor, Color disabledTextColor) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: s.hPadding, vertical: 0),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (widget.isLoading)
                _loader(textColor, s)
              else ...[
                if (widget.icon != null) ...[
                  Icon(widget.icon, size: s.iconSize, color: onPressed == null ? disabledTextColor : textColor),
                  SizedBox(width: DSDimensions.btnIconGap),
                ],
                Text(
                  widget.label,
                  style: TextStyle(
                    fontSize: s.fontSize,
                    fontWeight: FontWeight.w600,
                    color: onPressed == null ? disabledTextColor : textColor,
                    letterSpacing: 0.3,
                  ),
                ),
                if (widget.trailingIcon != null) ...[
                  SizedBox(width: DSDimensions.btnIconGap),
                  Icon(widget.trailingIcon, size: s.iconSize, color: onPressed == null ? disabledTextColor : textColor),
                ],
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _loader(Color color, _SizeConfig s) => SizedBox(
    height: s.iconSize,
    width: s.iconSize,
    child: CircularProgressIndicator(
      strokeWidth: 2.5,
      color: color,
    ),
  );

  _SizeConfig _sizeConfig(NeoButtonSize size) => switch (size) {
    NeoButtonSize.sm => _SizeConfig(height: 36, hPadding: 16, fontSize: 13, iconSize: 16),
    NeoButtonSize.md => _SizeConfig(height: 48, hPadding: 24, fontSize: 14, iconSize: 20),
    NeoButtonSize.lg => _SizeConfig(height: 56, hPadding: 32, fontSize: 16, iconSize: 24),
  };
}

class _SizeConfig {
  final double height, hPadding, fontSize, iconSize;
  const _SizeConfig({
    required this.height,
    required this.hPadding,
    required this.fontSize,
    required this.iconSize,
  });
}
