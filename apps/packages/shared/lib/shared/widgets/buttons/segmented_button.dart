import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

enum AppSegmentedVariant { standard, brand }

class AppSegmentedButton extends StatelessWidget {
  final List<String> labels;
  final int selectedIndex;
  final ValueChanged<int> onChanged;
  final AppSegmentedVariant variant;

  const AppSegmentedButton({
    super.key,
    required this.labels,
    required this.selectedIndex,
    required this.onChanged,
    this.variant = AppSegmentedVariant.standard,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.r12),
        color: isDark ? const Color(0xFF1C2333) : const Color(0xFFF0F0F0),
      ),
      padding: const EdgeInsets.all(4),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: List.generate(labels.length, (i) => _buildSegment(i, isDark, theme)),
      ),
    );
  }

  Widget _buildSegment(int index, bool isDark, ThemeData theme) {
    final isSelected = index == selectedIndex;

    return GestureDetector(
      onTap: () => onChanged(index),
      child: AnimatedContainer(
        duration: 200.ms,
        curve: Curves.easeInOut,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(DSDimensions.r8),
          color: isSelected ? DSColors.primary : Colors.transparent,
          boxShadow: isSelected
              ? [BoxShadow(color: DSColors.primary.withValues(alpha: 0.3), blurRadius: 8)]
              : null,
        ),
        child: Text(
          labels[index],
          style: TextStyle(
            fontSize: 13,
            fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
            color: isSelected ? DSColors.onPrimary : (isDark ? DSColors.white : DSColors.grey700),
          ),
        ),
      ),
    );
  }
}
