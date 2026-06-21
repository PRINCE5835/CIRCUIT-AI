import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class NeoTextField extends StatefulWidget {
  final String label;
  final String? hint;
  final String? errorText;
  final TextEditingController? controller;
  final FocusNode? focusNode;
  final TextInputType? keyboardType;
  final TextInputAction? textInputAction;
  final bool isPassword;
  final bool isReadOnly;
  final bool isRequired;
  final int? maxLines;
  final int? maxLength;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final FormFieldValidator<String>? validator;

  const NeoTextField({
    super.key,
    required this.label,
    this.hint,
    this.errorText,
    this.controller,
    this.focusNode,
    this.keyboardType,
    this.textInputAction,
    this.isPassword = false,
    this.isReadOnly = false,
    this.isRequired = false,
    this.maxLines = 1,
    this.maxLength,
    this.prefixIcon,
    this.suffixIcon,
    this.onChanged,
    this.onSubmitted,
    this.validator,
  });

  @override
  State<NeoTextField> createState() => _NeoTextFieldState();
}

class _NeoTextFieldState extends State<NeoTextField> with SingleTickerProviderStateMixin {
  late FocusNode _focusNode;
  bool _obscured = false;

  @override
  void initState() {
    super.initState();
    _focusNode = widget.focusNode ?? FocusNode();
    _focusNode.addListener(() => setState(() {}));
    _obscured = widget.isPassword;
  }

  @override
  void dispose() {
    if (widget.focusNode == null) _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final isFocused = _focusNode.hasFocus;
    final hasError = widget.errorText != null && widget.errorText!.isNotEmpty;

    Color borderColor;
    if (hasError) {
      borderColor = DSColors.danger;
    } else if (isFocused) {
      borderColor = DSColors.circuitCyan;
    } else {
      borderColor = isDark ? DSColors.white.withValues(alpha: 0.12) : DSColors.black.withValues(alpha: 0.12);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.label.isNotEmpty) ...[
          Row(
            children: [
              Text(widget.label, style: theme.textTheme.labelLarge),
              if (widget.isRequired)
                Text(' *', style: TextStyle(color: DSColors.danger, fontWeight: FontWeight.w600)),
            ],
          ),
          const SizedBox(height: DSDimensions.s6),
        ],
        AnimatedContainer(
          duration: 200.ms,
          curve: Curves.easeInOut,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
            color: isDark ? DSColors.surfaceDarkCard : const Color(0xFFF5F5F5),
            border: Border.all(color: borderColor, width: isFocused ? 1.5 : 1),
            boxShadow: isFocused
                ? [BoxShadow(color: DSColors.circuitCyan.withValues(alpha: 0.1), blurRadius: 8, spreadRadius: 1)]
                : null,
          ),
          child: TextField(
            controller: widget.controller,
            focusNode: _focusNode,
            keyboardType: widget.keyboardType,
            textInputAction: widget.textInputAction,
            obscureText: _obscured,
            readOnly: widget.isReadOnly,
            maxLines: widget.isPassword ? 1 : widget.maxLines,
            maxLength: widget.maxLength,
            onChanged: widget.onChanged,
            onSubmitted: widget.onSubmitted,
            style: theme.textTheme.bodyLarge,
            decoration: InputDecoration(
              hintText: widget.hint,
              hintStyle: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey300),
              border: InputBorder.none,
              contentPadding: const EdgeInsets.symmetric(
                horizontal: DSDimensions.s16,
                vertical: DSDimensions.s14,
              ),
              prefixIcon: widget.prefixIcon != null
                  ? Padding(
                      padding: const EdgeInsets.only(left: 12, right: 8),
                      child: widget.prefixIcon,
                    )
                  : null,
              suffixIcon: widget.isPassword
                  ? IconButton(
                      icon: Icon(_obscured ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                          size: 20, color: isDark ? DSColors.grey400 : DSColors.grey500),
                      onPressed: () => setState(() => _obscured = !_obscured),
                    )
                  : (widget.suffixIcon != null
                      ? Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: widget.suffixIcon,
                        )
                      : null),
              counterText: '',
            ),
          ),
        ),
        if (hasError) ...[
          const SizedBox(height: DSDimensions.s4),
          Padding(
            padding: const EdgeInsets.only(left: 4),
            child: Row(
              children: [
                const Icon(Icons.error_outline, size: 14, color: DSColors.danger),
                const SizedBox(width: 4),
                Text(widget.errorText!, style: TextStyle(fontSize: 12, color: DSColors.danger)),
              ],
            ),
          ),
        ],
      ],
    );
  }
}
