import 'package:flutter/material.dart';

/// Monopo Saigon Design System Tokens & App Theme
class AppColors {
  AppColors._();

  static const Color obsidian = Color(0xFF000000);
  static const Color paper = Color(0xFFFFFFFF);
  static const Color inkstone = Color(0xFF181818);
  static const Color cardBg = Color(0xFF121212);
  static const Color feltGray = Color(0xFF6D6D6D);
  static const Color slatePill = Color(0xFF636363);
  static const Color ashMist = Color(0xFF9A9A9A);
  static const Color hairline = Color(0xFF262626);
  static const Color surfaceBorder = Color(0xFF333333);

  // Semantic Status Colors (Used strictly for status and risk indicators)
  static const Color positive = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFFB300);
  static const Color critical = Color(0xFFE53935);
  static const Color info = Color(0xFF29B6F6);

  // Iridescent Hero Gradient (Restricted exclusively to atmospheric hero media)
  static const LinearGradient iridescentGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFA0E0AB),
      Color(0xFFFFAC2E),
      Color(0xFFA52D25),
    ],
  );
}

class AppTypography {
  AppTypography._();

  static const TextStyle heroHeadline = TextStyle(
    color: AppColors.paper,
    fontSize: 32,
    fontWeight: FontWeight.w300,
    letterSpacing: -0.5,
    height: 1.15,
  );

  static const TextStyle screenTitle = TextStyle(
    color: AppColors.paper,
    fontSize: 22,
    fontWeight: FontWeight.w600,
    letterSpacing: -0.2,
  );

  static const TextStyle cardHeader = TextStyle(
    color: AppColors.ashMist,
    fontSize: 11,
    fontWeight: FontWeight.w700,
    letterSpacing: 1.2,
  );

  static const TextStyle metricLarge = TextStyle(
    color: AppColors.paper,
    fontSize: 20,
    fontWeight: FontWeight.w700,
    fontFamily: 'monospace',
    letterSpacing: -0.5,
  );

  static const TextStyle metricMedium = TextStyle(
    color: AppColors.paper,
    fontSize: 16,
    fontWeight: FontWeight.w600,
    fontFamily: 'monospace',
  );

  static const TextStyle bodyRegular = TextStyle(
    color: AppColors.paper,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.4,
  );

  static const TextStyle bodySecondary = TextStyle(
    color: AppColors.ashMist,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    height: 1.3,
  );

  static const TextStyle buttonLabel = TextStyle(
    color: AppColors.paper,
    fontSize: 12,
    fontWeight: FontWeight.w700,
    letterSpacing: 0.8,
  );

  static const TextStyle badgeLabel = TextStyle(
    color: AppColors.paper,
    fontSize: 10,
    fontWeight: FontWeight.w700,
    letterSpacing: 0.6,
  );
}

class AppTheme {
  AppTheme._();

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.obsidian,
      primaryColor: AppColors.paper,
      cardColor: AppColors.inkstone,
      dividerColor: AppColors.hairline,
      splashColor: Colors.transparent,
      highlightColor: Colors.transparent,
      fontFamily: 'sans-serif',
      colorScheme: const ColorScheme.dark(
        primary: AppColors.paper,
        secondary: AppColors.slatePill,
        surface: AppColors.inkstone,
        background: AppColors.obsidian,
        error: AppColors.critical,
        onPrimary: AppColors.obsidian,
        onSecondary: AppColors.paper,
        onSurface: AppColors.paper,
        onBackground: AppColors.paper,
        onError: AppColors.paper,
      ),
      cardTheme: const CardTheme(
        color: AppColors.inkstone,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.zero,
          side: BorderSide(color: AppColors.hairline, width: 1.0),
        ),
        margin: EdgeInsets.zero,
      ),
      inputDecorationTheme: const InputDecorationTheme(
        filled: true,
        fillColor: AppColors.inkstone,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.zero,
          borderSide: BorderSide(color: AppColors.hairline, width: 1.0),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.zero,
          borderSide: BorderSide(color: AppColors.hairline, width: 1.0),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.zero,
          borderSide: BorderSide(color: AppColors.paper, width: 1.0),
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        hintStyle: TextStyle(color: AppColors.feltGray, fontSize: 13),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.paper,
          foregroundColor: AppColors.obsidian,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(75.0),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          textStyle: AppTypography.buttonLabel,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.paper,
          side: const BorderSide(color: AppColors.hairline, width: 1.0),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(75.0),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          textStyle: AppTypography.buttonLabel,
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.paper,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(75.0),
          ),
          textStyle: AppTypography.buttonLabel,
        ),
      ),
    );
  }
}
