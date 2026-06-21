import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';
import '../buttons/neo_button.dart';

class AppBottomSheet {
  AppBottomSheet._();

  static Future<T?> show<T>(BuildContext context, {
    required Widget child,
    String? title,
    double? maxHeight,
    bool useSafeArea = true,
    bool showHandle = true,
    bool isScrollControlled = true,
  }) {
    return showModalBottomSheet<T>(
      context: context,
      isScrollControlled: isScrollControlled,
      backgroundColor: Colors.transparent,
      barrierColor: Colors.black45,
      builder: (context) => _SheetBody(
        title: title,
        child: child,
        maxHeight: maxHeight,
        useSafeArea: useSafeArea,
        showHandle: showHandle,
      ),
    );
  }

  static Future<T?> actions<T>(BuildContext context, {
    required String title,
    required List<_ActionItem> actions,
  }) {
    return show<T>(context,
      title: title,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: actions.map((a) => ListTile(
          leading: Icon(a.icon, color: a.isDestructive ? DSColors.danger : null),
          title: Text(a.label, style: a.isDestructive ? TextStyle(color: DSColors.danger, fontWeight: FontWeight.w600) : null),
          subtitle: a.subtitle != null ? Text(a.subtitle!) : null,
          onTap: () {
            Navigator.of(context).pop();
            a.onTap?.call();
          },
        )).toList(),
      ),
    );
  }

  static Future<String?> audioInput(BuildContext context, {
    required String title,
    required Widget audioVisualizer,
  }) {
    return show<String>(context,
      title: title,
      maxHeight: 320,
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            audioVisualizer,
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                NeoButton(label: 'Cancel', variant: NeoButtonVariant.ghost, isFullWidth: false, onPressed: () => Navigator.of(context).pop()),
                NeoButton(label: 'Done', variant: NeoButtonVariant.primary, isFullWidth: false, onPressed: () => Navigator.of(context).pop('done')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _SheetBody extends StatelessWidget {
  final String? title;
  final Widget child;
  final double? maxHeight;
  final bool useSafeArea;
  final bool showHandle;

  const _SheetBody({
    this.title,
    required this.child,
    this.maxHeight,
    this.useSafeArea = true,
    this.showHandle = true,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bottomPadding = useSafeArea ? MediaQuery.of(context).padding.bottom : 0.0;

    return Container(
      margin: const EdgeInsets.only(top: 40),
      constraints: maxHeight != null ? BoxConstraints(maxHeight: maxHeight!) : null,
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(DSDimensions.sheetRadius),
          topRight: Radius.circular(DSDimensions.sheetRadius),
        ),
        color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
      ),
      child: Padding(
        padding: EdgeInsets.only(bottom: bottomPadding),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (showHandle) ...[
              const SizedBox(height: 12),
              Container(
                width: DSDimensions.sheetHandleWidth,
                height: 4,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(2),
                  color: isDark ? DSColors.grey400 : DSColors.grey200,
                ),
              ),
              const SizedBox(height: 8),
            ],
            if (title != null) ...[
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                child: Text(title!, style: Theme.of(context).textTheme.titleLarge),
              ),
              const Divider(),
            ],
            Flexible(child: child),
          ],
        ),
      ),
    ).animate().slideY(begin: 0.1, duration: 300.ms, curve: Curves.easeOut);
  }
}

class _ActionItem {
  final String label;
  final String? subtitle;
  final IconData icon;
  final bool isDestructive;
  final VoidCallback? onTap;

  _ActionItem({
    required this.label,
    this.subtitle,
    required this.icon,
    this.isDestructive = false,
    this.onTap,
  });
}
