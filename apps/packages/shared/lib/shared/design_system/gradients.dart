import 'dart:ui';
import 'package:flutter/painting.dart';
import 'colors.dart';

abstract class DSGradients {
  DSGradients._();

  // ── Brand Gradients (Neon Aurora) ─────────────────────────
  static const primaryGradient = LinearGradient(
    colors: [Color(0xFF00F0FF), Color(0xFFB847FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const secondaryGradient = LinearGradient(
    colors: [Color(0xFFB847FF), Color(0xFF00F0FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const tertiaryGradient = LinearGradient(
    colors: [Color(0xFFFFB347), Color(0xFFFF3D71)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ── Circuit Gradients ─────────────────────────────────────
  static const circuitCyanGradient = LinearGradient(
    colors: [Color(0xFF00F0FF), Color(0xFF00FFFF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const neonVioletGradient = LinearGradient(
    colors: [Color(0xFFB847FF), Color(0xFFCC66FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const amberGradient = LinearGradient(
    colors: [Color(0xFFFFB347), Color(0xFFFFCC66)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ── Surface Gradients ─────────────────────────────────────
  static const darkSurfaceGradient = LinearGradient(
    colors: [Color(0xFF0A0F1A), Color(0xFF161C2B)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const lightSurfaceGradient = LinearGradient(
    colors: [Color(0xFFF5F7FF), Color(0xFFFFFFFF)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  // ── Glow Gradients ────────────────────────────────────────
  static const cyanGlow = RadialGradient(
    colors: [Color(0x6600F0FF), Color(0x0000F0FF)],
    radius: 1.0,
  );

  static const violetGlow = RadialGradient(
    colors: [Color(0x33B847FF), Color(0x00B847FF)],
    radius: 1.2,
  );

  // ── Status Gradients ──────────────────────────────────────
  static const safeGradient = LinearGradient(
    colors: [Color(0xFF39FF14), Color(0xFF66FF33)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const warningGradient = LinearGradient(
    colors: [Color(0xFFFFB347), Color(0xFFFFCC66)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const dangerGradient = LinearGradient(
    colors: [Color(0xFFFF3D71), Color(0xFFFF6B9D)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ── Helper ────────────────────────────────────────────────
  static LinearGradient shimmerGradient(Brightness brightness) => LinearGradient(
    colors: brightness == Brightness.dark
        ? [const Color(0xFF121826), const Color(0xFF232B42), const Color(0xFF121826)]
        : [const Color(0xFFE0E0E0), const Color(0xFFF5F5F5), const Color(0xFFE0E0E0)],
    stops: const [0.0, 0.5, 1.0],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
