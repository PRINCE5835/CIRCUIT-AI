import 'package:flutter/widgets.dart';

abstract class AnimationConstants {
  AnimationConstants._();

  static const Duration fast = Duration(milliseconds: 200);
  static const Duration medium = Duration(milliseconds: 350);
  static const Duration slow = Duration(milliseconds: 500);
  static const Duration pageTransition = Duration(milliseconds: 300);

  // Flutter Animate presets
  static const double fadeInBegin = 0.0;
  static const double fadeInEnd = 1.0;
  static const Offset slideUpBegin = Offset(0, 0.1);
  static const Offset slideUpEnd = Offset.zero;
  static const double scaleBegin = 0.95;
  static const double scaleEnd = 1.0;
}
