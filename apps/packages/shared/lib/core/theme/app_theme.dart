import 'package:flutter/material.dart';
import '../../shared/design_system/colors.dart';
import '../../shared/design_system/typography.dart';
import '../../shared/design_system/dimensions.dart';
import '../../shared/design_system/shadows.dart';

abstract class AppTheme {
  AppTheme._();

  static ThemeData get light => _buildLight();
  static ThemeData get dark => _buildDark();

  static ThemeData _buildLight() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: DSColors.primary,
      brightness: Brightness.light,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: DSTypography.textTheme,
      fontFamily: DSTypography.displayFont,
      scaffoldBackgroundColor: DSColors.surfaceLight,
      appBarTheme: AppBarTheme(
        centerTitle: false,
        elevation: 0,
        scrolledUnderElevation: 1,
        backgroundColor: DSColors.surfaceLight,
        foregroundColor: DSColors.grey800,
        titleTextStyle: DSTypography.textTheme.titleLarge,
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        ),
        clipBehavior: Clip.antiAlias,
        color: DSColors.surfaceLightCard,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
          elevation: 0,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFFF5F5F5),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: BorderSide(color: DSColors.black.withValues(alpha: 0.12)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: BorderSide(color: DSColors.black.withValues(alpha: 0.12)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: const BorderSide(color: DSColors.primary, width: 1.5),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: const BorderSide(color: DSColors.danger),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: DSDimensions.s16,
          vertical: DSDimensions.s14,
        ),
      ),
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r8),
        ),
        backgroundColor: DSColors.glassDarkMedium,
      ),
      navigationBarTheme: NavigationBarThemeData(
        height: DSDimensions.navBarHeight,
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        indicatorShape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r12),
        ),
        indicatorColor: DSColors.primary.withValues(alpha: 0.12),
      ),
      dividerTheme: DividerThemeData(
        color: DSColors.black.withValues(alpha: 0.06),
        thickness: 1,
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: DSColors.primary,
        foregroundColor: DSColors.onPrimary,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r16),
        ),
      ),
    );
  }

  static ThemeData _buildDark() {
    const colorScheme = ColorScheme.dark(
      primary: DSColors.primary,
      onPrimary: DSColors.onPrimary,
      primaryContainer: DSColors.primaryContainer,
      onPrimaryContainer: DSColors.onPrimaryContainer,
      secondary: DSColors.secondary,
      onSecondary: DSColors.onSecondary,
      secondaryContainer: DSColors.secondaryContainer,
      onSecondaryContainer: DSColors.onSecondaryContainer,
      tertiary: DSColors.tertiary,
      onTertiary: DSColors.onTertiary,
      error: DSColors.error,
      onError: DSColors.onError,
      surface: DSColors.surfaceDark,
      onSurface: DSColors.white,
      onSurfaceVariant: DSColors.grey300,
      surfaceContainerHighest: DSColors.surfaceDarkCard,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: DSTypography.textTheme.apply(
        displayColor: DSColors.white,
        bodyColor: DSColors.white,
      ),
      fontFamily: DSTypography.displayFont,
      scaffoldBackgroundColor: DSColors.surfaceDark,
      appBarTheme: AppBarTheme(
        centerTitle: false,
        elevation: 0,
        scrolledUnderElevation: 1,
        backgroundColor: DSColors.surfaceDark,
        foregroundColor: DSColors.white,
        titleTextStyle: DSTypography.textTheme.titleLarge?.copyWith(color: DSColors.white),
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        ),
        clipBehavior: Clip.antiAlias,
        color: DSColors.surfaceDarkCard,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
          elevation: 0,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          minimumSize: const Size(DSDimensions.btnMinWidth, DSDimensions.btnHeight),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(DSDimensions.btnRadius),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: DSColors.surfaceDarkCard,
        hintStyle: TextStyle(color: DSColors.grey400),
        labelStyle: TextStyle(color: DSColors.grey300),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: BorderSide(color: DSColors.white.withValues(alpha: 0.12)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: BorderSide(color: DSColors.white.withValues(alpha: 0.12)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: const BorderSide(color: DSColors.primary, width: 1.5),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
          borderSide: const BorderSide(color: DSColors.danger),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: DSDimensions.s16,
          vertical: DSDimensions.s14,
        ),
      ),
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r8),
        ),
        backgroundColor: DSColors.glassMedium,
        labelStyle: TextStyle(color: DSColors.white),
      ),
      navigationBarTheme: NavigationBarThemeData(
        height: DSDimensions.navBarHeight,
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        indicatorShape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r12),
        ),
        indicatorColor: DSColors.primary.withValues(alpha: 0.2),
        backgroundColor: DSColors.surfaceDarkElevated,
      ),
      dividerTheme: DividerThemeData(
        color: DSColors.white.withValues(alpha: 0.06),
        thickness: 1,
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: DSColors.primary,
        foregroundColor: DSColors.onPrimary,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DSDimensions.r16),
        ),
      ),
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: DSColors.surfaceDarkElevated,
      ),
    );
  }
}
