import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class AppToast {
  AppToast._();

  static void show(BuildContext context, String message, {
    IconData? icon,
    Color? color,
    Duration duration = const Duration(seconds: 3),
  }) {
    final overlay = Overlay.of(context);
    late OverlayEntry entry;

    entry = OverlayEntry(
      builder: (context) => _ToastWidget(
        message: message,
        icon: icon,
        color: color,
        duration: duration,
        onDismiss: () => entry.remove(),
      ),
    );

    overlay.insert(entry);
  }

  static void success(BuildContext context, String message) {
    show(context, message, icon: Icons.check_circle, color: DSColors.safe);
  }

  static void error(BuildContext context, String message) {
    show(context, message, icon: Icons.error_outline, color: DSColors.danger);
  }

  static void warning(BuildContext context, String message) {
    show(context, message, icon: Icons.warning_amber, color: DSColors.warning);
  }

  static void info(BuildContext context, String message) {
    show(context, message, icon: Icons.info_outline, color: DSColors.neonViolet);
  }
}

class _ToastWidget extends StatefulWidget {
  final String message;
  final IconData? icon;
  final Color? color;
  final Duration duration;
  final VoidCallback onDismiss;

  const _ToastWidget({
    required this.message,
    this.icon,
    this.color,
    required this.duration,
    required this.onDismiss,
  });

  @override
  State<_ToastWidget> createState() => _ToastWidgetState();
}

class _ToastWidgetState extends State<_ToastWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _anim;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 500.ms);
    _anim = Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));
    _controller.forward();
    Future.delayed(widget.duration, _dismiss);
  }

  void _dismiss() {
    _controller.reverse().then((_) => widget.onDismiss());
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final col = widget.color ?? DSColors.circuitCyan;

    return FadeTransition(
      opacity: _anim,
      child: SlideTransition(
        position: Tween<Offset>(begin: const Offset(0, -0.5), end: Offset.zero).animate(_anim),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.only(top: 16, left: 16, right: 16),
            child: Material(
              elevation: 8,
              borderRadius: BorderRadius.circular(14),
              color: Theme.of(context).brightness == Brightness.dark
                  ? DSColors.surfaceDarkCard : DSColors.white,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: col.withValues(alpha: 0.3), width: 1),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (widget.icon != null) ...[
                      Icon(widget.icon, color: col, size: 20),
                      const SizedBox(width: 10),
                    ],
                    Expanded(child: Text(widget.message, style: const TextStyle(fontSize: 14))),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
