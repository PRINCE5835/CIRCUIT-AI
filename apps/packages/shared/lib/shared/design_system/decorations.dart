import 'package:flutter/material.dart';
import 'colors.dart';
import 'gradients.dart';

abstract class DSDecorations {
  DSDecorations._();

  // ── Glassmorphism ─────────────────────────────────────────
  static BoxDecoration glass({
    double blur = 20,
    double opacity = 0.15,
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
    Color? tint,
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      color: (tint ?? DSColors.white).withValues(alpha: opacity),
      border: Border.all(
        color: DSColors.white.withValues(alpha: 0.12),
        width: 0.5,
      ),
    );
  }

  static BoxDecoration glassDark({
    double blur = 20,
    double opacity = 0.10,
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
    Color? tint,
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      color: (tint ?? DSColors.white).withValues(alpha: opacity),
      border: Border.all(
        color: DSColors.white.withValues(alpha: 0.06),
        width: 0.5,
      ),
    );
  }

  // ── Glow Border ───────────────────────────────────────────
  static BoxDecoration glowBorder({
    required Color glowColor,
    double glowWidth = 1.5,
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
    Color? backgroundColor,
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      color: backgroundColor,
      border: Border.all(color: glowColor, width: glowWidth),
      boxShadow: [
        BoxShadow(
          color: glowColor.withValues(alpha: 0.3),
          blurRadius: 8,
          spreadRadius: 1,
        ),
      ],
    );
  }

  // ── Gradient Surface ──────────────────────────────────────
  static BoxDecoration gradientSurface({
    required Gradient gradient,
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
    List<BoxShadow>? shadows,
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      gradient: gradient,
      boxShadow: shadows,
    );
  }

  // ── Circuit Card (Dark Theme) ─────────────────────────────
  static BoxDecoration circuitCard({
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
    bool glowing = false,
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      gradient: const LinearGradient(
        colors: [Color(0xFF1C2333), Color(0xFF232B3F)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
      border: Border.all(
        color: Colors.white.withValues(alpha: 0.06),
        width: 1,
      ),
      boxShadow: [
        if (glowing)
          BoxShadow(
            color: DSColors.circuitCyan.withValues(alpha: 0.15),
            blurRadius: 20,
            spreadRadius: 2,
          ),
        const BoxShadow(
          color: Color(0x33000000),
          blurRadius: 12,
          offset: Offset(0, 4),
        ),
      ],
    );
  }

  // ── Light Card ────────────────────────────────────────────
  static BoxDecoration lightCard({
    BorderRadiusGeometry borderRadius = const BorderRadius.all(Radius.circular(16)),
  }) {
    return BoxDecoration(
      borderRadius: borderRadius,
      color: DSColors.white,
      border: Border.all(
        color: Colors.black.withValues(alpha: 0.06),
        width: 1,
      ),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.06),
          blurRadius: 12,
          offset: const Offset(0, 2),
        ),
      ],
    );
  }

  // ── Input Decoration ──────────────────────────────────────
  static BoxDecoration inputField({
    required BuildContext context,
    bool isFocused = false,
    bool hasError = false,
  }) {
    final brightness = Theme.of(context).brightness;
    final isDark = brightness == Brightness.dark;

    Color borderColor;
    if (hasError) {
      borderColor = DSColors.danger;
    } else if (isFocused) {
      borderColor = DSColors.circuitCyan;
    } else {
      borderColor = isDark ? Colors.white.withValues(alpha: 0.12) : Colors.black.withValues(alpha: 0.12);
    }

    return BoxDecoration(
      borderRadius: BorderRadius.circular(12),
      color: isDark ? const Color(0xFF1C2333) : const Color(0xFFF5F5F5),
      border: Border.all(color: borderColor, width: isFocused ? 1.5 : 1),
    );
  }
}
