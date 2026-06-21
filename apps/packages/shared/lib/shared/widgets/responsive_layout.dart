import 'package:flutter/material.dart';
import 'package:responsive_framework/responsive_framework.dart';
import '../design_system/dimensions.dart';

class ResponsiveLayout extends StatelessWidget {
  final Widget child;

  const ResponsiveLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return ResponsiveBreakpoints.builder(
      child: child,
      breakpoints: [
        const Breakpoint(start: 0, end: DSDimensions.mobile, name: MOBILE),
        const Breakpoint(start: DSDimensions.mobile, end: DSDimensions.desktop, name: TABLET),
        const Breakpoint(start: DSDimensions.desktop, end: double.infinity, name: DESKTOP),
      ],
    );
  }
}
