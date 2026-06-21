import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

abstract class DSTypography {
  DSTypography._();

  static const String displayFont = 'Inter';
  static const String bodyFont = 'Inter';
  static const String monoFont = 'JetBrainsMono';

  static TextTheme get textTheme {
    final inter = GoogleFonts.interTextTheme();

    return TextTheme(
      // Display – heroic, low frequency
      displayLarge: inter.displayLarge?.copyWith(
        fontSize: 57, height: 1.12, letterSpacing: -0.25,
        fontWeight: FontWeight.w800,
      ),
      displayMedium: inter.displayMedium?.copyWith(
        fontSize: 45, height: 1.16,
        fontWeight: FontWeight.w700,
      ),
      displaySmall: inter.displaySmall?.copyWith(
        fontSize: 36, height: 1.22,
        fontWeight: FontWeight.w700,
      ),

      // Headline – section entry points
      headlineLarge: inter.headlineLarge?.copyWith(
        fontSize: 32, height: 1.25,
        fontWeight: FontWeight.w600,
      ),
      headlineMedium: inter.headlineMedium?.copyWith(
        fontSize: 28, height: 1.29,
        fontWeight: FontWeight.w600,
      ),
      headlineSmall: inter.headlineSmall?.copyWith(
        fontSize: 24, height: 1.33,
        fontWeight: FontWeight.w600,
      ),

      // Title – card titles, medium-emphasis headings
      titleLarge: inter.titleLarge?.copyWith(
        fontSize: 22, height: 1.27,
        fontWeight: FontWeight.w600,
      ),
      titleMedium: inter.titleMedium?.copyWith(
        fontSize: 16, height: 1.50, letterSpacing: 0.15,
        fontWeight: FontWeight.w600,
      ),
      titleSmall: inter.titleSmall?.copyWith(
        fontSize: 14, height: 1.43, letterSpacing: 0.1,
        fontWeight: FontWeight.w500,
      ),

      // Body – reading text
      bodyLarge: inter.bodyLarge?.copyWith(
        fontSize: 16, height: 1.60, letterSpacing: 0.15,
      ),
      bodyMedium: inter.bodyMedium?.copyWith(
        fontSize: 14, height: 1.50, letterSpacing: 0.10,
      ),
      bodySmall: inter.bodySmall?.copyWith(
        fontSize: 12, height: 1.40, letterSpacing: 0.25,
        fontWeight: FontWeight.w400,
      ),

      // Label – button text, captions, overlines
      labelLarge: inter.labelLarge?.copyWith(
        fontSize: 14, height: 1.43, letterSpacing: 0.1,
        fontWeight: FontWeight.w600,
      ),
      labelMedium: inter.labelMedium?.copyWith(
        fontSize: 12, height: 1.33, letterSpacing: 0.5,
        fontWeight: FontWeight.w500,
      ),
      labelSmall: inter.labelSmall?.copyWith(
        fontSize: 11, height: 1.45, letterSpacing: 0.5,
        fontWeight: FontWeight.w500,
      ),
    );
  }

  static TextStyle codeStyle([double size = 14]) => TextStyle(
    fontFamily: monoFont,
    fontSize: size,
    height: 1.5,
    letterSpacing: 0,
    fontWeight: FontWeight.w400,
  );

  static TextStyle buttonLabel({required double size}) => TextStyle(
    fontFamily: displayFont,
    fontSize: size,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.3,
  );
}
