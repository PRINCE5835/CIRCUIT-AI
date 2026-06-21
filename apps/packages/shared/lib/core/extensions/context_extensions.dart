import 'package:flutter/material.dart';

extension BuildContextExtensions on BuildContext {
  ThemeData get theme => Theme.of(this);
  TextTheme get textTheme => theme.textTheme;
  ColorScheme get colorScheme => theme.colorScheme;
  MediaQueryData get mediaQuery => MediaQuery.of(this);
  Size get screenSize => mediaQuery.size;
  double get screenWidth => screenSize.width;
  double get screenHeight => screenSize.height;
  bool get isMobile => screenWidth < 600;
  bool get isTablet => screenWidth >= 600 && screenWidth < 900;
  bool get isDesktop => screenWidth >= 900;
  EdgeInsets get padding => mediaQuery.padding;
  double get topPadding => padding.top;
  double get bottomPadding => padding.bottom;
}

extension StringExtensions on String {
  String get capitalized => '${this[0].toUpperCase()}${substring(1)}';
  String get titleCased => replaceAll(RegExp(r'[_-]'), ' ').split(' ').map((w) => w.capitalized).join(' ');
  bool get isValidEmail => RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  bool get isValidPassword => length >= 8;
}

extension WidgetExtensions on Widget {
  Widget paddingAll(double value) => Padding(padding: EdgeInsets.all(value), child: this);
  Widget paddingSymmetric({double h = 0, double v = 0}) => Padding(padding: EdgeInsets.symmetric(horizontal: h, vertical: v), child: this);
  Widget paddingOnly({double l = 0, double t = 0, double r = 0, double b = 0}) => Padding(padding: EdgeInsets.only(left: l, top: t, right: r, bottom: b), child: this);
  Widget sliver() => SliverToBoxAdapter(child: this);
}
