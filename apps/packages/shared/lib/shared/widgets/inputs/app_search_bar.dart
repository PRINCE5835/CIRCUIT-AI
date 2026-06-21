import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class AppSearchBar extends StatefulWidget {
  final String hint;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onSubmitted;
  final TextEditingController? controller;

  const AppSearchBar({
    super.key,
    this.hint = 'Search components, circuits...',
    this.onChanged,
    this.onSubmitted,
    this.controller,
  });

  @override
  State<AppSearchBar> createState() => _AppSearchBarState();
}

class _AppSearchBarState extends State<AppSearchBar> {
  late FocusNode _focusNode;
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(() => setState(() => _isFocused = _focusNode.hasFocus));
  }

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return AnimatedContainer(
      duration: 200.ms,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        color: isDark ? const Color(0xFF1C2333) : const Color(0xFFF0F0F0),
        border: Border.all(
          color: _isFocused
              ? DSColors.circuitCyan.withValues(alpha: 0.5)
              : (isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
          width: 1.5,
        ),
      ),
      child: TextField(
        controller: widget.controller,
        focusNode: _focusNode,
        onChanged: widget.onChanged,
        onSubmitted: (_) => widget.onSubmitted?.call(),
        style: Theme.of(context).textTheme.bodyLarge,
        decoration: InputDecoration(
          hintText: widget.hint,
          hintStyle: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey300),
          border: InputBorder.none,
          prefixIcon: Icon(Icons.search_rounded, color: isDark ? DSColors.grey400 : DSColors.grey500, size: 22),
          suffixIcon: _isFocused
              ? IconButton(
                  icon: Icon(Icons.close, color: isDark ? DSColors.grey400 : DSColors.grey500, size: 20),
                  onPressed: () {
                    widget.controller?.clear();
                    widget.onChanged?.call('');
                  },
                )
              : null,
          contentPadding: const EdgeInsets.symmetric(vertical: 14),
        ),
      ),
    );
  }
}
