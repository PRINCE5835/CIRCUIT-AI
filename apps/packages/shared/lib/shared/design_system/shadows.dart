import 'package:flutter/widgets.dart';
import 'colors.dart';

abstract class DSShadows {
  DSShadows._();

  // ── Subtle ────────────────────────────────────────────────
  static const subtle = BoxShadow(
    color: Color(0x08000000),
    blurRadius: 4,
    offset: Offset(0, 1),
  );

  static const subtleDark = BoxShadow(
    color: Color(0x33FFFFFF),
    blurRadius: 4,
    offset: Offset(0, 1),
  );

  // ── Medium ────────────────────────────────────────────────
  static const medium = BoxShadow(
    color: Color(0x12000000),
    blurRadius: 8,
    offset: Offset(0, 2),
  );

  static const mediumDark = BoxShadow(
    color: Color(0x44FFFFFF),
    blurRadius: 8,
    offset: Offset(0, 2),
  );

  // ── Elevated ──────────────────────────────────────────────
  static const elevated = BoxShadow(
    color: Color(0x1A000000),
    blurRadius: 16,
    offset: Offset(0, 4),
  );

  static const elevatedDark = BoxShadow(
    color: Color(0x55FFFFFF),
    blurRadius: 16,
    offset: Offset(0, 4),
  );

  // ── Glow Effects (Neon Aurora) ────────────────────────────
  static BoxShadow glowCyan({double radius = 12, double opacity = 0.4}) => BoxShadow(
    color: DSColors.circuitCyan.withValues(alpha: opacity),
    blurRadius: radius,
    spreadRadius: radius * 0.25,
  );

  static BoxShadow glowViolet({double radius = 12, double opacity = 0.4}) => BoxShadow(
    color: DSColors.neonViolet.withValues(alpha: opacity),
    blurRadius: radius,
    spreadRadius: radius * 0.25,
  );

  static BoxShadow glowAmber({double radius = 12, double opacity = 0.4}) => BoxShadow(
    color: DSColors.warmAmber.withValues(alpha: opacity),
    blurRadius: radius,
    spreadRadius: radius * 0.25,
  );

  static BoxShadow glowDanger({double radius = 12, double opacity = 0.4}) => BoxShadow(
    color: DSColors.danger.withValues(alpha: opacity),
    blurRadius: radius,
    spreadRadius: radius * 0.25,
  );

  // ── Card ───────────────────────────────────────────────────
  static const card = BoxShadow(
    color: Color(0x0F000000),
    blurRadius: 10,
    offset: Offset(0, 2),
  );

  static const cardDark = BoxShadow(
    color: Color(0x33FFFFFF),
    blurRadius: 10,
    offset: Offset(0, 2),
  );
}
