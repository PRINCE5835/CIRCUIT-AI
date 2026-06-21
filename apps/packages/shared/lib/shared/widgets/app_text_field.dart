import 'package:flutter/material.dart';
import '../design_system/dimensions.dart';
import '../design_system/colors.dart';

class AppTextField extends StatefulWidget {
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

  const AppTextField({
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
  State<AppTextField> createState() => _AppTextFieldState();
}

class _AppTextFieldState extends State<AppTextField> {
  bool _obscured = true;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final hasError = widget.errorText != null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.label.isNotEmpty) ...[
          Row(
            children: [
              Text(widget.label, style: theme.textTheme.labelLarge),
              if (widget.isRequired)
                Text(' *', style: theme.textTheme.labelLarge?.copyWith(
                  color: theme.colorScheme.error,
                )),
            ],
          ),
          const SizedBox(height: DSDimensions.s4),
        ],
        TextFormField(
          controller: widget.controller,
          focusNode: widget.focusNode,
          keyboardType: widget.keyboardType,
          textInputAction: widget.textInputAction,
          obscureText: widget.isPassword ? _obscured : false,
          readOnly: widget.isReadOnly,
          maxLines: widget.isPassword ? 1 : widget.maxLines,
          maxLength: widget.maxLength,
          onChanged: widget.onChanged,
          onFieldSubmitted: widget.onSubmitted,
          validator: widget.validator,
          decoration: InputDecoration(
            hintText: widget.hint,
            errorText: widget.errorText,
            prefixIcon: widget.prefixIcon,
            suffixIcon: widget.isPassword
                ? IconButton(
                    icon: Icon(_obscured ? Icons.visibility_outlined : Icons.visibility_off_outlined),
                    onPressed: () => setState(() => _obscured = !_obscured),
                    color: hasError
                        ? theme.colorScheme.error
                        : isDark
                            ? DSColors.grey400
                            : DSColors.grey500,
                  )
                : widget.suffixIcon,
            filled: true,
            fillColor: hasError
                ? theme.colorScheme.errorContainer.withValues(alpha: 0.3)
                : isDark
                    ? DSColors.surfaceDarkCard
                    : DSColors.grey50,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
              borderSide: BorderSide(
                color: hasError
                    ? theme.colorScheme.error
                    : isDark
                        ? DSColors.white.withValues(alpha: 0.10)
                        : DSColors.black.withValues(alpha: 0.10),
              ),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
              borderSide: BorderSide(
                color: isDark
                    ? DSColors.white.withValues(alpha: 0.10)
                    : DSColors.black.withValues(alpha: 0.10),
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
              borderSide: BorderSide(
                color: hasError ? theme.colorScheme.error : theme.colorScheme.primary,
                width: 1.5,
              ),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
              borderSide: const BorderSide(color: DSColors.danger),
            ),
            focusedErrorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(DSDimensions.inputRadius),
              borderSide: const BorderSide(color: DSColors.danger, width: 1.5),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: DSDimensions.s16,
              vertical: DSDimensions.s14,
            ),
          ),
        ),
      ],
    );
  }
}
