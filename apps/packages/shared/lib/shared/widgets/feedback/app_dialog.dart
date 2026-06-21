import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';
import '../buttons/neo_button.dart';

class AppDialog {
  AppDialog._();

  static Future<T?> show<T>(BuildContext context, {
    required String title,
    required Widget content,
    String? confirmLabel,
    String? cancelLabel,
    VoidCallback? onConfirm,
    Color? accentColor,
    bool barrierDismissible = true,
  }) {
    return showDialog<T>(
      context: context,
      barrierDismissible: barrierDismissible,
      barrierColor: Colors.black54,
      builder: (context) => _DialogBody(
        title: title,
        content: content,
        confirmLabel: confirmLabel,
        cancelLabel: cancelLabel,
        onConfirm: onConfirm,
        accentColor: accentColor,
      ),
    );
  }

  static Future<bool?> confirm(BuildContext context, {
    required String title,
    required String message,
    String confirmLabel = 'Confirm',
    String cancelLabel = 'Cancel',
    Color? accentColor,
    bool isDangerous = false,
  }) {
    return show<bool>(context,
      title: title,
      accentColor: accentColor,
      content: Text(message, style: Theme.of(context).textTheme.bodyLarge),
      confirmLabel: confirmLabel,
      cancelLabel: cancelLabel,
      onConfirm: () => Navigator.of(context).pop(true),
    );
  }

  static Future<String?> input(BuildContext context, {
    required String title,
    String? hintText,
    String confirmLabel = 'Submit',
    String? initialValue,
    bool isPassword = false,
    TextInputType? keyboardType,
  }) {
    final controller = TextEditingController(text: initialValue);
    return show<String>(context,
      title: title,
      content: Padding(
        padding: const EdgeInsets.only(top: 8),
        child: TextField(
          controller: controller,
          obscureText: isPassword,
          keyboardType: keyboardType,
          decoration: InputDecoration(hintText: hintText),
          autofocus: true,
        ),
      ),
      confirmLabel: confirmLabel,
      onConfirm: () => Navigator.of(context).pop(controller.text),
    );
  }

  static void loading(BuildContext context, {String? message}) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => PopScope(
        canPop: false,
        child: _LoadingDialogBody(message: message ?? 'Please wait...'),
      ),
    );
  }

  static void hide(BuildContext context) {
    Navigator.of(context).pop();
  }
}

class _DialogBody extends StatelessWidget {
  final String title;
  final Widget content;
  final String? confirmLabel;
  final String? cancelLabel;
  final VoidCallback? onConfirm;
  final Color? accentColor;

  const _DialogBody({
    required this.title,
    required this.content,
    this.confirmLabel,
    this.cancelLabel,
    this.onConfirm,
    this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final col = accentColor ?? DSColors.circuitCyan;

    return AlertDialog(
      backgroundColor: isDark ? DSColors.surfaceDarkCard : DSColors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DSDimensions.dialogRadius),
      ),
      title: Text(title, style: Theme.of(context).textTheme.titleLarge),
      content: content,
      actions: [
        if (cancelLabel != null)
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text(cancelLabel!, style: TextStyle(color: Theme.of(context).colorScheme.onSurfaceVariant)),
          ),
        if (confirmLabel != null)
          NeoButton(
            label: confirmLabel!,
            variant: NeoButtonVariant.primary,
            isFullWidth: false,
            onPressed: onConfirm ?? () => Navigator.of(context).pop(true),
          ),
      ],
    ).animate().fadeIn(duration: 200.ms).scale(begin: const Offset(0.95, 0.95));
  }
}

class _LoadingDialogBody extends StatelessWidget {
  final String message;

  const _LoadingDialogBody({required this.message});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: Colors.transparent,
      elevation: 0,
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const _CircuitSpinnerIcon(size: 48),
          const SizedBox(height: 24),
          Text(message, style: const TextStyle(color: DSColors.white)),
        ],
      ),
    ).animate().fadeIn(duration: 200.ms);
  }
}

class _CircuitSpinnerIcon extends StatefulWidget {
  final double size;
  const _CircuitSpinnerIcon({this.size = 48});

  @override
  State<_CircuitSpinnerIcon> createState() => _CircuitSpinnerIconState();
}

class _CircuitSpinnerIconState extends State<_CircuitSpinnerIcon> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 1200.ms)..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RotationTransition(
      turns: _controller,
      child: Icon(Icons.circle_outlined, size: widget.size, color: DSColors.circuitCyan),
    );
  }
}
