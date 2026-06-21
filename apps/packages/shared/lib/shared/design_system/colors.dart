import 'package:flutter/material.dart';

abstract class DSColors {
  DSColors._();

  // ── Neon Aurora Palette ────────────────────────────────────
  static const primary = Color(0xFF00F0FF);
  static const onPrimary = Color(0xFF001F29);
  static const primaryContainer = Color(0xFF004D66);
  static const onPrimaryContainer = Color(0xFFB8F0FF);
  static const primaryFixed = Color(0xFFB8F0FF);
  static const onPrimaryFixed = Color(0xFF001F29);
  static const primaryFixedDim = Color(0xFF00E5FF);
  static const onPrimaryFixedVariant = Color(0xFF003D4D);

  static const secondary = Color(0xFFB847FF);
  static const onSecondary = Color(0xFF1F0033);
  static const secondaryContainer = Color(0xFF4A0080);
  static const onSecondaryContainer = Color(0xFFE6CCFF);
  static const secondaryFixed = Color(0xFFE6CCFF);
  static const onSecondaryFixed = Color(0xFF1F0033);
  static const secondaryFixedDim = Color(0xFFCC99FF);
  static const onSecondaryFixedVariant = Color(0xFF3D0066);

  static const tertiary = Color(0xFFFFB347);
  static const onTertiary = Color(0xFF2E1A00);
  static const tertiaryContainer = Color(0xFF4D2E00);
  static const onTertiaryContainer = Color(0xFFFFD699);

  static const success = Color(0xFF39FF14);
  static const onSuccess = Color(0xFF002600);
  static const error = Color(0xFFFF3D71);
  static const onError = Color(0xFF2D0015);

  // ── Surfaces ──────────────────────────────────────────────
  static const surfaceLight = Color(0xFFF5F7FF);
  static const surfaceLightHigh = Color(0xFFFFFFFF);
  static const surfaceLightCard = Color(0xFFFFFFFF);
  static const surfaceLightVariant = Color(0xFFE8ECF8);

  static const surfaceDark = Color(0xFF0A0F1A);
  static const surfaceDarkHigh = Color(0xFF161C2B);
  static const surfaceDarkCard = Color(0xFF121826);
  static const surfaceDarkElevated = Color(0xFF1A2235);
  static const surfaceDarkVariant = Color(0xFF232B42);

  // ── Electronics Theme Accents ─────────────────────────────
  static const circuitCyan = Color(0xFF00F0FF);
  static const circuitCyanGlow = Color(0xFF00FFFF);
  static const circuitCyanDim = Color(0xFF00B8CC);

  static const neonViolet = Color(0xFFB847FF);
  static const neonVioletGlow = Color(0xFFCC66FF);
  static const neonVioletDim = Color(0xFF9933CC);

  static const warmAmber = Color(0xFFFFB347);
  static const warmAmberGlow = Color(0xFFFFCC66);
  static const warmAmberDim = Color(0xFFCC8800);

  static const neonGreen = Color(0xFF39FF14);
  static const neonCoral = Color(0xFFFF3D71);

  // ── Component Detection Colors ────────────────────────────
  static const resistor = Color(0xFFE53935);
  static const capacitor = Color(0xFF1E88E5);
  static const inductor = Color(0xFF43A047);
  static const diode = Color(0xFFFB8C00);
  static const transistor = Color(0xFF8E24AA);
  static const ic = Color(0xFF00ACC1);
  static const led = Color(0xFFE53935);

  // ── Safety Status ─────────────────────────────────────────
  static const safe = Color(0xFF39FF14);
  static const safeLight = Color(0xFF66FF33);
  static const warning = Color(0xFFFFB347);
  static const warningLight = Color(0xFFFFCC66);
  static const danger = Color(0xFFFF3D71);
  static const dangerLight = Color(0xFFFF6B9D);
  static const critical = Color(0xFFD50000);

  // ── Glass / Frost Properties ──────────────────────────────
  static const glassLight = Color(0x19FFFFFF);
  static const glassMedium = Color(0x33FFFFFF);
  static const glassHeavy = Color(0x4DFFFFFF);
  static const glassDarkLight = Color(0x0A000000);
  static const glassDarkMedium = Color(0x1A000000);
  static const glassDarkHeavy = Color(0x33000000);

  // ── Neutral Palette ───────────────────────────────────────
  static const white = Color(0xFFFFFFFF);
  static const black = Color(0xFF000000);

  static const grey50 = Color(0xFFF5F5F5);
  static const grey100 = Color(0xFFE8E8ED);
  static const grey200 = Color(0xFFD0D0D7);
  static const grey300 = Color(0xFFB0B0BA);
  static const grey400 = Color(0xFF90909E);
  static const grey500 = Color(0xFF6E6E7A);
  static const grey600 = Color(0xFF52525C);
  static const grey700 = Color(0xFF3A3A42);
  static const grey800 = Color(0xFF24242A);
  static const grey900 = Color(0xFF141417);

  // ── Contextual Helpers ────────────────────────────────────
  static Color surface(BuildContext context) =>
      Theme.of(context).brightness == Brightness.dark ? surfaceDark : surfaceLight;

  static Color surfaceCard(BuildContext context) =>
      Theme.of(context).brightness == Brightness.dark ? surfaceDarkCard : surfaceLightCard;

  static Color surfaceElevated(BuildContext context) =>
      Theme.of(context).brightness == Brightness.dark ? surfaceDarkElevated : surfaceLightHigh;

  static Color onSurface(BuildContext context) =>
      Theme.of(context).brightness == Brightness.dark ? white : grey900;

  static Color onSurfaceVariant(BuildContext context) =>
      Theme.of(context).brightness == Brightness.dark ? grey300 : grey600;
}
